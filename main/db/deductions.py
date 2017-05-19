# from flask_sqlalchemy import cast
import datetime
import statistics
import functools
from . import db, models


def in_range(start_time=datetime.datetime.min, end_time=datetime.datetime.max):
    measurements = db.session.query(models.Measurement).filter(
        models.Measurement.timestamp >= start_time.isoformat(),
        models.Measurement.timestamp <= end_time.isoformat(),
    )
    return measurements

def reduce_measurements(total, add):
    if not isinstance(total, float):
        total = 0
    v = add.consumtion_delta
    if v>0:
        return total+v
    else:
        return total

def cumulative(start_time=datetime.datetime.min, end_time=datetime.datetime.max):
    results = in_range(start_time, end_time).all()
    if len(results) < 2:
        return 0.0
    consumtion = functools.reduce(reduce_measurements, results)
    return consumtion


def average(start_time=datetime.datetime.min, end_time=datetime.datetime.max):
    results = in_range(start_time, end_time)\
        .order_by(models.Measurement.timestamp)
    try:
        data_start = results[0]
        data_end = results[-1]
    except IndexError:
        return 0.0

    return statistics.mean([r.consumtion_delta for r in results])


# def last_minute():
#     one_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)
#     cumulative(start_time=one_minute_ago, end_time=datetime.datetime.now())


def last_delta():
    m = db.session.query(models.Measurement).\
        order_by(models.Measurement.timestamp.desc()).all()
    return m[-1].consumtion_delta, m[-1].timestamp - m[-2].timestamp


def stats():
    cum = cumulative()
    ld = last_delta()
    avg = average()
    return {"total": cum,
            # Gives you liters/second
            "last_delta": {"consumtion": ld[0], "time": ld[1].total_seconds()},
            "average": avg}
