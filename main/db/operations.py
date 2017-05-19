import datetime
from threading import Lock
from . import db, models

last_measurement_lock = Lock()

last_measurement = {
    'timestamp': datetime.datetime.now(),
    'weight': 0,
    'consumtion': 0,
}


def calculate_consumtion_delta(weight_delta):
    if weight_delta < 0:  # weight was added
        consumtion_delta = 0
    else:
        consumtion_delta = weight_delta * 1  # TODO: Replace with config value
    return consumtion_delta


def calulate_minor_update(value):
    with last_measurement_lock:
        global last_measurement
        now = datetime.datetime.now()
        delta_time = now - last_measurement['timestamp']
        delta_weight = last_measurement['weight'] - value
        delta_consumtion = calculate_consumtion_delta(delta_weight)
        total = last_measurement['consumtion'] + delta_consumtion

        last_measurement['timestamp'] = now
        last_measurement['weight'] = value
        last_measurement['consumtion'] = round(total, 1)
    return {
        'delta_time': delta_time.total_seconds(),
        'delta_consumtion': delta_consumtion,
        'total': total}


def add_measurement(timestamp, weight):
    prev_meas = models.Measurement.query\
        .order_by(models.Measurement.timestamp.desc()).first()
    if prev_meas:
        time_delta = timestamp - prev_meas.timestamp
        weight_delta = prev_meas.weight - weight
        consumtion_delta = calculate_consumtion_delta(weight_delta)
        consumtion = prev_meas.consumtion + consumtion_delta
    else:
        time_delta = datetime.timedelta(0)
        weight_delta = 0.0
        consumtion_delta = 0.0
        consumtion = 0.0

    meas = models.Measurement(timestamp, time_delta, consumtion,
                              consumtion_delta, weight)
    db.session.add(meas)
    db.session.commit()
    with last_measurement_lock:
        global last_measurement
        last_measurement['timestamp'] = timestamp
        last_measurement['weight'] = weight
        last_measurement['consumtion'] = consumtion
