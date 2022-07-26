#!/usr/bin/python3
import Adafruit_DHT
import datetime
import time as t
from influxdb import InfluxDBClient

# Sendmail -text file - only .py
 
import smtplib, sys
 
from email. mime. text import MIMEText
 
from email. header import Header

# API
import requests

# --------- User Settings ---------
SENSOR_LOCATION_NAME = "Pujd"
BUCKET_NAME = ":partly_sunny: Room Temperatures"
BUCKET_KEY = "dht22sensor"
ACCESS_KEY = "1892"
MINUTES_BETWEEN_READS = 3
METRIC_UNITS = True
# ---------------------------------

# influx configuration - edit these
ifuser = "grafana"
ifpass = "liverpool1892"
ifdb   = "home"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "temperature"

# api requests config
CITY_NAME = "Vechec"
API_KEY = "5eb96e32258e453ea80164526222507"

sensor = 22
gpio = 4

def send_email(value, apiValue):
    frm = 'j5jancik@gmail.com'
 
    to = 'j4jancik@gmail.com'
 
    subj = 'Temperature alert'
 
    msg = 'Sensor measured temperature ' + value + ' celsius, but weather.com has ' + str(apiValue)
    try:
         mime = MIMEText (msg, 'plain', 'utf -8')
         mime ['From'] = frm
         mime ['To'] = to
         mime ['Subject'] = (subj)
         smtp = smtplib. SMTP ("smtp.gmail.com")
         smtp. starttls ()
         smtp. login ("j5jancik@gmail.com", "npusafyghfwdjbwi")
         smtp. sendmail (frm, [to], mime. as_string ())
         smtp. quit ()
 
    except:
        print ("An error occurred while sending the e-mail:",
        sys. exc_info ())


alert = False

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

    response = requests.get('http://api.weatherapi.com/v1/current.json?key='+ API_KEY + '&q=' + CITY_NAME + '&aqi=no')
    print(response.json())
    apiTemp = response.json()['current']['temp_c']
    weatherIcon = response.json()['current']['condition']['icon']

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
            "location": SENSOR_LOCATION_NAME,
            "icon": weatherIcon
        }
    }
    ]
    # connect to influx
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

    # write the measurement
    ifclient.write_points(body)
    if(alert == False and float(temperature) > float(apiTemp)):
        send_email(temperature, apiTemp)
        alert = True

    t.sleep(60*MINUTES_BETWEEN_READS)
