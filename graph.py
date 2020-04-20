import matplotlib.pyplot as plt
import statistics
import seaborn as sbn

# Boiler plate defaults for matplotlib
plt.style.use('ggplot')
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 12

colors = sbn.color_palette("husl")

def save_graphs():

    # Generate Maze Graphs
    epea_batch_names = get_file_names('EPEA', 'maze')
    icts_batch_names = get_file_names('ICTS', 'maze')
    epea_results = get_all_results(epea_batch_names)
    icts_results = get_all_results(icts_batch_names)

    maze_labels = get_maze_labels('EPEA')
    save_runtime_graph(epea_results, icts_results, maze_labels)

def get_file_names(algorithm, prefix):
    batch_prefix_names = [prefix + '12x12', prefix + '25x25', prefix + '50x50', prefix + '100x100']
    batch_names = [batch + '_3_' + algorithm + '_results.txt' for batch in batch_prefix_names]
    return batch_names

def get_all_results(filenames):
    results = []
    for file in filenames:
        results.append(get_results(file))
    return results

def get_results(filename):
    results = []
    with open('results/' + filename, mode='r') as file:
        lines = file.readlines()
        while len(results) < 100:
            line = lines.pop()
            new_result = {}
            line = ''.join([char for char in line if char not in '{"}'])
            stats = line.split(',')
            for stat in stats:
                key_val = stat.split(':')
                key, val = key_val[0].strip().strip('"'), key_val[1].strip()
                try:
                    new_result[key] = float(val)
                except ValueError:
                    new_result[key] = val
            if new_result['time'] >= 0:
                results.append(new_result)
    return results

def save_runtime_graph(epea_results, icts_results, labels):
    epea_median_times = get_median_times(epea_results)
    icts_median_times = get_median_times(icts_results)
    save_beautiful_graph_medians(epea_median_times, icts_median_times, labels)

    # Lol don't use the below, the stddevs are HUGE
    #epea_means, epea_stddevs = get_means_and_stddevs(epea_results)
    #icts_means, icts_stddevs = get_means_and_stddevs(icts_results)
    #save_beautiful_graph_means(epea_means, epea_stddevs, icts_means, icts_stddevs, labels)


def get_median_times(results):
    result_times = results_to_times(results)
    medians = []
    for times in result_times:
        medians.append(statistics.median(times))
    return medians

def get_means_and_stddevs(results):
    result_times = results_to_times(results)
    means = []
    stddevs = []
    for times in result_times:
        means.append(statistics.mean(times))
        stddevs.append(statistics.stdev(times))
    return means, stddevs

def get_maze_labels(algorithm):
    labels = {}
    labels['x_title'] = 'Maze Size'
    labels['x_labels'] = ['12x12', '25x25', '50x50', '100x100']
    labels['y_title'] = 'Runtime in Seconds'
    labels['title'] = 'Median ' + algorithm + ' runtimes for increasingly large\nMaze Instances, using 3 agents'
    labels['legend'] = ['EPEA*', 'ICTS']
    return labels

def save_beautiful_graph_medians(epea_medians, icts_medians, labels):
    fig, ax = plt.subplots(1, 1)
    plt.plot(epea_medians)
    if icts_medians != []:
        plt.plot(icts_medians)
    ticks = list(range(len(epea_medians)))
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels['x_labels'], minor=False)

    plt.xlabel(labels['x_title'])
    plt.ylabel(labels['y_title'])
    plt.title(labels['title'])
    ax.legend(labels['legend'], facecolor='white')
    
    plt.show()

def save_beautiful_graph_means(epea_means, epea_stddevs, icts_means, icts_stddevs, labels):
    fig, ax = plt.subplots(1, 1)
    plt.plot(epea_means, c=colors[0])
    plt.plot(icts_means, c=colors[1])
    ticks = list(range(len(epea_means)))
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels['x_labels'], minor=False)

    # Fill
    for i in range(len(epea_stddevs)):
        epea_mean, epea_stddev = epea_means[i], epea_stddevs[i]
        icts_mean, icts_stddev = icts_means[i], icts_stddevs[i]
        ax.fill_between(ticks, epea_mean + epea_stddev, epea_mean - epea_stddev, alpha=0.25, facecolor=colors[0])
        ax.fill_between(ticks, icts_mean + icts_stddev, icts_mean - icts_stddev, alpha=0.25, facecolor=colors[1])


    plt.xlabel(labels['x_title'])
    plt.ylabel(labels['y_title'])
    plt.title(labels['title'])
    
    plt.show()

def results_to_times(results):
    sizes = ['12x12', '25x25', '50x50', '100x100']
    results_by_size = []
    algorithm = results[0][0]['algorithm']
    setup_time = 'heuristic_time'
    if algorithm == 'EPEA':
        setup_time = 'osf time'
    for i, size in enumerate(sizes):
        these_results = results[i]
        times = []
        for result in these_results:
            this_time = result['time'] + result[setup_time]
            times.append(this_time)
        results_by_size.append(times)
    return results_by_size


if __name__ == '__main__':
    save_graphs()
