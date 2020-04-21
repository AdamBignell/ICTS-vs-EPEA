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

    maze_runtime_labels = get_runtime_labels('Maze')
    save_runtime_graph(epea_results, icts_results, maze_runtime_labels, 'maze_runtime_medians.pdf')

    maze_expansion_epea_labels = get_node_expansion_labels('EPEA*', 'Maze')
    save_expansion_graph(epea_results, maze_expansion_epea_labels, 'maze_epea_expansions.pdf', 'EPEA')

    maze_expansion_icts_labels = get_node_expansion_labels('ICTS', 'Maze')
    save_expansion_graph(icts_results, maze_expansion_icts_labels, 'maze_icts_expansions.pdf', 'ICTS')

    maze_ratio_labels = get_ratio_labels('Maze')
    save_ratio_graph(epea_results, icts_results, maze_ratio_labels, 'maze_ratio_means.pdf')

    # Generate Open Graphs
    epea_open_batch_names = get_file_names('EPEA', 'open')
    icts_open_batch_names = get_file_names('ICTS', 'open')
    epea_open_results = get_all_results(epea_open_batch_names)
    icts_open_results = get_all_results(icts_open_batch_names)
    open_runtime_labels = get_runtime_labels('Open')
    save_runtime_graph(epea_open_results, icts_open_results, open_runtime_labels, 'open_runtime_medians.pdf')

    open_expansion_epea_labels = get_node_expansion_labels('EPEA*', 'Open')
    save_expansion_graph(epea_open_results, open_expansion_epea_labels, 'open_epea_expansions.pdf', 'EPEA')

    open_expansion_icts_labels = get_node_expansion_labels('ICTS', 'Open')
    save_expansion_graph(icts_open_results, open_expansion_icts_labels, 'open_icts_expansions.pdf', 'ICTS')

    open_ratio_labels = get_ratio_labels('Open')
    save_ratio_graph(epea_open_results, icts_open_results, open_ratio_labels, 'open_ratio_means.pdf')

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

def save_runtime_graph(epea_results, icts_results, labels, output_file):
    epea_median_times = get_medians(epea_results, 'time')
    icts_median_times = get_medians(icts_results, 'time')
    save_beautiful_graph_medians(epea_median_times, icts_median_times, labels, output_file)

def save_runtime_graph_means(epea_results, icts_results, labels, output_file):
    epea_means, epea_stddevs = get_means_and_stddevs(epea_results, 'time')
    icts_means, icts_stddevs = get_means_and_stddevs(icts_results, 'time')
    save_beautiful_graph_means(epea_means, epea_stddevs, icts_means, icts_stddevs, labels, output_file)

def save_expansion_graph(results, labels, output_file, algorithm):
    median_expansions = get_medians(results, 'expansions')
    save_beautiful_graph_medians(median_expansions, [], labels, output_file, algorithm=algorithm)

def save_ratio_graph(epea_results, icts_results, labels, output_file):
    epea_means, epea_stddevs = get_means_and_stddevs(epea_results, 'ratio')
    icts_means, icts_stddevs = get_means_and_stddevs(icts_results, 'ratio')
    save_beautiful_graph_means(epea_means, epea_stddevs, icts_means, icts_stddevs, labels, output_file)

def get_medians(results, stat):
    result_nums = results_to_nums(results, stat)
    medians = []
    for nums in result_nums:
        medians.append(statistics.median(nums))
    return medians

def get_means_and_stddevs(results, stat):
    result_nums = []
    if stat == 'ratio':
        result_nums = results_to_ratios(results)
    elif stat == 'time':
        result_nums = results_to_nums(results, stat)
    means = []
    stddevs = []
    for nums in result_nums:
        means.append(statistics.mean(nums))
        stddevs.append(statistics.stdev(nums))
    return means, stddevs

def get_runtime_labels(instance_type):
    labels = {}
    labels['x_title'] = instance_type + ' Instance Size'
    labels['x_labels'] = ['12x12', '25x25', '50x50', '100x100']
    labels['y_title'] = 'Median Runtime in Seconds'
    labels['title'] = 'Comparison of Median ICTS and EPEA*\nruntimes for increasingly large\n' + instance_type + ' Instances, using 3 agents'
    labels['colors'] = colors
    labels['legend'] = ['EPEA*', 'ICTS']
    return labels

def get_node_expansion_labels(algorithm, instance_type):
    labels = {}
    labels['x_title'] = instance_type + ' Instance Size'
    labels['x_labels'] = ['12x12', '25x25', '50x50', '100x100']
    if algorithm == 'ICTS':
        labels['y_title'] = 'Median Number of\nHigh Level Node Expansions'
        labels['colors'] = [colors[4]]
    elif algorithm == 'EPEA*':
        labels['y_title'] = 'Median Number of Node Expansions'
        labels['colors'] = [colors[0]]
    labels['title'] = 'Median ' + algorithm + ' Node Expansions for increasingly large\n' + instance_type + ' Instances, using 3 agents'
    labels['legend'] = [algorithm]
    return labels

def get_ratio_labels(instance_type):
    labels = {}
    labels['x_title'] = instance_type + ' Instance Size'
    labels['x_labels'] = ['12x12', '25x25', '50x50', '100x100']
    labels['y_title'] = 'Mean Ratio of Pre-Processing Time to Total Time'
    labels['colors'] = colors
    labels['title'] = 'Mean Pre-Processing Time to Total Time Ratio\n for ICTS and EPEA* for increasingly large\n' + instance_type + ' Instances, using 3 agents'
    labels['legend'] = ['EPEA*', 'ICTS']
    return labels

def save_beautiful_graph_medians(first_medians, second_medians, labels, filename, algorithm=None):
    fig, ax = plt.subplots(1, 1)
    plt.plot(first_medians, c=labels['colors'][0])
    if second_medians != []:
        plt.plot(second_medians, c=labels['colors'][4])
        ax.set_ylim([-0.2, 3.5])
    elif algorithm == 'ICTS':
        ax.set_ylim([-0.5, 11])
    elif algorithm == 'EPEA':
        ax.set_ylim([-0.5, 370])
    ticks = list(range(len(first_medians)))
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels['x_labels'], minor=False)

    plt.xlabel(labels['x_title'])
    plt.ylabel(labels['y_title'])
    plt.title(labels['title'])
    ax.legend(labels['legend'], facecolor='white', loc='upper left')
    plt.savefig(filename, bbox_inches='tight')

def save_beautiful_graph_means(first_means, first_stddevs, second_means, second_stddevs, labels, filename, algorithm=None):
    fig, ax = plt.subplots(1, 1)
    plt.plot(first_means, c=colors[0])
    if second_means != []:
        plt.plot(second_means, c=labels['colors'][4])
        ax.set_ylim([-0.1, 1.0])
    elif algorithm == 'ICTS':
        ax.set_ylim([-0.5, 11])
    elif algorithm == 'EPEA':
        ax.set_ylim([-0.5, 370])
    ticks = list(range(len(first_means)))
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels['x_labels'], minor=False)

    # Fill
    first_plus = []
    first_minus = []
    second_plus = []
    second_minus = []
    for i in range(len(first_stddevs)):
        first_plus.append(first_means[i] + first_stddevs[i])
        first_minus.append(first_means[i] - first_stddevs[i])
        second_plus.append(second_means[i]+ second_stddevs[i])
        second_minus.append(second_means[i] - second_stddevs[i])
    
    ax.fill_between(ticks, first_plus, first_minus, alpha=0.25, facecolor=colors[0])
    ax.fill_between(ticks, second_plus, second_minus, alpha=0.25, facecolor=colors[4])
    plt.xlabel(labels['x_title'])
    plt.ylabel(labels['y_title'])
    plt.title(labels['title'])
    ax.legend(labels['legend'], facecolor='white', loc='upper left')
    plt.savefig(filename, bbox_inches='tight')

def results_to_ratios(results):
    sizes = ['12x12', '25x25', '50x50', '100x100']
    algorithm = results[0][0]['algorithm']
    results_by_size = []
    setup_time = 'heuristic_time'
    if algorithm == 'EPEA':
        setup_time = 'osf time'
    for i, size in enumerate(sizes):
        these_results = results[i]
        nums = []
        for result in these_results:
            ratio = result[setup_time]/(result['time']+result[setup_time])
            nums.append(ratio)
        results_by_size.append(nums)
    return results_by_size
        
def results_to_nums(results, stat):
    sizes = ['12x12', '25x25', '50x50', '100x100']
    results_by_size = []
    algorithm = results[0][0]['algorithm']
    setup_time = 'heuristic_time'
    if algorithm == 'EPEA':
        setup_time = 'osf time'
    for i, size in enumerate(sizes):
        these_results = results[i]
        nums = []
        for result in these_results:
            if stat == 'time':
                this_time = result['time'] + result[setup_time]
                nums.append(this_time)
            elif stat == 'expansions':
                if "expanded nodes" not in result:
                    nums.append(0)
                else:
                    nums.append(result['expanded nodes'])
        results_by_size.append(nums)
    return results_by_size


if __name__ == '__main__':
    save_graphs()
