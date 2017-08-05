import json
import logging
import urllib.parse

import requests
from requests.auth import AuthBase

from iotclient.datanode import DataNode
from iotclient.datanode_value import DataNodeValue


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
        self.logger.debug("requesting data nodes.. (limit={0}, offset={1})".format(limit, offset))
        response = requests.get(self.base_url + "datanodes",
                                params={'limit': limit, 'offset': offset},
                                auth=OAuth2(self.token))
        if response.status_code != 200:
            raise RequestError(self.make_error_message(response))
        raw_data_nodes = json.loads(response.content)
        self.data_nodes = {}
        for raw_data_node in raw_data_nodes:
            data_node = DataNode.from_dict(raw_data_node)
            self.data_nodes[data_node.id] = data_node
        self.logger.debug("successfully got {0} data nodes.".format(len(self.data_nodes)))
        return self.data_nodes

    def get_data_node_by_name(self, path="", name=""):
        if not path and not name:
            self.logger.error("invalid parameters. name and path cannot both be empty!")
            return None

        self.get_data_nodes()
        for identifier, data_node in self.data_nodes.items():
            if data_node.name == name and data_node.path == path:
                return data_node
        return None

    def get_data_node_by_id(self, data_node_id):
        if not data_node_id:
            self.logger.error("invalid parameters. id must not be empty!")
            return None
        for identifier, data_node in self.data_nodes.items():
            if data_node_id == data_node.id:
                return data_node

        response = requests.get(self.base_url + "/datanodes/{0}".format(data_node_id), auth=OAuth2(self.token))

        if response.status_code != 200:
            raise RequestError(self.make_error_message(response))

        return DataNode.from_dict(json.loads(response.content))

    def save_data_node(self, data_node):
        if data_node.id and isinstance(data_node.id, int):
            logging.debug("updating existing data node with id: {0}".format(data_node.id))
            self.update_data_node(data_node)

        self.get_data_nodes()
        for existing_id, existing_data_node in self.data_nodes.items():
            if existing_data_node.full_name() == data_node.full_name():
                self.logger.warning("data node with same name and path already exists! not saving data node.")
                return existing_data_node

        self.logger.debug("saving data node..")
        response = requests.post(self.base_url + "datanodes",
                                 json.dumps(data_node.to_dict()),
                                 auth=OAuth2(self.token))

        if response.status_code != 201:
            raise RequestError(self.make_error_message(response))
        data_node = DataNode.from_dict(json.loads(response.content))
        self.data_nodes[data_node.id] = data_node
        self.logger.debug("successfully saved data node. received id: {0}".format(data_node.id))
        return data_node

    def update_data_node(self, data_node):
        if not data_node.id or not isinstance(data_node.id, int):
            self.logger.error("cannot update non-existing data node! data node must be saved first.")
            return False
        self.logger.debug("updating data node with id: {0} ..".format(data_node.id))
        response = requests.patch(self.base_url + "datanodes/" + str(data_node.id),
                                  json.dumps(data_node.to_dict()),
                                  auth=OAuth2(self.token))
        if response.status_code != 202:
            raise RequestError(self.make_error_message(response))
        data_node = DataNode.from_dict(json.loads(response.content))
        self.data_nodes[data_node.id] = data_node
        self.logger.debug("successfully updated data node with id: {0}".format(data_node.id))
        return data_node

    def delete_data_node(self, data_node):
        if not data_node.id or not isinstance(data_node.id, int):
            self.logger.error("cannot delete non-existing data node!")
            return False
        self.logger.debug("deleting data node with id: {0} ..".format(data_node.id))
        response = requests.delete(self.base_url + "datanodes/" + str(data_node.id),
                                   auth=OAuth2(self.token))
        if response.status_code != 200:
            raise RequestError(self.make_error_message(response))
        self.data_nodes.pop(data_node.id)
        return True

    def save_data_node_value(self, data_node_value):
        if data_node_value.id and isinstance(data_node_value.id, int):
            logging.debug("updating existing data node value with id: {0}".format(data_node_value.id))
            self.update_data_node_value(data_node_value)

        if not data_node_value.data_node:
            raise ValueError("data-node of value cannot be none")

        self.logger.debug("saving data node value..")
        response = requests.post(self.base_url + "datanodes/{0}/values".format(data_node_value.data_node.id),
                                 json.dumps(data_node_value.to_dict()),
                                 auth=OAuth2(self.token))

        if response.status_code != 201:
            raise RequestError(self.make_error_message(response))
        saved_data_node_value = DataNodeValue.from_dict(json.loads(response.content))
        data_node_value.data_node.values[saved_data_node_value.id] = saved_data_node_value

        self.logger.debug("successfully saved value of data-node. received id: {0}".format(saved_data_node_value.id))
        return saved_data_node_value

    def get_data_node_values(self, data_node, limit=50, offset=0):
        if not data_node.id or not isinstance(data_node.id, int):
            self.logger.error("cannot request data node values for data node without id!")
            return False

        self.logger.debug("requesting values of data node..")
        response = requests.get(self.base_url + "datanodes/{0}/values".format(data_node.id),
                                params={'limit': limit, 'offset': offset},
                                auth=OAuth2(self.token))
        if response.status_code != 200:
            raise RequestError(self.make_error_message(response))

        raw_values = json.loads(response.content)
        values = []
        for raw_value in raw_values:
            values.append(DataNodeValue.from_dict(raw_value))
        self.logger.debug("successfully got {0} values for data node with id:{1}".format(len(values), data_node.id))
        return values

    def get_current_data_node_value(self, data_node):
        try:
            return self.get_data_node_values(data_node, limit=1, offset=0)[0]
        except IndexError:
            return None

    def update_data_node_value(self, data_node_value):
        # TODO implement
        pass

    def make_error_message(self, response):
        return "api returned status code: {0} with message: {1}".format(response.status_code, response.content)
