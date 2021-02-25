import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.ensemble import RandomForestClassifier

from sklearn.base import clone
from sklearn.metrics import r2_score
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder
from scipy import stats
from pandas.api.types import is_numeric_dtype
from matplotlib.colors import ListedColormap
from matplotlib.ticker import FormatStrFormatter
from copy import copy
import warnings
import tempfile
from os import getpid, makedirs

from rfpimp import myround
from rfpimp import PimpViz

GREY = '#444443'

def plot_corr_heatmap(df,
                      color_threshold=0.6,
                      cmap=None,
                      figsize=None,
                      value_fontsize=8,
                      label_fontsize=9,
                      precision=2,
                      xrot=80,
                      method="spearman"):
    """
    Display the feature spearman's correlation matrix as a heatmap with
    any abs(value)>color_threshold appearing with background color.
    Spearman's correlation is the same thing as converting two variables
    to rank values and then running a standard Pearson's correlation
    on those ranked variables. Spearman's is nonparametric and does not
    assume a linear relationship between the variables; it looks for
    monotonic relationships.
    SAMPLE CODE
    from rfpimp import plot_corr_heatmap
    viz = plot_corr_heatmap(df_train, save='/tmp/corrheatmap.svg',
                      figsize=(7,5), label_fontsize=13, value_fontsize=11)
    viz.view() # or just viz in notebook
    """
    corr = stats.spearmanr(df).correlation #fixed spearmann coefficient
    if len(corr.shape) == 0:
        corr = np.array([[1.0, corr],
                         [corr, 1.0]])

    filtered = copy(corr)
    filtered = np.abs(filtered)  # work with abs but display negatives later
    mask = np.ones_like(corr)
    filtered[np.tril_indices_from(mask)] = -9999

    if cmap is None:
        cw = plt.get_cmap('coolwarm')
        cmap = ListedColormap([cw(x) for x in np.arange(color_threshold, .85, 0.01)])
    elif isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    cm = copy(cmap)
    cm.set_under(color='white')

    if figsize:
        plt.figure(figsize=figsize)
    im = plt.imshow(filtered, cmap=cm, vmin=color_threshold, vmax=1, aspect='equal')

    width, height = filtered.shape
    for x in range(width):
        for y in range(height):
            if x == y:
                plt.annotate('x', xy=(y, x),
                             horizontalalignment='center',
                             verticalalignment='center',
                             fontsize=value_fontsize, color=GREY)
            if x < y:
                plt.annotate(myround(corr[x, y], precision), xy=(y, x),
                             horizontalalignment='center',
                             verticalalignment='center',
                             fontsize=value_fontsize, color=GREY)

    cb = plt.colorbar(im, fraction=0.046, pad=0.04, ticks=[color_threshold, color_threshold + (1 - color_threshold) / 2, 1.0])
    cb.ax.tick_params(labelsize=label_fontsize, labelcolor=GREY, )
    cb.outline.set_edgecolor('white')
    plt.xticks(range(width), df.columns, rotation=xrot, horizontalalignment='right',
               fontsize=label_fontsize, color=GREY)
    plt.yticks(range(width), df.columns, verticalalignment='center',
               fontsize=label_fontsize, color=GREY)

    ax = plt.gca()
    ax.spines['top'].set_linewidth(.3)
    ax.spines['right'].set_linewidth(.3)
    ax.spines['left'].set_linewidth(.3)
    ax.spines['bottom'].set_linewidth(.3)

    plt.tight_layout()
    return PimpViz()