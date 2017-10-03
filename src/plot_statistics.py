import sys
import csv
import statistics
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt
from argparse import ArgumentParser

percentages = list(range(10, 100, 10))

output_variables = ['restarts', 'conflicts', 'decisions', 'conflict_literals',
    'propagations', 'cpu_time', 'clauses', 'variables']

parser = ArgumentParser(description='Draw a plot of a given statistic')
parser.add_argument('filename', type=str, help='Filename of the data source')
parser.add_argument('variable', type=str, help='Variable to put on the y axis')
parser.add_argument('--ylim-min', type=float, help='Lower bound for the y axis')
parser.add_argument('--ylim-max', type=float, help='Upper bound for the y axis')
args = parser.parse_args()

filename = args.filename
plot_name = args.variable
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
        if len(values) > 0:
            calc['mean'] = statistics.mean(values)
            # calc['var'] = statistics.stdev(values)
            aggregate[name][param_setting] = calc

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

plt.figure(figsize=(10, 8))
plt.title("%s" % (plot_name))
plt.xlabel('N')
plt.ylabel(plot_name)
if hasattr(args, 'ylim_min'):
    plt.gca().set_ylim(bottom=args.ylim_min)
if hasattr(args, 'ylim_max'):
    plt.gca().set_ylim(top=args.ylim_max)
smart = True
for M in data_x[smart].keys():
    # if M > 50:
    # print(data_x[smart][M])
    plt.plot(data_x[smart][M], data_y[smart][M], label="%s" % (M,))
plt.legend()
plt.show()
