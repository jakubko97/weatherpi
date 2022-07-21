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
sudo apt-get install -y grafana```
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

## References

https://fahadahammed.com/raspberrypi-with-dht22-sensor-for-humidity-and-temperature-data-with-influxdb/

https://medium.com/initial-state/how-to-build-a-raspberry-pi-temperature-monitor-8c2f70acaea9

https://simonhearne.com/2020/pi-metrics-influx/

https://grafana.com/tutorials/install-grafana-on-raspberry-pi/
