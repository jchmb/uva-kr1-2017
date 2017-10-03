from argparse import ArgumentParser
from compute_statistics import aggregate_statistics
import matplotlib.pyplot as plt
import numpy as np


parser = ArgumentParser(description='Draw a plot of a given statistic')
parser.add_argument('filename', type=str, help='Filename of the data source')
args = parser.parse_args()

filename = args.filename
aggregate = aggregate_statistics(filename)
field = 'cpu_time'
missing_value = '5'

a = np.zeros((9, 13))
# a[M][N] = 5
n_pos = 0
for n in range(3, 15):
    m_pos = 0
    for m in range(10, 100, 10):
        print(m_pos)
        print(n_pos)
        print()
        if (n, m, True) in aggregate[field]:
            a[m_pos][n_pos] = aggregate[field][(n, m, True)]['mean']
        else:
            a[m_pos][n_pos] = missing_value
        m_pos += 1
    n_pos += 1
a[8][12] = 10

ax = plt.gca()
plt.xlabel('N')
plt.ylabel('M')


plt.imshow(a, cmap='hot', interpolation='nearest')
plt.show()
