import sys
from compute_statistics import *
from plot_drawer import draw_plot

output_variables = get_output_variables()
filename = sys.argv[1]
aggregate = aggregate_statistics(filename)
for output_variable in output_variables:
    data_x, data_y = compute_plot_data(aggregate, output_variable)
    fig = draw_plot(data_x, data_y, output_variable)
    fig.savefig('doc/plots/%s.png' % (output_variable,))
