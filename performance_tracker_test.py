from performance_tracker import PerformanceTracker

def test_tracker_creates_a_stats_entry():
    def simple_print():
        print("Creating stats entry")

    tracker = PerformanceTracker()
    tracker.count("printCount", simple_print)
    all_stats = tracker.get_stats()
    number_of_stats = len(all_stats)
    assert number_of_stats is 1, "Cannot create a single stat entry for counting"

def test_tracker_counts_how_many_times_function_is_called():
    def empty_func():
        pass

    number_of_times_to_call_function = 5
    tracker = PerformanceTracker()

    for i in range(number_of_times_to_call_function):
        tracker.count("functionCallCount", empty_func)

    all_stats = tracker.get_stats()
    assert all_stats["functionCallCount"] is number_of_times_to_call_function, "Cannot correctly count the number of times a function is called"

if __name__ == "__main__":
    test_tracker_creates_a_stats_entry()
    test_tracker_counts_how_many_times_function_is_called()
    print("ALL TEST PASSED")