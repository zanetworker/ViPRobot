from scapy.config import Conf

__author__ = 'zanetworker'


import utils.ConfigurationUtils as ConfigurationUtils
import utils.CommonUtils as CommonUtils
import warnings
import time
import json

from utils.Constants import *


warnings.filterwarnings('ignore')

def status_completed(status):
    return True if status == STATUS_OK else False

def fetch_stats(post_response):
    return post_response['id'], post_response['state']


class CommandUtils:

    def __init__(self, communication_utils):   
        self.communication_utils = communication_utils

        #To track progress of an Aysnchronus Task
        self.status_counter = 0

        #A token to run the program sequentially
        self.free_token = True

    def list_storage_systems(self):
        storage_systems = self.communication_utils.get('vdc/storage-pools.json')
        print storage_systems

    def get_tenant(self):
        tenant_id = self.communication_utils.get('tenant.json')
        return tenant_id[0]['link']['href']


    def create_smis_provider(self):
        payload = ConfigurationUtils.load_smis_details()
        post_response, status = self.communication_utils.post('vdc/smis-providers.json', json_payload=payload)

        if not status_completed(status):
            task_id, state = fetch_stats(post_response)
            CommonUtils.log_this(__name__, "STATE is {0}".format(state.upper()), "")
            self.free_token = False
            result = "Task Completed" if self._prompt_status(task_id, 'Creating SMI-S Provider') else "Task Pending..!!"

        return result

    def create_storage_provider(self):
        result = None
        payload = ConfigurationUtils.load_vplex_details()
        post_response, status = self.communication_utils.post('vdc/storage-providers.json',  json_payload=payload)

        if not status_completed(status):
            task_id, state = fetch_stats(post_response)
            CommonUtils.log_this(__name__, "STATE is {0}".format(state.upper()), "")
            self.free_token = False
            result = "Task Completed" if self._prompt_status(task_id, 'Creating Storage Provider') else "Task Pending..!!"

        return result

    def create_cmcne_fabric_manager(self):
        payload = ConfigurationUtils.load_cmcne_details()
        post_response, status = self.communication_utils.post('vdc/network-systems', json_payload=payload)

        if not status_completed(status):
            task_id, state = fetch_stats(post_response)
            CommonUtils.log_this(__name__, "STATE is {0}".format(state.upper()), "")
            self.free_token = False
            result = "Task Completed" if self._prompt_status(task_id, 'Creating CMCNE Fabric') else "Task Pending..!!"

        return result

    def create_hosts(self):
        payloads = ConfigurationUtils.load_hosts_details()
        tenant_id = self.get_tenant()
        url = '{0}/hosts.json'.format(tenant_id).replace("/", "", 1)

        for i in range(0, len(payloads)):
            post_response, status = self.communication_utils.post(url, json_payload=payloads[i])

            if not status_completed(status):
                task_id, state = fetch_stats(post_response)
                CommonUtils.log_this(__name__, "STATE is {0}".format(state.upper()), "")
                result = "Task Completed" if self._prompt_status(task_id, 'Creating Host {0}'.format(i)) else "Task Pending..!!"
        return result
    #
    # def _prompt_status(self, task_id, task_name):
    #
    #     if self.status_counter == STATUS_COUNT_THRESHOLD:
    #         CommonUtils.log_this(__name__, VIPR_NOT_RESPONDING, "")
    #         self.free_token = True
    #         return
    #
    #     get_response, status = self.communication_utils.get('vdc/tasks/{0}.json'.format(task_id))
    #     task_id, state = fetch_stats(get_response)
    #     CommonUtils.log_this(__name__, "{0} is {1}".format(task_name, state.upper()), "")
    #     if state == 'ready':
    #         self.status_counter = 0
    #         self.free_token = True
    #         return True
    #     else:
    #         self.status_counter += 1
    #         time.sleep(1)
    #         self._prompt_status(task_id, task_name)


    def _prompt_status(self, task_id, task_name):

        self.free_token = False
        returnValue = False

        for i in range(0, STATUS_COUNT_THRESHOLD):

            get_response, status = self.communication_utils.get('vdc/tasks/{0}.json'.format(task_id))
            task_id, state = fetch_stats(get_response)
            CommonUtils.log_this(__name__, "{0} is {1}".format(task_name, state.upper()), "")

            if state == 'ready':
                self.free_token = True
                returnValue = True
                break

            else:
                if self.status_counter == STATUS_COUNT_THRESHOLD:
                    returnValue = False
                    break
                time.sleep(1)

        return returnValue

    def create_vPool(self):
        """TO_DO"""
        pass

    def create_vArray(self):
        """TO_DO"""
        pass

