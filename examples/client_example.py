from iotclient import IOTClient, DataNode
from iotclient.value_type import ValueType

import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    client = IOTClient()
    client.set_credentials("<your-device-id>", "<your-device-password>")
    client.connect()
    # create and save new data node (if data node already exists, existing one will be returned instead)
    temperature_node = client.save_data_node(
        DataNode(name="Temperature", value_type=ValueType.NUMBER, unit="°C", keep_history=True,
                 path="Controller", read_only=True)
    )
    # create new value of data node
    value = temperature_node.new_value(23.5)
    # save the value
    client.save_data_node_value(value)
