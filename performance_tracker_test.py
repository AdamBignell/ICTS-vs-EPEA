from performance_tracker import PerformanceTracker

def test_tracker_creates_a_stats_entry():
    tracker = PerformanceTracker()
    tracker.count("printCount", print("Creating stats entry"))
    all_stats = tracker.get_stats()
    number_of_stats = len(all_stats)
    assert number_of_stats is 1, "Cannot create a single stat entry for counting"

if __name__ == "__main__":
    test_tracker_creates_a_stats_entry()
    print("ALL TEST PASSED")