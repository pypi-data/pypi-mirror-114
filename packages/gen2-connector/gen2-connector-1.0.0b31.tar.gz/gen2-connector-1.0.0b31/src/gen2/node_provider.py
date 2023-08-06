#
# (C) Copyright IBM Corp. 2021
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import inspect

import logging
import time
from uuid import uuid4

import re
import threading

from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_platform_services import GlobalSearchV2, GlobalTaggingV1
from ibm_vpc import VpcV1
from ray.autoscaler.node_provider import NodeProvider
from ray.autoscaler.tags import TAG_RAY_CLUSTER_NAME, TAG_RAY_NODE_NAME, TAG_RAY_NODE_KIND, TAG_RAY_LAUNCH_CONFIG
from ray.autoscaler._private.cli_logger import cli_logger


logger = logging.getLogger(__name__)

INSTANCE_NAME_UUID_LEN = 8
INSTANCE_NAME_MAX_LEN = 64

#TODO: move to constants
PROFILE_NAME_DEFAULT = 'cx2-2x4'
VOLUME_TIER_NAME_DEFAULT = 'general-purpose'
RAY_RECYCLABLE = 'ray-recyclable'

ALL_STATUS_TAGS = ['ray-node-status:uninitialized', 'ray-node-status:waiting-for-ssh', 'ray-node-status:setting-up', 'ray-node-status:syncing-files', 'ray-node-status:up-to-date', 'ray-node-status:update-failed']
RETRIES = 5

WORKER = 'ray-node-type:worker'
HEAD = 'ray-node-type:head'

def _create_vpc_client(endpoint, authenticator):
    """
    Creates an IBM VPC python-sdk instance
    """
    ibm_vpc_client = VpcV1('2021-01-19', authenticator=authenticator)
    ibm_vpc_client.set_service_url(endpoint + '/v1')

    return ibm_vpc_client


class Gen2NodeProvider(NodeProvider):


    def retry_on_except(func):
        def decorated_func(*args, **kwargs):
            name = func.__name__
            for retry in range RETRIES:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    msg = f"Error in {name}, {e}, retries left {RETRIES}"
                    cli_logger.error(msg)
                    logger.exception(msg)

                    logger.info("reiniting the clients and waiting few seconds")
                    args[0]._init()
                    time.sleep(1)

            # we got here only because run out of retries, TODO: consider to return default empty instead of raising. raising may kill monitor
            raise e
        return decorated_func

    def log_in_out(func):

      def decorated_func(*args, **kwargs):
        name = func.__name__
        logger.info(f"Enter {name} from {inspect.stack()[0][3]} {inspect.stack()[1][3]}  {inspect.stack()[2][3]} with args: {args} and kwargs {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Leave {name} from {inspect.stack()[1][3]} with result {result}")
        except:
            cli_logger.error(f"Error in {name}")
            raise
        return result
      return decorated_func

    @log_in_out
    def _init(self):
        with self.lock:
            self.ibm_vpc_client = _create_vpc_client(self.endpoint, IAMAuthenticator(self.iam_api_key))
            self.global_tagging_service = GlobalTaggingV1(IAMAuthenticator(self.iam_api_key))
            self.global_search_service = GlobalSearchV2(IAMAuthenticator(self.iam_api_key))

    def __init__(self, provider_config, cluster_name):
        NodeProvider.__init__(self, provider_config, cluster_name)

        self.endpoint = self.provider_config["endpoint"]
        self.iam_api_key = self.provider_config["iam_api_key"]

        self._init()

        self.lock = threading.RLock()
        # Cache of node objects from the last nodes() call
        self.cached_nodes = {}
        self.pending_nodes = {}
        self.prev_nodes = {HEAD: set(), WORKER: set()}
        self.deleted_nodes = []

        self.cache_stopped_nodes = provider_config.get("cache_stopped_nodes", True)

    def _get_node_type(self, node):
        for tag in node['tags']:
            kv = tag.split(':')
            if kv[0] == 'ray-node-type':
                return kv[1]

#    @log_in_out
    @retry_on_except
    def non_terminated_nodes(self, tag_filters):
        # get all nodes tagged for cluster "query":"tags:\"ray-cluster-name:default\" AND tags:\"ray-node-type:head\""
        CLUSTER_NAME_QUERY = f"tags:\"{TAG_RAY_CLUSTER_NAME}:{self.cluster_name}\""
        query = CLUSTER_NAME_QUERY
        for k, v in sorted(tag_filters.items()):
            query += f" AND tags:\"{k}:{v}\""

        with self.lock:
            # retry search few times in case node misteriously dissapeared
            NT_RETRIES = 5
            for retry in range(NT_RETRIES):
                logger.info(f'self.global_search_service.search with query {query}')
                result = self.global_search_service.search(query=query, fields=['*']).get_result()

                items = result['items']
                nodes = []

                # update objects with floating ips. 
                for node in items:

                    # check if node marked for delete
                    if node['resource_id'] in self.deleted_nodes:
                        logger.info(f"{node['resource_id']} been scheduled for delete")
                        continue

                    # TODO: should be special case here in case of cache_stopped_nodes?
                    if node['doc']['status'] not in ['pending', 'starting', 'running']:
                        logger.info(f"{node['resource_id']} status {node['doc']['status']} not in ['pending', 'starting', 'running'], skipping")
                        continue

                    instance_id = node['resource_id']
                    try:
                        logger.info(f"getting instance {instance_id}")
                        # this one needed to filter out zombie resources
                        self.ibm_vpc_client.get_instance(instance_id)
                    except Exception as e:
                        cli_logger.warning(instance_id)
                        if e.message == 'Instance not found':
                            logger.error(f"failed to find instance {instance_id}, skipping")
                            continue
                        logger.error(f"failed to find instance {instance_id}, raising")
                        raise e

                    node_type = self._get_node_type(node)
                    if node_type == 'head':
                        nic_id = node['doc']['network_interfaces'][0]['id']
                        res = self.ibm_vpc_client.list_instance_network_interface_floating_ips(instance_id, nic_id).get_result()

                        floating_ips = res['floating_ips']
                        if len(floating_ips) == 0:
                            # not adding a head node that is missing floating ip
                            continue
                        else:
                            # currently head node should always have floating ip.
                            # in case floating ip present we want to add it
                            node['floating_ips'] = floating_ips
                    nodes.append(node)

                found_nodes = {node["resource_id"]: node for node in nodes}

                # check if previously cached node present in the list of found nodes
                logger.info(f'self.prev_nodes {self.prev_nodes} vs found_nodes {found_nodes.keys()}')

                # check if no worker disappeared
                prev_nodes_keys = []
                if WORKER in query:
                    prev_nodes_keys = self.prev_nodes.get(WORKER, set())
                elif HEAD in query:
                    prev_nodes_keys = self.prev_nodes.get(HEAD, set())
                else:
                    prev_nodes_keys = self.prev_nodes.get(HEAD, set())
                    prev_nodes_keys.update(self.prev_nodes.get(WORKER, set()))

                if prev_nodes_keys - found_nodes.keys():
                    # nodes shouldn't dissapear too frequently, if happened most likely it is a glitch in search, retry
#                    import pdb;pdb.set_trace()
                    logger.warning(f'{prev_nodes_keys - found_nodes.keys()} from perviously cached node missing in the list of found_nodes {found_nodes.keys()} found using query {query}, retrying search')
                    time.sleep(3)
                    continue
                else:
                    logger.info("new nodes dont miss any perviously cached nodes")
                    for node in nodes:
                        if HEAD in node['tags']:
                            self.prev_nodes[HEAD].add(node["resource_id"])
                        else:
                            self.prev_nodes[WORKER].add(node["resource_id"])
                    break

                # one or more nodes dissapeared, updating prev
                for n in prev_nodes_keys - found_nodes.keys():
                    self.prev_nodes[WORKER].discard(n)
                    self.prev_nodes[HEAD].discard(n)
                    self.cached_nodes.pop(n, None)

            for key in found_nodes.keys():
                self.cached_nodes[key] = found_nodes[key]
    
            node_ids = [node["resource_id"] for node in nodes]

            # workaround for issues woth tagging/searching
            for pend_id in list(self.pending_nodes.keys()):
                if pend_id in found_nodes:
                    if found_nodes[pend_id]['doc']['status'] == 'running':
                        #the instance seems to be running, lets remove it from pendings
                        self.pending_nodes.pop(pend_id, None)
                else:
                    # if instance in pendings for more than PENDING_TIMEOUT it is time to delete it
                    PENDING_TIMEOUT = 120
                    pending_time = self.pending_nodes[pend_id] - time.time()
                    logger.info(f'the instance {pend_id} is in pendings list for {pending_time}')
                    if pending_time > PENDING_TIMEOUT:
                        logger.error(f'pending timeout {PENDING_TIMEOUT} reached, deleting instance {pend_id}')
                        self._delete_node(pend_id)
                        self.pending_nodes.pop(pend_id)
                    else:
                        node_ids.append(pend_id)

        return node_ids

    @log_in_out
    def is_running(self, node_id):
        with self.lock:
            node = self._get_cached_node(node_id)
            return node['doc']['status'] == 'running'

    @log_in_out
    def is_terminated(self, node_id):
        with self.lock:
            node = self._get_cached_node(node_id)
            state = node['doc']['status']
            return state not in ["running", "starting", "pending"]

    def _tags_to_dict(self, tags_list):
        tags_dict = {}
        #logger.info(f'in _tags_to_dict with {tags_list}')
        for tag in tags_list:
            _tags_split = tag.split(':')
#            logger.info(f'in _tags_to_dict - {_tags_split}')
            tags_dict[_tags_split[0]] = _tags_split[1]

        return tags_dict

    @log_in_out
    def node_tags(self, node_id):
        with self.lock:
            node = self._get_cached_node(node_id)
            return self._tags_to_dict(node['tags'])

    def _get_hybrid_ip(self, node_id):
        node = self._get_cached_node(node_id)
        node_type = self._get_node_type(node)
        if node_type == 'head':
            fip = node.get("floating_ips")
            if fip:
                return fip[0]['address']

            node = self._get_node(node_id)
            fip = node.get("floating_ips")
            if fip:
                return fip[0]['address']
        else:
            return self.internal_ip(node_id)

    @log_in_out
    def external_ip(self, node_id):
        with self.lock:
            if self.provider_config.get('use_hybrid_ips'):
                return self._get_hybrid_ip(node_id)

            node = self._get_cached_node(node_id)

            fip = node.get("floating_ips")
            if fip:
                return fip[0]['address']
            
            node = self._get_node(node_id)
            fip = node.get("floating_ips")
            if fip:
                return fip[0]['address']

    def internal_ip(self, node_id):
        node = self._get_cached_node(node_id)

        try:
            primary_ipv4_address = node['doc']['network_interfaces'][0].get('primary_ipv4_address')
            if primary_ipv4_address is None:
                node = self._get_node(node_id)
        except Exception:
            node = self._get_node(node_id)

        return node['doc']['network_interfaces'][0].get('primary_ipv4_address')
    
    def _global_tagging_with_retries(self, resource_crn, f_name, tags=None):
        e = None
        resource_model = {'resource_id': resource_crn}
        for retry in range(RETRIES):
            logger.info(f'retry #{retry} to {f_name} {resource_crn}')
            try:
                if f_name == 'attach_tag':
                    tag_results = self.global_tagging_service.attach_tag(
                        resources=[resource_model],
                        tag_names=tags,
                        tag_type='user').get_result()
                    if not tag_results['results'][0]['is_error']:
                        return tag_results
                elif f_name == 'list_tags':
                    return self.global_tagging_service.list_tags(attached_to=resource_crn).get_result()['items']
                else:
                    #detach
                    tag_results = self.global_tagging_service.detach_tag(
                        resources=[resource_model],
                        tag_names=tags,
                        tag_type='user').get_result()
                    if not tag_results['results'][0]['is_error']:
                        return tag_results
                logger.error(f"failed to {f_name} tags {tags} for {resource_model}, {tag_results}")
            except Exception as e:
                logger.error(f"Failed to {f_name} {tags} for {resource_model}, {e}")

            if retry == RETRIES / 2:
                # try to reinit client
                self.global_tagging_service = GlobalTaggingV1(IAMAuthenticator(self.iam_api_key))

            time.sleep(10)

        # if exception occured and reinit didn't help, raise exception
        if e:
            raise e
        else:
            return False

    @log_in_out
    def set_node_tags(self, node_id, tags):
        node = self._get_node(node_id)
        with self.lock:
            resource_crn = node['crn']

            # detach all status tags
            if not self._global_tagging_with_retries(resource_crn, 'detach_tag', tags=ALL_STATUS_TAGS):
                logger.error("failed to detach old status tags")
                raise

            logger.info("===========================")
            logger.info(f"detached {ALL_STATUS_TAGS}")
            logger.info("===========================")

            time.sleep(1)

            # attach new tags
            _tags = [f"{k}:{v}" for k,v in tags.items()]
            if not self._global_tagging_with_retries(resource_crn, 'attach_tag', tags=_tags):
                cli_logger.error(f"failed to tag node {node_id} with tags {_tags}, raising error")
                raise

            logger.info("===========================")
            logger.info(f"attached {_tags}")
            logger.info("===========================")

#            # get latest tags
#            node_tags = [t['name'] for t in self._global_tagging_with_retries(node['crn'], 'list_tags')]
#            tags_dict = self._tags_to_dict(node_tags)
#
#            # remove from dict those that not overwritten
#            for old_tag_key in list(tags_dict.keys()):
#                if old_tag_key not in tags or tags.get(old_tag_key) == tags_dict[old_tag_key]:
#                    del tags_dict[old_tag_key]
#            
#            # convert to gen2 format
#            old_tags = [f"{k}:{v}" for k,v in tags_dict.items()]
#
#            # and now detach old tags. yes, it probably may break few things, because set_tags is not atomic
#            if old_tags:
#                if not self._global_tagging_with_retries(resource_crn, 'detach_tag', tags=old_tags):
#                    cli_logger.error(f"failed to untag node {node_id} with tags {old_tags}, raising error")
#                    raise
#
#                logger.info("===========================")
#                logger.info(f"detached {old_tags}")
#                logger.info("===========================")
#
            return {} 

    def _get_instance_data(self, name):
        """
        Returns the instance information
        """
        instances_data = self.ibm_vpc_client.list_instances(name=name).get_result()
        if len(instances_data['instances']) > 0:
            return instances_data['instances'][0]            
        return None

    def _create_instance(self, name, base_config):
        """
        Creates a new VM instance

        TODO: consider to use gen2 template file instead of generating dict
        """
        logger.debug("Creating new VM instance {}".format(name))

        security_group_identity_model = {'id': base_config['security_group_id']}
        subnet_identity_model = {'id': base_config['subnet_id']}
        primary_network_interface = {
            'name': 'eth0',
            'subnet': subnet_identity_model,
            'security_groups': [security_group_identity_model]
        }

        boot_volume_profile = {
            'capacity': 100,
            'name': '{}-boot'.format(name),
            'profile': {'name': base_config.get('volume_tier_name', VOLUME_TIER_NAME_DEFAULT)}}

        boot_volume_attachment = {
            'delete_volume_on_instance_delete': True,
            'volume': boot_volume_profile
        }

        key_identity_model = {'id': base_config['key_id']}
        profile_name = base_config.get('instance_profile_name', PROFILE_NAME_DEFAULT)

        instance_prototype = {}
        instance_prototype['name'] = name
        instance_prototype['keys'] = [key_identity_model]
        instance_prototype['profile'] = {'name': profile_name}
        instance_prototype['resource_group'] = {'id': base_config['resource_group_id']}
        instance_prototype['vpc'] = {'id': base_config['vpc_id']}
        instance_prototype['image'] = {'id': base_config['image_id']}
        instance_prototype['zone'] = {'name': self.provider_config['zone_name']}
        instance_prototype['boot_volume_attachment'] = boot_volume_attachment
        instance_prototype['primary_network_interface'] = primary_network_interface

        try:
            resp = self.ibm_vpc_client.create_instance(instance_prototype)
        except ApiException as e:
            if e.code == 400 and 'already exists' in e.message:
                return self._get_instance_data(name)
            elif e.code == 400 and 'over quota' in e.message:
                cli_logger.error("Create VM instance {} failed due to quota limit"
                             .format(name))
            else:
                cli_logger.error("Create VM instance {} failed with status code {}"
                             .format(name, str(e.code)))
            raise e

        logger.info("VM instance {} created successfully ".format(name))

        return resp.result

    def _create_floating_ip(self, base_config):
        """
        Creates or attaches floating IP address
        """
        if base_config.get('head_ip'):
            for ip in self.ibm_vpc_client.list_floating_ips().get_result()['floating_ips']:
                if ip['address'] == base_config['head_ip']:
                    return ip

        floating_ip_name = '{}-{}'.format(RAY_RECYCLABLE, uuid4().hex[:4]) 
            
        logger.debug('Creating floating IP {}'.format(floating_ip_name))
        floating_ip_prototype = {}
        floating_ip_prototype['name'] = floating_ip_name
        floating_ip_prototype['zone'] = {'name': self.provider_config['zone_name']}
        floating_ip_prototype['resource_group'] = {'id': base_config['resource_group_id']}
        response = self.ibm_vpc_client.create_floating_ip(floating_ip_prototype)
        floating_ip_data = response.result

        return floating_ip_data

    def _attach_floating_ip(self, instance, fip_data):
        fip = fip_data['address']
        fip_id = fip_data['id']

        logger.debug('Attaching floating IP {} to VM instance {}'.format(fip, instance['id']))

        # we need to check if floating ip is not attached already. if not, attach it to instance
        instance_primary_ni = instance['primary_network_interface']

        if instance_primary_ni['primary_ipv4_address'] and instance_primary_ni['id'] == fip_id:
            # floating ip already attached. do nothing
            logger.debug('Floating IP {} already attached to eth0'.format(fip))
        else:
            self.ibm_vpc_client.add_instance_network_interface_floating_ip(
                instance['id'], instance['network_interfaces'][0]['id'], fip_id)        

    def _stopped_nodes(self, tags):
        # get all nodes tagged for cluster "query":"tags:\"ray-cluster-name:default\" AND tags:\"ray-node-type:head\""
        query = f"tags:\"{TAG_RAY_CLUSTER_NAME}:{self.cluster_name}\""
        query += f" AND tags:\"{TAG_RAY_NODE_KIND}:{tags[TAG_RAY_NODE_KIND]}\""
        query += f" AND tags:\"{TAG_RAY_LAUNCH_CONFIG}:{tags[TAG_RAY_LAUNCH_CONFIG]}\""

        with self.lock:
            try:
                result = self.global_search_service.search(query=query, fields=['*']).get_result()
            except ApiException as e:
                cli_logger.warning(f"failed to query global search service with message: {e.message}, reiniting now")
                self.global_search_service = GlobalSearchV2(IAMAuthenticator(self.iam_api_key))
                result = self.global_search_service.search(query=query, fields=['*']).get_result()

            items = result['items']
            nodes = []

            # filter instances by state (stopped,stopping)
            for node in items:
                instance_id = node['resource_id']
                try:
                    instance = self.ibm_vpc_client.get_instance(instance_id)
                    state = node['doc']['status']
                    if state in ["stopped", "stopping"]:
                        nodes.append(node)
                except Exception as e:
                    cli_logger.warning(instance_id)
                    if e.message == 'Instance not found':
                       continue
                    raise e
            return nodes

    def _create_node(self, base_config, tags):
        name_tag = tags[TAG_RAY_NODE_NAME]
        assert (len(name_tag) <=
                (INSTANCE_NAME_MAX_LEN - INSTANCE_NAME_UUID_LEN - 1)) and re.match("^[a-z0-9-:-]*$", name_tag), (
                    name_tag, len(name_tag))

        name = "{name_tag}-{uuid}".format(
                                name_tag=name_tag,
                                uuid=uuid4().hex[:INSTANCE_NAME_UUID_LEN])
        logger.info(f"self._create_instance with {name}")
        instance = self._create_instance(name, base_config)

        tags[TAG_RAY_CLUSTER_NAME] = self.cluster_name

        _tags = [f"{k}:{v}" for k,v in tags.items()]
        if not self._global_tagging_with_retries(instance['crn'], 'attach_tag', tags=_tags):
            # terminate the weird node that failed to be tagged
            logger.error(f"failed to tag node {instance} with tags {_tags}, terminating instance")
            self._delete_node(instance['id'])
            return {}

        # currently always creating public ip for head node
        if tags['ray-node-type'] == 'head':# or not self.provider_config.get("use_internal_ips", False):
            fip_data = self._create_floating_ip(base_config)
            self._attach_floating_ip(instance, fip_data)

        return {instance['id']: instance}

    @log_in_out
    def create_node(self, base_config, tags, count) -> None:
        with self.lock:

            # here will be implementation of reuse of stopped instances
            stopped_nodes_dict = {}
        
            # Try to reuse previously stopped nodes with compatible configs
            if self.cache_stopped_nodes:
                stopped_nodes = self._stopped_nodes(tags)
                stopped_nodes_ids = [n['resource_id'] for n in stopped_nodes]
                stopped_nodes_dict = {n['resource_id']: n for n in stopped_nodes}

                if stopped_nodes:
                    cli_logger.print(f"Reusing nodes {stopped_nodes_ids}. "
                    "To disable reuse, set `cache_stopped_nodes: False` "
                    "under `provider` in the cluster configuration.")

                for node in stopped_nodes:
                    logger.info(f"Starting instance {node['resource_id']}")
                    self.ibm_vpc_client.create_instance_action(node['resource_id'], 'start')

                    # due to issues with tagging/searching services lets keep this node in pendings for now
                    self.pending_nodes[node['resource_id']] = time.time()

                time.sleep(1)

                for node_id in stopped_nodes_ids:
                    #import pdb;pdb.set_trace()
                    self.set_node_tags(node_id, tags)

                count -= len(stopped_nodes_ids)

            created_nodes_dict = {}
            while count > 0:
                created_nodes_dict = self._create_node(base_config, tags)

                # due to issues with tagging/searching services lets keep this node in pendings for now
                for k in created_nodes_dict:
                    self.pending_nodes[k] = time.time()
                    count -= 1


            all_created_nodes = stopped_nodes_dict
            all_created_nodes.update(created_nodes_dict)
            return all_created_nodes

    def _delete_node(self, resource_id):
        logger.error(f'in _delete_node with id {resource_id}')
        try:
            floating_ips = []

            try:
                node = self._get_node(resource_id)
                floating_ips = node.get('floating_ips', [])
            except:
                pass

            self.ibm_vpc_client.delete_instance(resource_id)

            for ip in floating_ips:
                if ip['name'].startswith(RAY_RECYCLABLE): # TODO: replace prefix with tags
                    self.ibm_vpc_client.delete_floating_ip(ip['id'])
        except ApiException as e:
            if e.code == 404:
                pass
            else:
                raise e

    @log_in_out
    def terminate_node(self, node_id):  # TODO: implement  terminate_nodes() as well to optimize. use instance group instead of single instance
        """
        Deletes the VM instance and the associated volume
        """
        logger.debug("Deleting VM instance {}".format(node_id))

        with self.lock:
            """
            Deletes the VM instance and the associated volume
            """
            try:
#                import pdb;pdb.set_trace()
                if self.cache_stopped_nodes:
                    cli_logger.print(f"Stopping instance {node_id}. To terminate instead, set `cache_stopped_nodes: False` "
                                    "under `provider` in the cluster configuration")

                    self.ibm_vpc_client.create_instance_action(node_id, 'stop')
                else:
                    self._delete_node(node_id)

                self.deleted_nodes.append(node_id)

                # and remove it from all caches
                self.prev_nodes[WORKER].discard(node_id)
                self.prev_nodes[HEAD].discard(node_id)

                self.cached_nodes.pop(node_id, None)
                self.pending_nodes.pop(node_id, None)
            except ApiException as e:
                if e.code == 404:
                    pass
                else:
                    raise e

    def _get_node(self, node_id):
        """Refresh and get info for this node, updating the cache."""
        self.non_terminated_nodes({})  # Side effect: updates cache

        with self.lock:
            if node_id in self.cached_nodes:
                return self.cached_nodes[node_id]

            try:
                node = self.ibm_vpc_client.get_instance(node_id).get_result()
            except Exception as e:
                logger.error(f'failed to get instance with id {node_id}')
                raise e
            try:
                node_tags = self._global_tagging_with_retries(node['crn'], 'list_tags')
                # TODO: what to do with a weird node that failed to list tags for?

            except Exception as e:
                logger.error(f'Error listing tags for node {node}: {e}')
                raise e

            return {"resource_id": node['id'], 'crn':  node['crn'], 'doc': node, 'tags': [t['name'] for t in node_tags]}

    def _get_cached_node(self, node_id):
        """Return node info from cache if possible, otherwise fetches it."""
        if node_id in self.cached_nodes:
            return self.cached_nodes[node_id]

        return self._get_node(node_id)


    @staticmethod
    def bootstrap_config(cluster_config):
        return cluster_config
