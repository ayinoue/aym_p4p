#!/usr/bin/env python3

import os
import pymongo
import time

###########################################################
#connect database
#db_user = os.environ["mongodb_user"]
#db_pw = os.environ["mongodb_pw"]
conn = "mongodb+srv://" + db_user + ":" + db_pw + "@cluster0.vaogw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(conn)
mydb = myclient.RPi
mycol = mydb.sensorData

###########################################################
#get currect soil humidity
def get_one():
    data = mycol.find().sort("_id", -1)
    value = ""
    for i in data:
        value = "土壌湿度" + i["humidity"] +  "%"
        break
    
    return value

#https://www.w3schools.com/python/python_mongodb_sort.asp

