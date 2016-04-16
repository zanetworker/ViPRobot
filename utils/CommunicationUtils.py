__author__ = 'zanetworker'

import ConfigurationUtils
import requests
import os
import json

from utils.ViPRobotExceptions import ViPRobotException
from utils.CommonUtils import log_this
from utils.token_request import TokenRequest
from utils.Constants import *

VIPR_CRED = ConfigurationUtils.load_vipr_credentials()



VIPR_HOST = VIPR_CRED['vipr_host']
VIPR_PORT = VIPR_CRED['vipr_port']


class CommunicationUtils:

    def __init__(self, username, password, token=None, verify_ssl=False, token_filename='token',
                 token_location='config',
                 request_timeout=15.0,
                 cache_token=True):

        self.username = str(username)
        self.password = str(password)
        self.token = token
        self.verify_ssl = verify_ssl
        self.token_filename = token_filename
        self.token_location = token_location
        self.request_timeout = request_timeout
        self.cache_token = cache_token
        self._session = requests.Session()
        self.vipr_endpoint = self._get_root_uri('').rstrip('/')
        self.token_endpoint = self._get_root_uri(LOGIN_URI).rstrip('/')
        self._token_request = TokenRequest(
            username=self.username,
            password=self.password,
            vipr_endpoint=self.vipr_endpoint,
            token_endpoint=self.token_endpoint,
            verify_ssl=self.verify_ssl,
            token_filename=self.token_filename,
            token_location=self.token_location,
            request_timeout=self.request_timeout,
            cache_token=self.cache_token)

        self.token_file = os.path.join(self.token_location, self.token_filename)


    def _get_root_uri(self, uri):
        return 'https://{0}:{1}{2}'.format(VIPR_HOST, VIPR_PORT, uri)

    def _construct_url(self, url):
        return '{0}/{1}'.format(self.vipr_endpoint, url)

    def _fetch_headers(self):
        if self.token:
            return {'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'x-sds-auth-token': self.token}
        else:
            return {'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'x-sds-auth-token': self._token_request.get_token()}

    def get(self, url, params=None):
        return self._request(url, params=params)

    def post(self, url, json_payload='{}'):
        return self._request(url, json_payload, http_verb='POST')

    def put(self, url, json_payload='{}'):
        return self._request(url, json_payload, http_verb='PUT')

    def _request(self, url, json_payload='{}', http_verb='GET', params=None):
            json_payload = json.dumps(json_payload)

            try:
                if http_verb == "PUT":
                    req = self._session.put(
                        self._construct_url(url),
                        verify=self.verify_ssl,
                        headers=self._fetch_headers(),
                        timeout=self.request_timeout,
                        data=json_payload)

                elif http_verb == 'POST':
                    req = self._session.post(
                        self._construct_url(url),
                        verify=self.verify_ssl,
                        headers=self._fetch_headers(),
                        timeout=self.request_timeout,
                        data=json_payload)

                else:  # Default to GET
                    req = self._session.get(
                        self._construct_url(url),
                        verify=self.verify_ssl,
                        headers=self._fetch_headers(),
                        timeout=self.request_timeout,
                        params=params)

                if req.status_code not in [STATUS_OK, STATUS_PENDING]:
                    raise ViPRobotException(
                        http_status_code=req.status_code,
                        vipr_message=req.text)
                return req.json(), req.status_code
                #return json.dumps(req.json(), sort_keys=True, indent=4), req.status_code

            except requests.ConnectionError as conn_err:
                raise ViPRobotException(message=conn_err.message)
            except requests.HTTPError as http_err:
                raise ViPRobotException(message=http_err.message)
            except requests.RequestException as req_err:
                raise ViPRobotException(message=req_err.message)
            except ValueError:
                return

