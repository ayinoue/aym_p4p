#!/usr/bin/env python3

import os
import pymongo

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
