#!/usr/bin/python3
import Adafruit_DHT
import datetime
from ISStreamer.Streamer import Streamer
import time as t
import board
from influxdb import InfluxDBClient

# --------- User Settings ---------
SENSOR_LOCATION_NAME = "Jakubs Room"
BUCKET_NAME = ":partly_sunny: Room Temperatures"
BUCKET_KEY = "dht22sensor"
ACCESS_KEY = "1892"
MINUTES_BETWEEN_READS = 5
METRIC_UNITS = True
# ---------------------------------

# influx configuration - edit these
ifuser = "grafana"
ifpass = "liverpool1892"
ifdb   = "home"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "temperature"

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

sensor = 22
gpio = 4

while True:
    try:
        h_t = Adafruit_DHT.read_retry(sensor, gpio)
        humidity = h_t[0]
        temperature = h_t[1]
    except RuntimeError:
        print("RuntimeError, trying again...")
        continue

    humidity = format(humidity,".2f")
    temperature = format(temperature,".2f")

    streamer.log(SENSOR_LOCATION_NAME + " Temperature(C)", temperature)
    print(" Temperature(C)", temperature)

    streamer.log(SENSOR_LOCATION_NAME + " Humidity(%)", humidity)
    print(" Humidity(%)", humidity)


    # take a timestamp for this measurement
    time = datetime.datetime.utcnow()

    # format the data as a single measurement for influx
    body = [
    {
        "measurement": measurement_name,
        "time": time,
        "fields": {
            "temperature": temperature,
            "humidity": humidity,
            "location": SENSOR_LOCATION_NAME
        }
    }
    ]
    # connect to influx
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

    # write the measurement
    ifclient.write_points(body)
    streamer.flush()
    t.sleep(60*MINUTES_BETWEEN_READS)
