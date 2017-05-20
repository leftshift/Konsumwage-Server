import serial
import datetime
import requests
ser = serial.Serial("/dev/ttyUSB0", 38400)

endpoint = "http://localhost:5000/api/put"
current_weight = 100


def add_measurement(value, timestamp):
    requests.put(endpoint, json={"value": value, "timestamp": timestamp})
    print({"value": value, "timestamp": timestamp})

while True:
    weight = round(float(ser.readline().strip()), 1)
    add_measurement(weight, datetime.datetime.now().timestamp())
