import time
import json
import os.path

class PerformanceTracker(object):
    def __init__(self):
        self.stats = self.create_stats()
        self.res_file_name = "no_name"

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
        else:
            self.update_time(statName, elapsed_time)

        return result

    def update_time(self, stat_name, new_time):
        self.stats[stat_name] = self.stats[stat_name] + new_time

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
        print("Performance Tracker Stats:")
        print(json.dumps(self.stats, indent = 4))

    def write_stats_to_file(self, file_name):
        stats_file = ""
        file_name = file_name.replace("*", ".txt")

        if os.path.exists(file_name):
            stats_file = open(file_name, "a")
        else:
            stats_file = open(file_name, "x")

        if stats_file != "":
            json.dump(self.stats, stats_file)

        stats_file.write('\n')
        stats_file.close()

    def set_map_name(self, map_name):
        self.stats["map_name"] = map_name

    def set_results_file_name(self, file_name):
        self.res_file_name = file_name

    def get_results_file_name(self):
        return self.res_file_name
