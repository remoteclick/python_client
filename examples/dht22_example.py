#!/usr/bin/python
# coding=utf-8

from remoteclick import RemoteClickClient, DataNode
from remoteclick.value_type import ValueType
import RPi.GPIO as GPIO
import Adafruit_DHT  # see https://github.com/adafruit/Adafruit_Python_DHT
import time
import logging

logging.basicConfig(level=logging.DEBUG)

# Example script which:
# 1. cyclically reads the temperature from a DHT22 sensor (https://www.adafruit.com/product/385) and sends it to the remoteclick api
# 2. reads a read-write boolean value from the api and controls a relay with it

read_interval = 0.5  # interval with which sensor data is read and sent to the API

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11

GPIO.setmode(GPIO.BCM)  # use BCM numbering mode
GPIO_Temperature_Pin = 4  # set the BCM Pin Number of Temperature Pin
RELAIS_PIN = 25  # Pin with which relay is wired
GPIO.setup(RELAIS_PIN, GPIO.OUT)
GPIO.output(RELAIS_PIN, False)

if __name__ == '__main__':
    print('connecting to remoteclick api...')
    client = RemoteClickClient()
    client.set_credentials("<your-device-id>", "<your-device-password>")
    client.connect()

    # create and save new data node (if data node already exists, existing one will be returned instead)
    temperature_node = client.save_data_node(
        DataNode(name="Temperature", value_type=ValueType.NUMBER, unit="°C", keep_history=True,
                 path="", read_only=True)
    )

    ventilator_node = client.save_data_node(
        DataNode(name="Ventilator", value_type=ValueType.BOOLEAN, unit="", keep_history=True,
                 path="", read_only=False)
    )
    client.save_data_node_value(ventilator_node.new_value(False))

    print("starting read/write cycle..")
    try:
        while 1:

            # read_retry returns a tuple of humidity and temperature
            humidity, temperature = Adafruit_DHT.read_retry(DHTSensor, GPIO_Temperature_Pin)
            if temperature is not None:
                print('temperature: {0:0.1f}°C  | humidity = {1:0.1f}%'.format(temperature, humidity))

                # send temperature value to remoteclick api
                client.save_data_node_value(temperature_node.new_value(temperature))
            else:
                print('could not read data from sensor!')

            # get current ventilator control value
            ventilator_node_value = client.get_current_data_node_value(ventilator_node)
            # set the output pin
            GPIO.output(RELAIS_PIN, ventilator_node_value.value)

            print("-" * 30)
            time.sleep(read_interval)

    except KeyboardInterrupt:
        client.disconnect()
        GPIO.cleanup()
