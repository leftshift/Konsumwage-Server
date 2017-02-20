import datetime
from . import db, models


def add_measurement(timestamp, weight):
    prev_meas = models.Measurement.query\
        .order_by(models.Measurement.timestamp.desc()).first()
    if prev_meas:
        time_delta = timestamp - prev_meas.timestamp
        weight_delta = prev_meas.weight - weight
        if weight_delta < 0:  # weight was added
            consumtion_delta = 0
        else:
            consumtion_delta = weight_delta * 1  # TODO: Replace with config value
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
