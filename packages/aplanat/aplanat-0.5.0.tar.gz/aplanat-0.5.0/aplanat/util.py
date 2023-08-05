"""Utility functions for aiding plotting."""

import logging

from bokeh import palettes
from bokeh.models import Label
from bokeh.plotting import figure
import numpy as np
import pandas as pd
from scipy import stats as sp_stats


def get_named_logger(name):
    """Create a logger with a name.

    :param name: name of logger.
    """
    name = name.ljust(10)[:10]  # so logging is aligned
    logger = logging.getLogger('{}.{}'.format(__package__, name))
    logger.name = name
    return logger


def set_basic_logging(level=logging.INFO):
    """Set basic log formatting.

    :returns: logger instance.
    """
    logging.basicConfig(
        format='[%(asctime)s - %(name)s] %(message)s',
        datefmt='%H:%M:%S', level=level)
    logger = logging.getLogger(__package__)
    logger.setLevel(level)
    return logger


def read_files(summaries):
    """Read a set of files and join to single dataframe."""
    dfs = list()
    if not isinstance(summaries, (list, tuple)):
        summaries = [summaries]
    for fname in sorted(summaries):
        dfs.append(pd.read_csv(fname, sep="\t"))
    return pd.concat(dfs)


class _colors:
    """Some colours that someone thought were nice."""

    cerulean = "#0084A9"
    not_black = "#001A21"
    feldgrau = "#455556"
    dim_gray = "#666666"
    light_cornflower_blue = "#90C5E7"
    dark_gray = "#B5AEA7"
    isabelline = "#F0EFED"
    medium_spring_bud = "#B8E986"
    cinnabar = "#EF4134"
    sandstorm = "#F5CC49"
    fandango = "#A53F96"
    green = "#17BB75"
    verdigris = "#54B8B1"


Colors = _colors()


class Limiter(object):
    """Helper class to determine limits of data."""

    def __init__(self, limits=None):
        """Initialize the limit gathering."""
        if limits is not None:
            self.min, self.max = limits
        else:
            self.min, self.max = +float('inf'), -float('inf')

    def accumulate(self, data):
        """Analyse data to update limits.

        :param data: new data to analyse.

        """
        self.min = min(self.min, min(data))
        self.max = max(self.max, max(data))
        return self

    def fix(self, lower=None, upper=None):
        """Fix limits to new values.

        :param lower: new lower limit.
        :param upper: new upper limit.

        """
        if lower is not None:
            self.min = lower
        if upper is not None:
            self.max = upper
        return self

    def __repr__(self):
        """Return string representation of self."""
        return repr((self.min, self.max))


def pad(data):
    """Attempt to find a sensible plot bounds for a vector."""
    uniq = sorted(np.unique(data))
    pad = 0.5 * min(np.ediff1d(uniq))
    return uniq[0] - pad, uniq[-1] + pad


def kernel_density_estimate(x, step=0.2):
    """Kernel density to approximate distribution.

    :param x: data of which to find mode.
    :param step: discretization of KDE PDF.
    """
    # estimate bandwidth of kde, R's nrd0 rule-of-thumb
    hi = np.std(x, ddof=1)
    q75, q25 = np.percentile(x, [75, 25])
    iqr = q75 - q25
    lo = min(hi, iqr/1.34)
    if not ((lo == hi) or (lo == abs(x[0])) or (lo == 1)):
        lo = 1
    bw = 0.9 * lo * len(x)**-0.2

    # create a KDE
    x_grid = np.arange(min(x), max(x), step)
    kernel = sp_stats.gaussian_kde(x, bw_method=bw)
    pdf = kernel(x_grid)
    return x_grid, pdf


def choose_palette(ncolours):
    """Choose colour palette.

    :param: ncolours: number of colours.
    """
    if ncolours <= 20:
        # Category20 contains dark/light pairs, avoid using these
        pal = palettes.Category20[20]
        palette = pal[0::2] + pal[1::2]
        cols = palette[0:ncolours]
    elif ncolours <= 256:
        cols = palettes.Viridis256[::256//ncolours]
    else:
        raise ValueError(
            "Cannot create colour palette with more than 256 colours.")
    return cols


def emptyPlot(**kwargs):
    """Empty plot for when all else fails.

    :param kwargs: kwargs for bokeh figure.

    :returns: a bokeh plot.
    """
    p = figure(
        plot_width=300,
        plot_height=300,
        **kwargs
    )
    failLabel = Label(x=125, y=125, x_units='screen',
                      y_units='screen',
                      text=str('Failed to plot'),
                      text_font_style='italic',
                      text_align='center')

    p.circle([1, 2], [3, 4], fill_color='white', line_color='white')
    p.add_layout(failLabel)
    return p


def plot_wrapper(func):
    """Test for function and output empty graph if fails.

    :param func:  name of plotting function from aplanat.
    :param args: the arguments provided.
    :param kwargs: other optional key word arguments.

    :returns: plot.

    """
    def wrapper_accepting_arguments(*args, **kwargs):
        """Argument wrapper for decorator."""
        logger = get_named_logger('PlotWrap')
        try:
            p = (func(*args, **kwargs))
            return p
        except Exception as e:

            try:
                p = emptyPlot(**kwargs)
                logger.exception('Plotting user plot failed with: '+str(e))
                return p

            except Exception as f:
                p = emptyPlot()
                logger.exception(
                    'Plotting templated Empty plot failed with: ' + str(f))
                return p

    return wrapper_accepting_arguments
