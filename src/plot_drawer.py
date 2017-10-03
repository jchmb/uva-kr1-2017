import matplotlib
import matplotlib.pyplot as plt
from compute_statistics import *

'''
Apply the ylimit, given a min and a max boundary.
@param float|None ylim_min
@param float|None ylim_max
'''
def apply_ylimit(ylim_min=None, ylim_max=None):
    if ylim_min is not None:
        plt.gca().set_ylim(bottom=ylim_min)
    if ylim_max is not None:
        plt.gca().set_ylim(top=ylim_max)

'''
Draw the plot, given x and y points.
@param dict<bool, dict<int, list<float>>> different values for N, indexed by smart and M
@param dict<bool, dict<int, list<float>>> different values for [plot_name], indexed by smart and M
@param str plot_name
@param float|None ylim_min
@param float|None ylim_max
@param bool show
'''
def draw_plot(data_x, data_y, plot_name, ylim_min=None, ylim_max=None, show=False):
    plt.clf()
    plt.close()
    fig = plt.figure(figsize=(10, 8))
    plt.title("%s" % (plot_name))
    plt.legend(ncol=1)
    for smart in [True, False]:
        share = None if smart else subplt
        subplt = plt.subplot(311 if smart else 312,
            sharex=share, sharey=share)
        if smart:
            plt.setp(subplt.get_xticklabels(), visible=False)
        apply_ylimit(ylim_min, ylim_max)
        plt.xlabel('N (size)')
        plt.ylabel(plot_name)
        for M in sorted(data_x[smart].keys()):
            plt.plot(data_x[smart][M], data_y[smart][M], label="M=%s%%" % (M,))
    plt.legend(ncol=1, bbox_to_anchor=(1,1))
    if show:
        plt.show()
    return fig
