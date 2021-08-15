from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from linebot import LineBotApi
from linebot.models import TextSendMessage
from oauth2client.service_account import ServiceAccountCredentials
from setenv import db_user,db_pw,spread_sheet_key,line_user_id,line_toooooooken
import ast
import gspread
import json
import os
import pymongo
import time

# setenv
jsonf = "/home/ayinoue/aym_p4p/p4pj-316009-1268ec63115a.json"
spsh_key = spread_sheet_key
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

enough_water = 1

def callback(message):
    str_json = message.data.decode('utf-8')
    set_db(str_json)
    push_line(str_json)
    #set_gspreadsheet(str_json)
    message.ack()

# set data to mongodb 
def set_db(str_json):
    #convert string to dictionary
    mydoc = ast.literal_eval(str_json)
    #send data to mongodb per 10 min (hh:M"M":ss)
    if mydoc["datetime"][-4] == "0":
        mycol.insert_one(mydoc)

def push_line(str_json):
    line_bot_api = LineBotApi(line_toooooooken)
    # enough water?
    mydoc = ast.literal_eval(str_json)
    water = int(mydoc["humidity"])
    if water < 90 and enough_water == 1:
        messages = TextSendMessage(text="ひまわり「そろそろ水がほしい」")
        line_bot_api.push_message(user_id, messages=messages)
        enough_water = 0
    elif water >= 90:
        enough_water = 1

def set_gspreadsheet(str_json):
    mydoc = ast.literal_eval(str_json)
    # (1) access to Google Spread Sheets
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(spsh_key).sheet1
    # (2) append values on Google Spread Sheets
    values = [mydoc["datetime"], mydoc["humidity"]]
    if mydoc["datetime"][-4] == "0":
        worksheet.append_row(values)

while True:
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    time.sleep(60)
