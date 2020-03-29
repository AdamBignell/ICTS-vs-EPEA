import time

from performance_tracker import PerformanceTracker

def test_tracker_creates_a_stats_entry():
    def simple_print(message):
        print(message)

    tracker = PerformanceTracker()
    tracker.count("printCount", lambda: simple_print("count 0"))
    all_stats = tracker.get_stats()
    number_of_stats = len(all_stats)
    assert number_of_stats is 1, "Cannot create a single stat entry for counting"

def test_tracker_creates_multiple_stats_entry():
    def simple_print(message):
        print(message)

    tracker = PerformanceTracker()
    tracker.count("printCount1", lambda: simple_print("count 1"))
    tracker.count("printCount2", lambda: simple_print("count 2"))
    tracker.count("printCount3", lambda: simple_print("count 3"))
    tracker.count("printCount4", lambda: simple_print("count 4"))
    tracker.count("printCount5", lambda: simple_print("count 5"))
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
    def waiting(time_to_wait):
        time.sleep(time_to_wait)

    tracker = PerformanceTracker()
    tracker.time("wait", lambda: waiting(1))

    all_stats = tracker.get_stats()
    number_of_stats = len(all_stats)
    assert number_of_stats is 1, "Cannot create a single stat entry for timing"

def test_tracker_times_how_long_a_function_takes_to_run():
    def waiting(waiting_time):
        time.sleep(waiting_time)

    time_to_wait = 2
    tracker = PerformanceTracker()
    tracker.time("wait", lambda: waiting(time_to_wait))

    all_stats = tracker.get_stats()
    time_taken = all_stats["wait"]
    threshold = 0.1
    assert (time_taken < (time_to_wait + threshold)) and (time_taken > (time_to_wait - threshold)), "Cannot accurately time function within a certain threshold"

def test_print_stats_for_tracker():
    def waiting(waiting_time):
        time.sleep(waiting_time)

    def empty_func():
        pass

    time_to_wait = 2
    tracker = PerformanceTracker()
    tracker.time("wait", lambda: waiting(time_to_wait))

    for i in range(10):
        tracker.count("empty", lambda: empty_func())
    tracker.print_stats()

def test_tracker_times_multiple_instances_of_same_key():
    def waiting(waiting_time):
        time.sleep(waiting_time)

    time_to_wait = 1
    expected_time = 2
    tracker = PerformanceTracker()

    for i in range(expected_time):
        tracker.time("wait", lambda: waiting(time_to_wait))

    all_stats = tracker.get_stats()
    time_taken = all_stats["wait"]
    threshold = 0.1
    assert (time_taken < (expected_time + threshold)) and (time_taken > (expected_time - threshold)), "Cannot accurately add times of multiple function calls"

if __name__ == "__main__":
    test_tracker_creates_a_stats_entry()
    test_tracker_creates_multiple_stats_entry()
    test_tracker_counts_how_many_times_function_is_called()
    test_tracker_adds_stat_for_time()
    test_tracker_times_how_long_a_function_takes_to_run()
    test_print_stats_for_tracker()
    test_tracker_times_multiple_instances_of_same_key()
    print("ALL TEST PASSED")