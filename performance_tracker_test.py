import time
import os.path

from performance_tracker import PerformanceTracker

file_name_1 = "results/test_file1.txt"
file_name_2 = "results/test_file2.txt"
file_name_3 = "results/test_file3.txt"
algorithm_name = "ICTS"

def test_tracker_creates_a_stats_entry():
    def simple_print(message):
        print(message)

    tracker = PerformanceTracker(algorithm_name)
    tracker.count("printCount", lambda: simple_print("count 0"))
    all_stats = tracker.get_stats()
    number_of_stats = len(all_stats)
    assert number_of_stats == 2, "Cannot create a single stat entry for counting"

def test_tracker_creates_multiple_stats_entry():
    def simple_print(message):
        print(message)

    tracker = PerformanceTracker(algorithm_name)
    tracker.count("printCount1", lambda: simple_print("count 1"))
    tracker.count("printCount2", lambda: simple_print("count 2"))
    tracker.count("printCount3", lambda: simple_print("count 3"))
    tracker.count("printCount4", lambda: simple_print("count 4"))
    tracker.count("printCount5", lambda: simple_print("count 5"))
    all_stats = tracker.get_stats()
    number_of_stats = len(all_stats)
    assert number_of_stats == 6, "Cannot create multiple stats entry for counting"

def test_tracker_counts_how_many_times_function_is_called():
    def empty_func():
        pass

    number_of_times_to_call_function = 5
    tracker = PerformanceTracker(algorithm_name)

    for i in range(number_of_times_to_call_function):
        tracker.count("functionCallCount", empty_func)

    all_stats = tracker.get_stats()
    assert all_stats["functionCallCount"] is number_of_times_to_call_function, "Cannot correctly count the number of times a function is called"


def test_tracker_adds_stat_for_time():
    def waiting(time_to_wait):
        time.sleep(time_to_wait)

    tracker = PerformanceTracker(algorithm_name)
    tracker.time("wait", lambda: waiting(1))

    all_stats = tracker.get_stats()
    number_of_stats = len(all_stats)
    assert number_of_stats == 2, "Cannot create a single stat entry for timing"

def test_tracker_times_how_long_a_function_takes_to_run():
    def waiting(waiting_time):
        time.sleep(waiting_time)

    time_to_wait = 2
    tracker = PerformanceTracker(algorithm_name)
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
    tracker = PerformanceTracker(algorithm_name)
    tracker.time("wait", lambda: waiting(time_to_wait))

    for i in range(10):
        tracker.count("empty", lambda: empty_func())
    tracker.print_stats()

def test_tracker_times_multiple_instances_of_same_key():
    def waiting(waiting_time):
        time.sleep(waiting_time)

    time_to_wait = 1
    expected_time = 2
    tracker = PerformanceTracker(algorithm_name)

    for i in range(expected_time):
        tracker.time("wait", lambda: waiting(time_to_wait))

    all_stats = tracker.get_stats()
    time_taken = all_stats["wait"]
    threshold = 0.1
    assert (time_taken < (expected_time + threshold)) and (time_taken > (expected_time - threshold)), "Cannot accurately add times of multiple function calls"

def test_tracker_can_write_file():
    def empty_func():
        pass

    tracker = PerformanceTracker(algorithm_name)

    for i in range(10):
        tracker.count("empty", lambda: empty_func())

    tracker.write_stats_to_file(file_name_1)
    assert os.path.exists(file_name_1), "Cannot create file for performance tracker"
    os.remove(file_name_1)

def test_tracker_can_write_single_entry_to_file():
    def empty_func():
        pass

    tracker = PerformanceTracker(algorithm_name)
    expected_result = "{\"algorithm\": \"ICTS\", \"empty\": 10, \"map_name\": \"test_map\"}\n"

    for i in range(10):
        tracker.count("empty", lambda: empty_func())

    tracker.set_map_name("test_map")
    tracker.write_stats_to_file(file_name_2)
    stats_file = open(file_name_2, "r")

    file_contents = ""
    if stats_file.mode == "r":
        file_contents = stats_file.read()

    assert file_contents == expected_result, "Cannot write single performance tracker entry to file"
    stats_file.close()
    os.remove(file_name_2)

def test_tracker_can_write_multiple_entries_to_file():
    def empty_func():
        pass

    tracker1 = PerformanceTracker(algorithm_name)
    tracker2 = PerformanceTracker(algorithm_name)
    expected_result = '{"algorithm": "ICTS", "empty": 10, "map_name": "test_map"}\n{"algorithm": "ICTS", "empty": 5, "map_name": "test_2_map"}\n'

    for i in range(10):
        tracker1.count("empty", lambda: empty_func())

    for i in range(5):
        tracker2.count("empty", lambda: empty_func())

    tracker1.set_map_name("test_map")
    tracker2.set_map_name("test_2_map")

    tracker1.write_stats_to_file(file_name_3)
    tracker2.write_stats_to_file(file_name_3)

    stats_file = open(file_name_3, "r")

    file_contents = ""
    if stats_file.mode == "r":
        file_contents = stats_file.read()

    assert file_contents == expected_result, "Cannot write multiple performance tracker entry to file, each entry being on a different line"
    stats_file.close()
    os.remove(file_name_3)

def test_tracker_can_track_the_size_of_list():
    tracker = PerformanceTracker(algorithm_name)

    list_name = "test_list"
    test_list = []
    size_of_list = 5

    tracker.add_list_to_record(list_name, test_list)

    for i in range(size_of_list):
        test_list.append(0)

    tracker.update_all_list_lengths()

    stats = tracker.get_stats()
    list_size = stats[list_name]

    assert list_size == len(test_list), "Cannot correctly record size of list upon call to record the length of the list"

def test_tracker_can_track_the_max_length_of_a_list():
    tracker = PerformanceTracker(algorithm_name)

    list_name = "test_list"
    test_list = []
    size_of_list = 5
    elements_to_remove = 3

    for i in range(size_of_list):
        lambda: test_list.append(0)
        tracker.record_max(list_name, len(test_list))

    for j in range(elements_to_remove):
        test_list.pop()

    stats = tracker.get_stats()
    list_size = stats[list_name]

    assert list_size == size_of_list, "Cannot correctly record size of list at its larger size"

if __name__ == "__main__":
    test_tracker_creates_a_stats_entry()
    test_tracker_creates_multiple_stats_entry()
    test_tracker_counts_how_many_times_function_is_called()
    test_tracker_adds_stat_for_time()
    test_tracker_times_how_long_a_function_takes_to_run()
    test_print_stats_for_tracker()
    test_tracker_times_multiple_instances_of_same_key()
    test_tracker_can_write_file()
    test_tracker_can_write_single_entry_to_file()
    test_tracker_can_write_multiple_entries_to_file()
    test_tracker_can_track_the_size_of_list()
    test_tracker_can_track_the_max_length_of_a_list()
    print("ALL TEST PASSED")
