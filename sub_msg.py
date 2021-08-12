from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from setenv import db_user,db_pw
import os
import pymongo
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/ayinoue/aym_p4p/p4pj-316009-1268ec63115a.json'

# TODO(developer)
project_id = "p4pj-316009"
subscription_id = "RPi-data-sub"
# Number of seconds the subscriber should listen for messages
timeout = 5.0

# connect database
conn = "mongodb+srv://" + db_user + ":" + db_pw + "@cluster0.vaogw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(conn)
mydb = myclient.RPi
mycol = mydb.sensorData

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    #print(f"Received {message}.")
    #print(message)
    list_msg = [] 
    list_msg = message.data.decode('utf-8')
    values_list = list_msg.split(",")
    #print(values_list)
    set_db(values_list)
    ##message.ack()

# set data to mongodb 
def set_db(values_list):
    #Insert a document
    keys_list = ["datetime", "humidity"]
    mydoc = {}
    for i in range(len(keys_list)):
        mydoc[keys_list[i]] = values_list[i]

    #print(mydoc)
    #send data to mongodb per 10 min (hh:M"M":ss)
    if mydoc["datetime"][-4] == "0":
        mycol.insert_one(mydoc)
        pass

#print(f"Listening for messages on {subscription_path}..\n")

while True:
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    time.sleep(60)
