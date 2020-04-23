import time
import json
import os.path

class PerformanceTracker(object):
    def __init__(self, algorithm_name):
        self.stats = self.create_stats()
        self.stats['algorithm'] = algorithm_name
        self.res_file_name = "no_name"
        self.lists = dict()

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

    def count(self, stat_name, func):
        if self.stats_contain_stat(stat_name):
            self.increment_stat(stat_name, 1)
        else:
            self.add_stat(stat_name, 1)

        return func()

    def record_max(self, stat_name, list_length):
        if self.stats_contain_stat(stat_name):
            self.stats[stat_name] = max(self.stats[stat_name], list_length)
        else:
            self.stats[stat_name] = max(0, list_length)

    def stats_contain_stat(self, stat_name):
        return stat_name in self.stats

    def increment_stat(self, stat_name, amount_to_increment):
        self.stats[stat_name] = self.stats[stat_name] + amount_to_increment

    def add_stat(self, stat_name, initial_value):
        self.stats[stat_name] = initial_value

    def print_stats(self):
        print("Performance Tracker Stats:")
        print(json.dumps(self.stats, indent = 4))

    def write_stats_to_file(self, file_name):
        stats_file = ""

        if '\\' in file_name:
            directories = file_name.split('\\')
            directories[0] = 'results'
            file_name = '\\'.join(directories)
        else:
            directories = file_name.split('/')
            directories[0] = 'results'
            file_name = '/'.join(directories)
        file_name = file_name.replace("*", self.stats['algorithm'] + "_results.txt")

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

    def add_list_to_record(self, list_name, list_reference):
        self.lists[list_name] = list_reference

    def update_all_list_lengths(self):
        for key in self.lists:
            self.add_stat(key, len(self.lists[key]))
