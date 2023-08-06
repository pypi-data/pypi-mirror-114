import numpy as np
from ..plotting._histogram import _plot_histogram

def _zero_centered_random(size=1, scalar=1, selection="gaussian", plot=False, n_bins=20, color='#9ABD76'):

    """
    By default, gives zero-centered array between -1 and 1 of size=1.
    Size can be any numpy-compatible size. If a scalar is provided,
    the array is multiplied by that scalar.

    Parameters:
    -----------
    size
        any size np array
        e.g.: 1, [1, 2], [100, 2],...

    scalar [optional | default: 1]
        Multiple by which to scale array.
        type: float or list of floats

    selection [optional | default: 'gaussian' | options: 'gaussian', 'random']

        gaussian
            Uses numpy.random.normal to select a gaussian distribution around zero.
            Typically used as np.random.normal(loc=0.0, scale=1.0, size=None)

        random
            Uses numpy.random.random()

    plot [optional | default: False]
    Returns:
    --------
    array
        type: numpy.ndarray
    """

    if selection == "random":
        array = (np.random.random(size) * 2 - 1) * scalar

    elif selection == "gaussian":
        array = np.random.normal(loc=0, scale=scalar, size=size)
    else:
        assert selection in ["random", "gaussian"], print(
            "Please choose a valid selection parameter, i.e., ['gaussian', 'random']"
        )

    if plot:
        try:
            _plot_histogram(array, n_bins, color='#9ABD76')
        except:
            print("WARNING: Histogram is of dimension: {}, plotting currently only supports 1-D arrays".format(array.shape))
    return array