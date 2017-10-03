import matplotlib
import matplotlib.pyplot as plt
from compute_statistics import *

def apply_ylimit(ylim_min=None, ylim_max=None):
    if ylim_min is not None:
        plt.gca().set_ylim(bottom=ylim_min)
    if ylim_max is not None:
        plt.gca().set_ylim(top=ylim_max)

def draw_plot(data_x, data_y, plot_name, ylim_min=None, ylim_max=None, show=False):
    plt.clf()
    plt.close()
    fig = plt.figure(figsize=(10, 8))
    plt.title("%s" % (plot_name))
    plt.ylabel(plot_name)
    for smart in [True, False]:
        subplt = plt.subplot(311 if smart else 312, sharex=None if smart else subplt)
        apply_ylimit(ylim_min, ylim_max)
        plt.xlabel('N (size)')
        plt.ylabel(plot_name)
        for M in sorted(data_x[smart].keys()):
            plt.plot(data_x[smart][M], data_y[smart][M], label="%s" % (M,))
    plt.legend()
    if show:
        plt.show()
    return fig
