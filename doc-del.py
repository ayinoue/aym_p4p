#!/usr/bin/env python3

from setenv import db_user,db_pw
import os
import paho.mqtt.client as mqtt
import pymongo
import time

###########################################################
#####  Set constant values for MQTT broker   ##############

#BrokerAddress = "127.0.0.1"              # Local MQTT 
BrokerAddress = "test.mosquitto.org"    # Cloud MQTT
MqttTopic = "ayinoueTopic"

###########################################################
#connect database
conn = "mongodb+srv://" + db_user + ":" + db_pw + "@cluster0.vaogw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(conn)
mydb = myclient.RPi
mycol = mydb.sensorData

###########################################################
#####  Define functions   #################################

def on_message(client, userdata, message):  ### callback when get message from MQTT broker
    msg = str(message.payload.decode("utf-8"))
    #print("Message received:" + msg)
    set_db(msg)                             ### call Function set_db(msg)

def set_db(msg):                            ### set data to mongodb 
    #Insert a document
    keys_list = ["datetime", "date", "time", "humidity"]
    values_list = msg.split(",")
    mydoc = {}
    for i in range(len(keys_list)):
        mydoc[keys_list[i]] = values_list[i]

    x = mycol.insert_one(mydoc)
    #print (x)
    #print(mydoc)
    

###########################################################
#####  Main                     ###########################

mycol.remove({})
