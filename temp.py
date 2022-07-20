#!/usr/bin/python3
import Adafruit_DHT
import datetime
import time as t
from influxdb import InfluxDBClient

# --------- User Settings ---------
SENSOR_LOCATION_NAME = "In backyard"
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

    print("Temperature(C)", temperature)

    print("Humidity(%)", humidity)


    # take a timestamp for this measurement
    time = datetime.datetime.utcnow()

    # format the data as a single measurement for influx
    body = [
    {
        "measurement": measurement_name,
        "time": time,
        "fields": {
            "temperature": float(temperature),
            "humidity": float(humidity),
            "location": SENSOR_LOCATION_NAME
        }
    }
    ]
    # connect to influx
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

    # write the measurement
    ifclient.write_points(body)
    t.sleep(60*MINUTES_BETWEEN_READS)
