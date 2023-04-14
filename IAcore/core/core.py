import sys
import warnings
from abc import ABC, abstractmethod
#from time import time,sleep,localtime

#import cv2
#import numpy as np
#import pickle

#from skimage.exposure import match_histograms
#from sklearn.svm import LinearSVC

#import pyrealsense2 as rs

#from modbus_mqtt.libseedlingmodbus import SeedlingModbusClient
#from modbus_mqtt import libseedlingmodbus as lsmodb
#from paho.mqtt.client import Client as mqttClient

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

    @abstractmethod
    def operation(**kwargs):
        """interface to child classes
        """
        pass

class Initialize_mqqt_client(CoreRunningOps):
    """
    """

    def operation(**kwargs):
        if kwargs["op_mode"] == "run_op":
            print("Initializing mqqt client")
            """
            mqtt_client = mqttClient()
                if main_mqtt_client.is_connected():
                    mqtt_client.on_connect = on_connect_
                    mqtt_client.on_message = on_message_
            """
        elif kwargs["op_mode"] == "list_ops":
            kwargs["mqttclient"] = "mqttclient" #mqtt_client

        return kwargs

class Initialize_modbus_client(CoreRunningOps):
    """
    """

    def operation(**kwargs):
        if kwargs["op_mode"] == "run_op":
            print("Initializing modbus client")
            """
            modbus_client = SeedlingModbusClient(modServerIp,modServerPort)
            if modbus_client.connectToServer() is True:
                print("Modbus Client's connection -> successful")
            else:
                print("Modbus Client's connection -> failed")
            """
        elif kwargs["op_mode"] == "list_ops":
            kwargs["modbusclient"] = "modbusclient" #modbus_client

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
        if kwargs["op_mode"] == "run_op":
            print("Loading models")
            """
            model4horizontalimage = ...
            model4verticalimage = ...
            model4classification = ...
            """
        elif kwargs["op_mode"] == "list_ops":
            kwargs["model4horizontalimage"] = "model4horizontalimage" #model4horizontalimage
            kwargs["model4verticalimage"] = "model4verticalimage"
            kwargs["model4classification"] = "model4classification"

        return kwargs

class Send_waiting_state_to_PLC(CoreRunningOps):
    """ PLC needs to acknowleadge model core is up and running
    """

    def operation(**kwargs):
        if kwargs["op_mode"] == "run_op":
            print("Sending waiting state code to PLC")
            """
            if kwargs["modbus_client"].modbusConnectedFlag is True:
                kwargs["modbus_client"].writeCvStatus(lsmodb.CV_WAITING_STAT)
            """
        elif kwargs["op_mode"] == "list_ops":
            kwargs["sendwaitingstate2plc"] = "sendwaitingstate2plc"

        return kwargs

class Start_IAcore_PLC_connection_loop(CoreRunningOps):
    """ Endless loop to be connected to modbus. Models are used here
        when inputs are correctly loaded. Outputs are predictions
        en communication messaged for PLC.
    """

    def operation(**kwargs):
        if kwargs["op_mode"] == "run_op":
            print("Starting IA core PLC connection loop")
            """
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
            """
        elif kwargs["op_mode"] == "list_ops":
            kwargs["startiacoreplcconnectionloop"] = "startiacoreplcconnectionloop"

        return kwargs

class CoreRunning:
    """ Call all Core running operations
    """

    @staticmethod
    def call_operations(**kwargs):
        for operation in CoreRunningOps.__subclasses__():
            kwargs = operation.operation(**kwargs)

        return kwargs

