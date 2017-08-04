import json
import logging
import random
from unittest import TestCase

from iotclient import IOTClient
from iotclient.datanode import DataNode
from iotclient.value_type import ValueType

logging.basicConfig(level=logging.DEBUG)


class TestIOTClient(TestCase):
    @classmethod
    def setUpClass(cls):
        with open('config.json', 'r') as f:
            config = json.load(f)
            cls.username = config["username"]
            cls.password = config["password"]
            cls.base_url = config["base_url"]

    def setUp(self):
        self.client = IOTClient()
        self.client.set_credentials(self.username, self.password)

    def test_set_credentials(self):
        self.assertTrue(self.client.username, self.username)
        self.assertTrue(self.client.password, self.password)

    def test_connect(self):
        self.assertTrue(self.client.connect())
        self.assertTrue(self.client.is_connected())

    def test_disconnect(self):
        self.client.connect()
        self.assertTrue(self.client.is_connected())
        self.client.disconnect()
        self.assertFalse(self.client.is_connected())

    def test_save_data_node(self):
        data_node = DataNode("Temperature", ValueType.NUMBER, "°C", True, "Controller")
        self.client.connect()
        data_node = self.client.save_data_node(data_node)
        self.assertIsNotNone(data_node)
        self.assertEqual(data_node.name, "Temperature")
        self.assertEqual(data_node.value_type, ValueType.NUMBER)
        self.assertEqual(data_node.unit, "°C")
        self.assertEqual(data_node.keep_history, True)
        self.assertGreaterEqual(len(self.client.data_nodes), 1)

    def test_get_data_nodes(self):
        self.client.connect()
        data_nodes = self.client.get_data_nodes()
        self.assertGreater(len(data_nodes), 0)

    def test_update_data_node(self):
        self.client.connect()
        data_nodes = self.client.get_data_nodes()
        data_node = list(data_nodes.values())[0]
        data_node.name = "Temperature-XYZ"
        self.assertTrue(self.client.update_data_node(data_node))

    def test_delete_data_node(self):
        self.client.connect()
        data_node = DataNode("AboutToGetDeleted", ValueType.NUMBER, "Kg", True, "Test")
        data_node = self.client.save_data_node(data_node)
        self.assertTrue(self.client.delete_data_node(data_node))

    def test_save_data_node_value(self):
        self.client.connect()
        data_node = self.client.save_data_node(DataNode("Temperature", ValueType.NUMBER, "°C", True, "Controller"))
        value = data_node.new_value(random.randint(15, 30))
        response_value = self.client.save_data_node_value(value)
        self.assertIsNotNone(response_value)
