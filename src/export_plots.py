import sys
from collections import defaultdict
from compute_statistics import *
from plot_drawer import draw_plot

ylims_min = defaultdict(lambda: None)
ylims_max = defaultdict(lambda: None)
ylims_max['restarts'] = 5.0
ylims_max['conflicts'] = 5000.0
ylims_max['cpu_time'] = 0.025

output_variables = get_output_variables()
filename = sys.argv[1]
aggregate = aggregate_statistics(filename)
for output_variable in output_variables:
    ylim_min = ylims_min[output_variable]
    ylim_max = ylims_max[output_variable]
    data_x, data_y = compute_plot_data(aggregate, output_variable)
    fig = draw_plot(data_x, data_y, output_variable, ylim_min, ylim_max)
    fig.savefig('doc/plots/%s.png' % (output_variable,))
