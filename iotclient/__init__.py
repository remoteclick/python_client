import json
import logging
import urllib.parse

import requests
from requests.auth import AuthBase

from iotclient.datanode import DataNode


class RequestError(Exception):
    pass


class OAuth2(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = self.token
        return r


class IOTClient:
    def __init__(self):
        self.logger = logging.getLogger("IOTClient")
        self.password = ""
        self.username = ""
        self.base_url = "http://api.iotcloud.local/api/"
        self.connected = False

        self.name = ""
        self.manufacturer = ""
        self.device_type = ""
        self.description = ""
        self.data_nodes = {}
        self.id = ""
        self.token = ""

    def set_credentials(self, username, password):
        self.password = password
        self.username = username

    def set_base_url(self, base_url):
        self.base_url = base_url

    def connect(self):
        if self.connected:
            self.logger.warning("already connected!")
            return self.connected

        self.logger.debug("connecting..")
        response = requests.post(
            self.base_url + "oauth/device/token",
            urllib.parse.urlencode({'username': self.username, 'password': self.password, 'grant_type': 'password'})
        )
        if response.status_code != 200:
            raise ConnectionError(self.make_error_message(response))
        response_content = json.loads(response.content)
        self.name = response_content["name"]
        self.device_type = response_content["deviceType"]
        self.manufacturer = response_content["manufacturer"]
        self.id = response_content["id"]
        self.token = response_content["token"]
        self.connected = True
        self.logger.debug("successfully connected and authenticated.")
        return self.connected

    def is_connected(self):
        return self.connected

    def disconnect(self):
        self.connected = False

    def get_data_nodes(self, limit=50, offset=0):
        # TODO support params: limit, offset
        response = requests.get(self.base_url + "datanodes", auth=OAuth2(self.token))
        if response.status_code != 200:
            raise RequestError(self.make_error_message(response))
        raw_data_nodes = json.loads(response.content)
        self.data_nodes = {}
        for raw_data_node in raw_data_nodes:
            data_node = DataNode.from_dict(raw_data_node)
            self.data_nodes[data_node.id] = data_node
        self.logger.debug("successfully got {0} data nodes.".format(len(self.data_nodes)))
        return self.data_nodes

    def save_data_node(self, data_node):
        # TODO check if datanode with same name and path already exists
        response = requests.post(self.base_url + "datanodes",
                                 json.dumps(data_node.to_dict()),
                                 auth=OAuth2(self.token))
        if response.status_code != 201:
            raise RequestError(self.make_error_message(response))
        data_node = DataNode.from_dict(json.loads(response.content))
        self.data_nodes[data_node.id] = data_node
        self.logger.debug("successfully saved data node. received id: {0}".format(data_node.id))
        return data_node

    def make_error_message(self, response):
        return "api returned status code: {0} with message: {1}".format(response.status_code, response.content)
