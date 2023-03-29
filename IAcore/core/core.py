import sys
from time import time,sleep,localtime
import warnings

import cv2
import numpy as np
import pickle

from skimage.exposure import match_histograms
from sklearn.svm import LinearSVC

import pyrealsense2 as rs

from modbus_mqtt.libseedlingmodbus import SeedlingModbusClient
from modbus_mqtt import libseedlingmodbus as lsmodb
from paho.mqtt.client import Client as mqttClient

warnings.filterwarnings("ignore")

def on_connect_(self, userdata, flags, rc):
    print("Connected MQTT with result code " + str(rc))
    main_mqtt_client.subscribe("PUT_HERE_THE_TOPIC_OF_INTEREST_tinterest")

def on_message_(self, userdata, msg):
    topic = str(msg.topic)
    payload = str(msg.payload.decode('utf-8'))
    print("payload: " + payload)
    print("topic: " + topic)


class CoreRunningOps(ABC):
    """ Perform all operations for running the core
    """

    @abstracmethod
    def operation(**kwargs):
        """interface to child classes
        """
        pass

class Initialize_mqqt_client(CoreRunningOps):
    """
    """

    def operation(**kwargs):
        mqtt_client = mqttClient()
            if main_mqtt_client.is_connected():
                mqtt_client.on_connect = on_connect_
                mqtt_client.on_message = on_message_
        kwargs["mqtt_client"] = mqtt_client

        return kwargs

class Initialize_modbus_client(CoreRunningOps):
    """
    """

    def operation(**kwargs):
        modbus_client = SeedlingModbusClient(modServerIp,modServerPort)
        if modbus_client.connectToServer() is True:
            print("Modbus Client's connection -> successful")
        else:
            print("Modbus Client's connection -> failed")
        kwargs["modbus_client"] = modbus_client

        return kwargs

class Load_models(CoreRunningOps):
    """ Load models for three predictions
        - image segmentation for horizontal view
        - image segmentation for vertical view
        - seedling classification
        inputs:
            - horizontal picture
            - vertical pictur
        output:
            - json with predictions
    """

    def operation(**kwargs):
        #TODO
        model4horizontalimage = ...
        model4verticalimage = ...
        model4classification = ...

        kwargs["model4horizontalimage"] = model4horizontalimage
        kwargs["model4verticalimage"] = model4verticalimage
        kwargs["model4classification"] = model4classification

        return kwargs

class Send_waiting_state_to_PLC(CoreRunningOps):
    """ PLC needs to acknowleadge model core is up and running
    """

    def operation(**kwargs):
        if kwargs["modbus_client"].modbusConnectedFlag is True:
            kwargs["modbus_client"].writeCvStatus(lsmodb.CV_WAITING_STAT)

        return kwargs

class Start_IAcore_PLC_connection_loop(CoreRunningOps):
    """ Endless loop to be connected to modbus. Models are used here
        when inputs are correctly loaded. Outputs are predictions
        en communication messaged for PLC.
    """

    def operation(**kwargs):
        #TODO
        while True:
            if kwargs["modbus_client"].modbusConnectedFlag is True:
                plcInstruction = kwargs["modbus_client"].getPLCInstruction()
            if plcInstruction == lsmodb.PLC_PROCODD_INST:
                if CV_system_switch == "SysP":
                    if kwargs["modbus_client"].modbusConnectedFlag is True:
                        kwargs["modbus_client"].writeCvStatus(
                            lsmodb.CV_PROCESSING_STAT
                        )

                    if CV_MODE == "offline":

            elif plcInstruction == lsmodb.PLC_PROCEVEN_INST:
                if CV_system_switch is "SysP":
                    if kwargs["modbus_client"].modbusConnectedFlag is True:
                        kwargs["modbus_client"].writeCvStatus(
                            lsmodb.CV_PROCESSING_STAT
                        )

            try:
                cv2.imshow("Results",rgbGUI)
                cv2.waitKey(15)
            except:
                pass
                cv2.destroyAllWindows()

                return kwargs

class CoreRunning:
    """ Call all Core running operations
    """

    @staticmethod
    def call_operations(**kwargs):
        for operation in CoreRunningOps.__subclasses__():
            kwargs = operation.operation(**kwargs)

        return kwargs

