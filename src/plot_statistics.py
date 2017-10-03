import sys
import csv
import statistics
from collections import defaultdict
from argparse import ArgumentParser
from compute_statistics import *
from plot_drawer import draw_plot

parser = ArgumentParser(description='Draw a plot of a given statistic')
parser.add_argument('filename', type=str, help='Filename of the data source')
parser.add_argument('variable', type=str, help='Variable to put on the y axis')
parser.add_argument('--ylim-min', type=float, help='Lower bound for the y axis')
parser.add_argument('--ylim-max', type=float, help='Upper bound for the y axis')
args = parser.parse_args()

filename = args.filename
plot_name = args.variable

aggregate = aggregate_statistics(filename)
data_x, data_y = compute_plot_data(aggregate, plot_name)
ylim_min = args.ylim_min if hasattr(args, 'ylim_min') else None
ylim_max = args.ylim_max if hasattr(args, 'ylim_max') else None
draw_plot(data_x, data_y, plot_name, ylim_min, ylim_max, True)
# fig.savefig('doc/plots/%s.png' % (plot_name,))
