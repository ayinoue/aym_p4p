"""Publishes multiple messages to a Pub/Sub topic with an error handler."""

from google.cloud import pubsub_v1
import ADC0832
import datetime
import os
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/pi/.config/gcloud/application_default_credentials.json'

# TODO(developer)
project_id = "p4pj-316009"
topic_id = "RPi-data"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def setup():
    ADC0832.setup()

def loop():
    while True:
        res = ADC0832.getResult()
        value = (255 - res) * 100 / 255
        time_now = datetime.datetime.now()
        dt_json = {"datetime": "","humidity": ""}
        dt_json["datetime"] = time_now.strftime("%Y/%m/%d %H:%M:%S")
        dt_json["humidity"] = value
        str_dt_json = str(dt_json)
        publisher.publish(topic_path, str_dt_json.encode("utf-8"))
        time.sleep(60)

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        ADC0832.destroy()
        print ('The end !!')
