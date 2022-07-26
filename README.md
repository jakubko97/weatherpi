# WeatherPi
## Monitoring temperature and humidity with Raspberry Pi

- Sensor DHT22
- Raspberry Pi 3 Model B
- Python3
- Grafana and InfluxDB

## Requirements to run code
The first thing we should do before installing packages is making sure that all the currently installed packages are up to date.
```
sudo apt update
sudo apt upgrade
```
Next install packages for support sensor DHT22
```
sudo apt-get install python3-pip
sudo python3 -m pip install --upgrade pip setuptools wheel
sudo pip3 install Adafruit_DHT
```

### Install influxDB

Add the InfluxDB repository key to our Raspberry Pi
```
curl https://repos.influxdata.com/influxdb.key | gpg --dearmor | sudo tee /usr/share/keyrings/influxdb-archive-keyring.gpg >/dev/null
```

Add the InfluxDB repository to the sources list (Raspbian / Raspberry Pi OS)
```
echo "deb [signed-by=/usr/share/keyrings/influxdb-archive-keyring.gpg] https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
```

Update the package list again.
```
sudo apt update

```

To install InfluxDB to our Raspberry Pi, all we need to do is run the command below.
```
sudo apt install influxdb

```


Run the following two commands to enable InfluxDB to start at boot on your Raspberry Pi.
```
sudo systemctl unmask influxdb
sudo systemctl enable influxdb
```

And now start up the InfluxDB server.
```
sudo systemctl start influxdb
```

We should now be able to run the influx client with influx and create a user for later (here I use a single admin user grafana for simplicity):

```
create database home
use home

create user grafana with password '<passwordhere>' with all privileges
grant all privileges on home to grafana

show users

user admin
---- -----
grafana true
```

### Install Grafana

Add the APT key used to authenticate packages:

```
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
```
Add the Grafana APT repository:

```
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
```

Install Grafana:

```
sudo apt-get update
sudo apt-get install -y grafana
```


Enable the Grafana server:

```
sudo /bin/systemctl enable grafana-server
```

Start the Grafana server:


```
sudo /bin/systemctl start grafana-server
```

Open a browser and go to http://localhost:3000
Log in to Grafana with the default username admin, and the default password admin.

Next add Influx as a Grafana data source

![adddatasource](https://user-images.githubusercontent.com/45421791/180199017-589021c2-5884-4f4a-8de0-bd08ab5696d9.png)

We then need to add the database, user and password that we set.

![influxdbdetatil](https://user-images.githubusercontent.com/45421791/180199162-2a5b1591-5de8-4406-b062-5111db2f5621.png)

For visualization we need to create new dashboard where we can set custom select query for our table. Beside the query we can select the date range or visualization type (we use Time Series for our measurement). Our visualization looks like this.

![grafana](https://user-images.githubusercontent.com/45421791/180198262-1adfb8f8-a4a9-4177-ac01-da083de61ef1.png)

We have temerature, humidity and location as our parameters. Our select query looks like this. 

![selectQuery](https://user-images.githubusercontent.com/45421791/180200801-e3c70473-4221-4483-8f25-510b011c42fc.png)

Just as simple as it looks! Good look and have a nice day!

## References

https://fahadahammed.com/raspberrypi-with-dht22-sensor-for-humidity-and-temperature-data-with-influxdb/

https://medium.com/initial-state/how-to-build-a-raspberry-pi-temperature-monitor-8c2f70acaea9

https://simonhearne.com/2020/pi-metrics-influx/

https://simonhearne.com/2020/pi-influx-grafana/

https://grafana.com/tutorials/install-grafana-on-raspberry-pi/
