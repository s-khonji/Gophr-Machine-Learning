import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def cyclic_chart(cycle, bins, dt_object=None, *, indicator=None, subplot=111, cmap=plt.cm.Greys, **kwargs):
    """plot a cyclic chart of a datetime object

    Arguments:
        cycle (class Cycle): cycle type properties
        bins (int or list): bins to plot or number of bins requested
        dt_object: datetime object to bin
        indicator: boolean object of the same length as dt_object for colorization
        subplot (int or list, optional): subplot to add

    Returns:
        axis object: axis of the subplot
    """

    # generate theta grid
    angles, labels = cycle.angles, cycle.labels

    # set default parameter
    target_ratio = None

    # bin datetime data if necessary
    if np.isscalar(bins):  # i.e. bins refers to n of bins
        seconds = cycle.seconds(dt_object)
        bin_edges = np.linspace(.0, cycle.duration, bins + 1)
        bins, _ = np.histogram(seconds, bin_edges)

        if indicator is not None:
            # indicator is binary, count only indicated dt entries
            target_count = seconds[indicator == 1]
            # bin the indicated entries
            target_bins, _ = np.histogram(target_count, bin_edges)
            # divide indicated entries by all entries to get the ratio
            target_ratio = np.divide(target_bins, bins, out=np.zeros_like(bins, dtype=float), where=bins != 0)
            # parameters out and where takes care of zeroes in the bins and just returns 0
            # see https://stackoverflow.com/questions/26248654/how-to-return-0-with-divide-by-zero

    scaler = (dt_object.max() - dt_object.min()).total_seconds() / cycle.duration

    ax, cbar = polar_chart(bins/scaler, angles, labels, intensity=target_ratio, subplot=subplot, cmap=cmap, **kwargs)

    return ax, cbar


def polar_chart(bins, angles, labels, *, intensity=None, subplot=111, cmap, **kwargs):
    """plot a polar chart from bins with theta grid labels and positions

    Arguments:
        bins (list of int)
        angles (list of int): position of the thetagrid labels in degrees
        labels (list of str): thetagrid labels
        subplot (int or list, optional): subplot to add
        intensity (list of float, optional): color intensity of every bin, range [0, 1]. must have same length as bins

    Returns:
        axis object: axis of the subplot
    """

    # Based upon the gallery example at matplotlib.org
    # https://matplotlib.org/gallery/pie_and_polar_charts/polar_bar.html

    # Compute pie slices
    n = len(bins)
    bar_max = max(bins)
    theta = np.linspace(0.0, 2 * np.pi, n, endpoint=False)
    radii = bins
    width = 2 * np.pi / n
    if intensity is not None:
        scaler = MinMaxScaler()
        scaler.fit(intensity.reshape(-1, 1))
        norm = plt.Normalize(vmin=scaler.data_min_, vmax=scaler.data_max_)
        colors = cmap(scaler.transform(intensity.reshape(-1, 1)).reshape(-1))
    else:
        norm = None
        colors = cmap(radii / bar_max)

    # default alpha
    alpha = kwargs.pop('alpha', 0.5)

    ax = plt.subplot(subplot, projection='polar')

    # Make theta axis go clockwise
    ax.set_theta_direction(-1)
    # Place 0 at the top
    ax.set_theta_offset(np.pi / 2.0)
    # Set theta labels
    ax.set_thetagrids(angles, labels)

    ax.bar(theta, radii, width=width, bottom=0.0, color=colors, align='edge', alpha=alpha, **kwargs)

    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=norm), ax=ax, alpha=alpha)

    return ax, cbar
