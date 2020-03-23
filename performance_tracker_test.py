import time

from performance_tracker import PerformanceTracker

def test_tracker_creates_a_stats_entry():
    def simple_print():
        print("Creating stats entry")

    tracker = PerformanceTracker()
    tracker.count("printCount", simple_print)
    all_stats = tracker.get_stats()
    number_of_stats = len(all_stats)
    assert number_of_stats is 1, "Cannot create a single stat entry for counting"

def test_tracker_creates_multiple_stats_entry():
    def simple_print():
        print("Creating stats entry")

    tracker = PerformanceTracker()
    tracker.count("printCount1", simple_print)
    tracker.count("printCount2", simple_print)
    tracker.count("printCount3", simple_print)
    tracker.count("printCount4", simple_print)
    tracker.count("printCount5", simple_print)
    all_stats = tracker.get_stats()
    number_of_stats = len(all_stats)
    assert number_of_stats is 5, "Cannot create a single stat entry for counting"

def test_tracker_counts_how_many_times_function_is_called():
    def empty_func():
        pass

    number_of_times_to_call_function = 5
    tracker = PerformanceTracker()

    for i in range(number_of_times_to_call_function):
        tracker.count("functionCallCount", empty_func)

    all_stats = tracker.get_stats()
    assert all_stats["functionCallCount"] is number_of_times_to_call_function, "Cannot correctly count the number of times a function is called"


def test_tracker_adds_stat_for_time():
    def waiting():
        time.sleep(1)

    tracker = PerformanceTracker()
    tracker.time("wait", waiting)

    all_stats = tracker.get_stats()
    number_of_stats = len(all_stats)
    assert number_of_stats is 1, "Cannot create a single stat entry for timing"

def test_tracker_times_how_long_a_function_takes_to_run():
    def waiting():
        time.sleep(2)

    tracker = PerformanceTracker()
    tracker.time("wait", waiting)

    all_stats = tracker.get_stats()
    time_taken = all_stats["wait"]
    threshold = 0.001
    assert (time_taken < (2 + threshold)) and (time_taken > (2 - threshold)), "Cannot accurately time function within a certain threshold"

if __name__ == "__main__":
    test_tracker_creates_a_stats_entry()
    test_tracker_creates_multiple_stats_entry()
    test_tracker_counts_how_many_times_function_is_called()
    test_tracker_adds_stat_for_time()
    test_tracker_times_how_long_a_function_takes_to_run()
    print("ALL TEST PASSED")