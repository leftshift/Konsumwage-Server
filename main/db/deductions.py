# from flask_sqlalchemy import cast
import datetime
import statistics
from . import db, models


def in_range(start_time=datetime.datetime.min, end_time=datetime.datetime.max):
    measurements = db.session.query(models.Measurement).filter(
        models.Measurement.timestamp >= start_time.isoformat(),
        models.Measurement.timestamp <= end_time.isoformat(),
    )
    return measurements


def cumulative(start_time=datetime.datetime.min, end_time=datetime.datetime.max):
    results = in_range(start_time, end_time)
    try:
        data_start = results[0]
        data_end = results[-1]
    except IndexError:
        return 0.0
    return data_end.consumtion - data_start.consumtion


def average(start_time=datetime.datetime.min, end_time=datetime.datetime.max):
    results = in_range(start_time, end_time)\
        .order_by(models.Measurement.timestamp)
    try:
        data_start = results[0]
        data_end = results[-1]
    except IndexError:
        return 0.0

        return statistics.median([r.consumtion_delta for r in results])


def last_minute():
    one_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)
    cumulative(start_time=one_minute_ago, end_time=datetime.datetime.now())


def last_delta():
    m = db.session.query(models.Measurement).\
        order_by(models.Measurement.timestamp.desc()).first()
    return m.consumtion_delta, m.time_delta


def stats():
    cum = cumulative()
    lm = last_minute()
    ld = last_delta()
    avg = average()
    return {"total": cum,
            "last_minute": lm,
            "last_delta": {"consumtion": ld[0], "time": ld[1].total_seconds()},
            "average": avg}
