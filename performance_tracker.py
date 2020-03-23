import time
import json

class PerformanceTracker(object):
    def __init__(self):
        self.stats = self.create_stats()

    def create_stats(self):
        return dict()

    def get_stats(self):
        return self.stats

    def time(self, statName, func):
        start_time = time.time()
        result = func()
        end_time = time.time()
        elapsed_time = end_time - start_time

        if not self.stats_contain_stat(statName):
            self.add_stat(statName, elapsed_time)

        return result

    def count(self, statName, func):
        if self.stats_contain_stat(statName):
            self.increment_stat(statName, 1)
        else:
            self.add_stat(statName, 1)

        return func()

    def stats_contain_stat(self, statName):
        return statName in self.stats

    def increment_stat(self, stat_name, amount_to_increment):
        self.stats[stat_name] = self.stats[stat_name] + amount_to_increment

    def add_stat(self, stat_name, initial_value):
        self.stats[stat_name] = initial_value

    def print_stats(self):
        print(json.dumps(self.stats, indent = 4))
