import random
import time
import datetime
import threading

from ..api import operations


class RandomWeightGenerator(threading.Thread):
    """docstring for RandomWeightGenerator."""
    def __init__(self, app_context, start_value):
        super(RandomWeightGenerator, self).__init__()
        self.app_context = app_context
        self.current_weight = start_value

    def run(self):
        while True:
            r = random.randint(4, 10)
            while r > 0:
                time.sleep(1)
                with self.app_context:
                    operations.add_measurement(datetime.datetime.now(),
                                               self.current_weight)
                r -= 1
            self.current_weight -= random.randint(1, 2)
            if self.current_weight <= 0:
                self.current_weight = random.randint(100, 150)


def start_generating(app_context):
    RandomWeightGenerator(app_context, 100).start()
