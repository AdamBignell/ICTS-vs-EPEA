class PerformanceTracker(object):
    def __init__(self):
        self.stats = self.create_stats()

    def create_stats(self):
        return dict()

    def get_stats(self):
        return self.stats

    def count(self, statName, func):
        if self.stats_contain_stat(statName):
            self.increment_stat(statName, 1)
        else:
            self.add_stat(statName, 1)

    def stats_contain_stat(self, statName):
        return statName in self.stats

    def increment_stat(self, stat_name, amount_to_increment):
        self.stats[stat_name] = self.stats[stat_name] + amount_to_increment

    def add_stat(self, stat_name, initial_value):
        self.stats[stat_name] = initial_value
