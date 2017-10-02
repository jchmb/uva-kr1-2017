import sys
import csv
import statistics
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt

percentages = list(range(10, 100, 10))

output_variables = ['restarts', 'conflicts', 'decisions', 'conflict_literals',
    'propagations', 'cpu_time', 'clauses', 'variables']

filename = sys.argv[1]
plot_name = sys.argv[2]
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

plt.figure(figsize=(10, 8))
plt.title("%s" % (plot_name))
plt.xlabel('N')
plt.ylabel(plot_name)
# plt.ylim(0, 0.01)
smart = True
for M in data_x[smart].keys():
    if M > 50:
        plt.plot(data_x[smart][M], data_y[smart][M], label="%s" % (M,))
plt.legend()
plt.show()
