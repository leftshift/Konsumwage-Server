import datetime
from threading import Lock
from . import db, models, deductions

last_measurement_lock = Lock()

last_measurement = {
    'timestamp': datetime.datetime.now(),
    'weight': 0,
    'total': 0
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
        delta_weight = last_measurement['weight'] - value
        delta_consumtion = calculate_consumtion_delta(delta_weight)
        delta_time = now - last_measurement['timestamp']
        total = deductions.cumulative() + delta_consumtion
        last_measurement['timestamp'] = now
        last_measurement['weight'] = value
        last_measurement['total'] = total
    return {
        'delta_time': delta_time.total_seconds(),
        'delta_consumtion': delta_consumtion,
        'total': total}


def add_measurement(timestamp, weight):
    prev_meas = models.Measurement.query\
        .order_by(models.Measurement.timestamp.desc()).first()
    if prev_meas:
        weight_delta = prev_meas.weight - weight
        consumtion_delta = calculate_consumtion_delta(weight_delta)
    else:
        weight_delta = 0.0
        consumtion_delta = 0.0

    meas = models.Measurement(timestamp, consumtion_delta, weight)
    db.session.add(meas)
    db.session.commit()
    with last_measurement_lock:
        global last_measurement
        last_measurement['timestamp'] = timestamp
        last_measurement['weight'] = weight
