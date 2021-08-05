#!/usr/bin/env python3

import os
import paho.mqtt.client as mqtt
import pymongo
import time

###########################################################
#connect database
db_user = os.environ["mongodb_user"]
db_pw = os.environ["mongodb_pw"]
conn = "mongodb+srv://" + db_user + ":" + db_pw + "@cluster0.vaogw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(conn)
mydb = myclient.RPi
mycol = mydb.sensorData

###########################################################
#set constant values for MQTT broker
BrokerAddress = "test.mosquitto.org"    # Cloud MQTT
MqttTopic = "ayinoueTopic"

###########################################################
#get currect soil humidity
def get_one():
    data = mycol.find().sort("_id", -1)

    for i in data:
        text = "土壌湿度" + i["humidity"] +  "%"
        break
    
    return text

###########################################################
#set db via mqtt
def set_db():
    #print("Connecting to MQTT broker:" + BrokerAddress)
    client = mqtt.Client()               # Create new instance with Any clientID
    msg = str(message.payload.decode("utf-8"))
    keys_list = ["datetime", "date", "time", "humidity"]
    values_list = msg.split(",")
    mydoc = {}
    for i in range(len(keys_list)):
        mydoc[keys_list[i]] = values_list[i]

    x = mycol.insert_one(mydoc)
    client.on_message=on_message         # Attach function to callback
    try:
        client.connect(BrokerAddress)    #connect to broker
    except:
        #print("***** Broker connection failed *****")
        exit(1) 

    ### Subscribe ###
    #print("Subscribe topic:", MqttTopic)
    client.subscribe(MqttTopic)          # Subscribe MQTT

    ### loop forever to wait a message ###
    #print("Waiting message...")
    client.loop_forever()                # Loop forever