import random
import requests
import time
import datetime

endpoint = "http://localhost:5000/api/put"
current_weight = 100


def add_measurement(value, timestamp):
    requests.put(endpoint, json={"value": value, "timestamp": timestamp})


def generate():
    global current_weight
    while True:
        r = random.randint(4, 10)
        while r > 0:
            time.sleep(2)
            add_measurement(current_weight, datetime.datetime.now().timestamp())
            r -= 1
        current_weight -= random.randint(1, 2)
        if current_weight <= 0:
            current_weight = random.randint(100, 150)

if __name__ == '__main__':
    generate()
