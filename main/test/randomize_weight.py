import random
import threading

from api import operations


class RandomWeightGenerator(threading.Thread):
    """docstring for RandomWeightGenerator."""
    def __init__(self, start_value):
        super(RandomWeightGenerator, self).__init__()
        self.current_weight = start_value

    def run():
