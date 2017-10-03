import csv
import statistics
from collections import defaultdict

'''
@typedef dict<str, dict<(int, int, bool), dict<str, float>>> Aggregate
'''

'''
Get the relevant output variables.
@return list<string>
'''
def get_output_variables():
    return ['restarts', 'conflicts', 'decisions', 'conflict_literals',
        'propagations', 'cpu_time', 'clauses', 'variables']

'''
Aggregate the statistics from the given CSV file.
@param str filename
@return Aggregate grouped results
'''
def aggregate_statistics(filename):
    percentages = list(range(10, 100, 10))

    output_variables = get_output_variables()

    grouped_results = defaultdict(list)
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            N = int(row['N'])
            M = (float(row['M']) / float(N**3))
            M = min(percentages, key=lambda perc: abs((M - (float(perc) / 100.0))))
            smart = row['smart'] == 'True'
            param_setting = (N, M, smart)
            res = {name: float(row[name]) for name in output_variables if row[name] != ''}
            grouped_results[param_setting].append(res)

    aggregate = {}
    for name in output_variables:
        aggregate[name] = {}
        for param_setting, results in grouped_results.items():
            calc = {}
            values = [res[name] for res in results if name in res]
            if len(values) > 1:
                calc['mean'] = statistics.mean(values)
                calc['var'] = statistics.stdev(values)
                aggregate[name][param_setting] = calc
    return aggregate

'''
Compute the plot data from an aggregate of statistics.
@param Aggregate aggregate
@param str plot_name
'''
def compute_plot_data(aggregate, plot_name):
    data_x = {True: defaultdict(list), False: defaultdict(list)}
    data_y = {True: defaultdict(list), False: defaultdict(list)}
    for param_setting, calc in aggregate[plot_name].items():
        N, M, smart = param_setting
        data_y[smart][M].append(calc['mean'])
        data_x[smart][M].append(N)

    for smart in data_x.keys():
        for M in data_x[smart].keys():
            data = list(zip(data_x[smart][M], data_y[smart][M]))
            data = sorted(data, key=lambda pair: pair[0])
            data_x[smart][M] = [pair[0] for pair in data]
            data_y[smart][M] = [pair[1] for pair in data]
    return (data_x, data_y)
