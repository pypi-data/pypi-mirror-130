# -*- coding: utf-8 -*-
"""Helper functions for pybaselines.

Created on March 5, 2021
@author: Donald Erb

"""

from math import ceil

import numpy as np
from scipy.ndimage import grey_opening
from scipy.signal import convolve
from scipy.sparse import diags, identity

from ._compat import _pentapy_solve, jit


# Note: the triple quotes are for including the attributes within the documentation
PENTAPY_SOLVER = 2
"""An integer designating the solver to use if pentapy is installed.
pentapy's solver can be used for solving pentadiagonal linear systems, such
as those used for the Whittaker-smoothing-based algorithms. Should be 2 (default)
or 1. See :func:`pentapy.core.solve` for more details.
"""


def _pentapy_solver(ab, y):
    """
    Convenience function for calling pentapy's solver with defaults already set.

    Solves the linear system :math:`A @ x = y` for `x`, given the matrix `A` in
    banded format, `ab`. The default settings of :func`:pentapy.solve` are
    already set for the fastest configuration.

    Parameters
    ----------
    ab : array-like
        The matrix `A` in row-wise banded format (see :func:`pentapy.solve`).
    y : array-like
        The right hand side of the equation.

    Returns
    -------
    numpy.ndarray
        The solution to the linear system.

    """
    return _pentapy_solve(ab, y, is_flat=True, index_row_wise=True, solver=PENTAPY_SOLVER)


# the minimum positive float values such that a + _MIN_FLOAT != a
# TODO this is mostly used to prevent dividing by 0; is there a better way to do that?
# especially since it is usually max(value, _MIN_FLOAT) and in some cases value could be
# < _MIN_FLOAT but still > 0 and useful; think about it
_MIN_FLOAT = np.finfo(float).eps


class ParameterWarning(UserWarning):
    """
    Warning issued when a parameter value is outside of the recommended range.

    For cases where a parameter value is valid and will not cause errors, but is
    outside of the recommended range of values and as a result may cause issues
    such as numerical instability that would otherwise be hard to diagnose.
    """


def relative_difference(old, new, norm_order=None):
    """
    Calculates the relative difference (norm(new-old) / norm(old)) of two values.

    Used as an exit criteria in many baseline algorithms.

    Parameters
    ----------
    old : numpy.ndarray or float
        The array or single value from the previous iteration.
    new : numpy.ndarray or float
        The array or single value from the current iteration.
    norm_order : int, optional
        The type of norm to calculate. Default is None, which is l2
        norm for arrays, abs for scalars.

    Returns
    -------
    float
        The relative difference between the old and new values.

    """
    numerator = np.linalg.norm(new - old, norm_order)
    denominator = np.maximum(np.linalg.norm(old, norm_order), _MIN_FLOAT)
    return numerator / denominator


def gaussian(x, height=1.0, center=0.0, sigma=1.0):
    """
    Generates a gaussian distribution based on height, center, and sigma.

    Parameters
    ----------
    x : numpy.ndarray
        The x-values at which to evaluate the distribution.
    height : float, optional
        The maximum height of the distribution. Default is 1.0.
    center : float, optional
        The center of the distribution. Default is 0.0.
    sigma : float, optional
        The standard deviation of the distribution. Default is 1.0.

    Returns
    -------
    numpy.ndarray
        The gaussian distribution evaluated with x.

    """
    return height * np.exp(-0.5 * ((x - center)**2) / max(sigma, _MIN_FLOAT)**2)


def gaussian_kernel(window_size, sigma=1.0):
    """
    Creates an area-normalized gaussian kernel for convolution.

    Parameters
    ----------
    window_size : int
        The number of points for the entire kernel.
    sigma : float, optional
        The standard deviation of the gaussian model.

    Returns
    -------
    numpy.ndarray, shape (window_size,)
        The area-normalized gaussian kernel.

    Notes
    -----
    Return gaus/sum(gaus) rather than creating a unit-area gaussian
    since the unit-area gaussian would have an area smaller than 1
    for window_size < ~ 6 * sigma.

    """
    # centers distribution from -half_window to half_window
    window_size = max(1, window_size)
    x = np.arange(window_size) - (window_size - 1) / 2
    gaus = gaussian(x, 1, 0, sigma)
    return gaus / np.sum(gaus)


def _mollifier_kernel(window_size):
    """
    A kernel for smoothing/mollification.

    Parameters
    ----------
    window_size : int
        The number of points for the entire kernel.

    Returns
    -------
    numpy.ndarray, shape (2 * window_size + 1,)
        The area normalized kernel.

    References
    ----------
    Chen, H., et al. An Adaptive and Fully Automated Baseline Correction
    Method for Raman Spectroscopy Based on Morphological Operations and
    Mollifications. Applied Spectroscopy, 2019, 73(3), 284-293.

    """
    x = (np.arange(0, 2 * window_size + 1) - window_size) / window_size
    kernel = np.zeros_like(x)
    # x[1:-1] is same as x[abs(x) < 1]
    kernel[1:-1] = np.exp(-1 / (1 - (x[1:-1])**2))
    return kernel / kernel.sum()


def _get_edges(data, pad_length, mode='extrapolate', extrapolate_window=None, **pad_kwargs):
    """
    Provides the left and right edges for padding data.

    Parameters
    ----------
    data : array-like
        The array of the data.
    pad_length : int
        The number of points to add to the left and right edges.
    mode : str or Callable, optional
        The method for padding. Default is 'extrapolate'. Any method other than
        'extrapolate' will use numpy.pad.
    extrapolate_window : int, optional
        The number of values to use for linear fitting on the left and right
        edges. Default is None, which will set the extrapolate window size equal
        to `pad_length`.
    **pad_kwargs
        Any keyword arguments to pass to numpy.pad, which will be used if `mode`
        is not 'extrapolate'.

    Returns
    -------
    left_edge : numpy.ndarray, shape(pad_length,)
        The array of data for the left padding.
    right_edge : numpy.ndarray, shape(pad_length,)
        The array of data for the right padding.

    Raises
    ------
    ValueError
        Raised if `pad_length` is < 0, or if `extrapolate_window` is <= 0 and
        `mode` is `extrapolate`.

    Notes
    -----
    If mode is 'extrapolate', then the left and right edges will be fit with
    a first order polynomial and then extrapolated. Otherwise, uses :func:`numpy.pad`.

    """
    y = np.asarray(data)
    if pad_length == 0:
        return np.array([]), np.array([])
    elif pad_length < 0:
        raise ValueError('pad length must be greater or equal to 0')

    if isinstance(mode, str):
        mode = mode.lower()
    if mode == 'extrapolate':
        if extrapolate_window is None:
            extrapolate_window = pad_length
        extrapolate_windows = _check_scalar(extrapolate_window, 2, True, dtype=int)[0]

        if np.any(extrapolate_windows <= 0):
            raise ValueError('extrapolate_window must be greater than 0')
        left_edge = np.empty(pad_length)
        right_edge = np.empty(pad_length)
        # use x[pad_length:-pad_length] for fitting to ensure x and y are
        # same shape regardless of extrapolate window value
        x = np.arange(len(y) + 2 * pad_length)
        for i, array in enumerate((left_edge, right_edge)):
            extrapolate_window_i = extrapolate_windows[i]
            if extrapolate_window_i == 1:
                # just use the edges rather than trying to fit a line
                array[:] = y[0] if i == 0 else y[-1]
            elif i == 0:
                poly = np.polynomial.Polynomial.fit(
                    x[pad_length:-pad_length][:extrapolate_window_i],
                    y[:extrapolate_window_i], 1
                )
                array[:] = poly(x[:pad_length])
            else:
                poly = np.polynomial.Polynomial.fit(
                    x[pad_length:-pad_length][-extrapolate_window_i:],
                    y[-extrapolate_window_i:], 1
                )
                array[:] = poly(x[-pad_length:])
    else:
        padded_data = np.pad(y, pad_length, mode, **pad_kwargs)
        left_edge = padded_data[:pad_length]
        right_edge = padded_data[-pad_length:]

    return left_edge, right_edge


def pad_edges(data, pad_length, mode='extrapolate',
              extrapolate_window=None, **pad_kwargs):
    """
    Adds left and right edges to the data.

    Parameters
    ----------
    data : array-like
        The array of the data.
    pad_length : int
        The number of points to add to the left and right edges.
    mode : str or Callable, optional
        The method for padding. Default is 'extrapolate'. Any method other than
        'extrapolate' will use :func:`numpy.pad`.
    extrapolate_window : int, optional
        The number of values to use for linear fitting on the left and right
        edges. Default is None, which will set the extrapolate window size equal
        to `pad_length`.
    **pad_kwargs
        Any keyword arguments to pass to :func:`numpy.pad`, which will be used if `mode`
        is not 'extrapolate'.

    Returns
    -------
    padded_data : numpy.ndarray, shape (N + 2 * half_window,)
        The data with padding on the left and right edges.

    Notes
    -----
    If mode is 'extrapolate', then the left and right edges will be fit with
    a first order polynomial and then extrapolated. Otherwise, uses :func:`numpy.pad`.

    """
    y = np.asarray(data)
    if pad_length == 0:
        return y

    if isinstance(mode, str):
        mode = mode.lower()
    if mode == 'extrapolate':
        left_edge, right_edge = _get_edges(y, pad_length, mode, extrapolate_window)
        padded_data = np.concatenate((left_edge, y, right_edge))
    else:
        padded_data = np.pad(y, pad_length, mode, **pad_kwargs)

    return padded_data


def padded_convolve(data, kernel, mode='reflect', **pad_kwargs):
    """
    Pads data before convolving to reduce edge effects.

    Parameters
    ----------
    data : array-like, shape (N,)
        The data to convolve.
    kernel : array-like, shape (M,)
        The convolution kernel.
    mode : str or Callable, optional
        The method for padding to pass to :func:`.pad_edges`. Default is 'reflect'.
    **pad_kwargs
        Any additional keyword arguments to pass to :func:`.pad_edges`.

    Returns
    -------
    convolution : numpy.ndarray, shape (N,)
        The convolution output.

    """
    # TODO need to revisit this and ensure everything is correct
    # TODO look at using scipy.ndimage.convolve1d instead, or at least
    # comparing the output in tests; that function should have a similar usage
    padding = ceil(min(len(data), len(kernel)) / 2)
    convolution = convolve(
        pad_edges(data, padding, mode, **pad_kwargs), kernel, mode='same'
    )
    return convolution[padding:-padding]


@jit(nopython=True, cache=True)
def _interp_inplace(x, y, y_start, y_end):
    """
    Interpolates values inplace between the two ends of an array.

    Parameters
    ----------
    x : numpy.ndarray
        The x-values for interpolation. All values are assumed to be valid.
    y : numpy.ndarray
        The y-values. The two endpoints, y[0] and y[-1] are assumed to be valid,
        and all values inbetween (ie. y[1:-1]) will be replaced by interpolation.
    y_start : float, optional
        The initial y-value for interpolation.
    y_end : float, optional
        The end y-value for interpolation.

    Returns
    -------
    y : numpy.ndarray
        The input `y` array, with the interpolation performed inplace.

    """
    y[1:-1] = y_start + (x[1:-1] - x[0]) * ((y_end - y_start) / (x[-1] - x[0]))

    return y


def _convert_coef(coef, original_domain):
    """
    Scales the polynomial coefficients back to the original domain of the data.

    For fitting, the x-values are scaled from their original domain, [min(x),
    max(x)], to [-1, 1] in order to improve the numerical stability of fitting.
    This function rescales the retrieved polynomial coefficients for the fit
    x-values back to the original domain.

    Parameters
    ----------
    coef : array-like
        The array of coefficients for the polynomial. Should increase in
        order, for example (c0, c1, c2) from `y = c0 + c1 * x + c2 * x**2`.
    original_domain : array-like, shape (2,)
        The domain, [min(x), max(x)], of the original data used for fitting.

    Returns
    -------
    output_coefs : numpy.ndarray
        The array of coefficients scaled for the original domain.

    """
    zeros_mask = np.equal(coef, 0)
    if zeros_mask.any():
        # coefficients with one or several zeros sometimes get compressed
        # to leave out some of the coefficients, so replace zero with another value
        # and then fill in later
        coef = coef.copy()
        coef[zeros_mask] = _MIN_FLOAT  # could probably fill it with any non-zero value

    fit_polynomial = np.polynomial.Polynomial(coef, domain=original_domain)
    output_coefs = fit_polynomial.convert().coef
    output_coefs[zeros_mask] = 0

    return output_coefs


def difference_matrix(data_size, diff_order=2, diff_format=None):
    """
    Creates an n-order finite-difference matrix.

    Parameters
    ----------
    data_size : int
        The number of data points.
    diff_order : int, optional
        The integer differential order; must be >= 0. Default is 2.
    diff_format : str or None, optional
        The sparse format to use for the difference matrix. Default is None,
        which will use the default specified in :func:`scipy.sparse.diags`.

    Returns
    -------
    diff_matrix : scipy.sparse.base.spmatrix
        The sparse difference matrix.

    Raises
    ------
    ValueError
        Raised if `diff_order` or `data_size` is negative.

    Notes
    -----
    The resulting matrices are sparse versions of::

        import numpy as np
        np.diff(np.eye(data_size), diff_order, axis=0)

    This implementation allows using the differential matrices are they
    are written in various publications, ie. ``D.T @ D``.

    Most baseline algorithms use 2nd order differential matrices when
    doing penalized least squared fitting or Whittaker-smoothing-based fitting.

    """
    if diff_order < 0:
        raise ValueError('the differential order must be >= 0')
    elif data_size < 0:
        raise ValueError('data size must be >= 0')
    elif diff_order > data_size:
        # do not issue warning or exception to maintain parity with np.diff
        diff_order = data_size

    if diff_order == 0:
        # faster to directly create identity matrix
        diff_matrix = identity(data_size, format=diff_format)
    else:
        diagonals = np.zeros(2 * diff_order + 1)
        diagonals[diff_order] = 1
        for _ in range(diff_order):
            diagonals = diagonals[:-1] - diagonals[1:]

        diff_matrix = diags(
            diagonals, np.arange(diff_order + 1),
            shape=(data_size - diff_order, data_size), format=diff_format
        )

    return diff_matrix


def optimize_window(data, increment=1, max_hits=3, window_tol=1e-6,
                    max_half_window=None, min_half_window=None):
    """
    Optimizes the morphological half-window size.

    Parameters
    ----------
    data : array-like, shape (N,)
        The measured data values.
    increment : int, optional
        The step size for iterating half windows. Default is 1.
    max_hits : int, optional
        The number of consecutive half windows that must produce the same
        morphological opening before accepting the half window as the optimum
        value. Default is 3.
    window_tol : float, optional
        The tolerance value for considering two morphological openings as
        equivalent. Default is 1e-6.
    max_half_window : int, optional
        The maximum allowable half-window size. If None (default), will be set
        to (len(data) - 1) / 2.
    min_half_window : int, optional
        The minimum half-window size. If None (default), will be set to 1.

    Returns
    -------
    half_window : int
        The optimized half window size.

    Notes
    -----
    May only provide good results for some morphological algorithms, so use with
    caution.

    References
    ----------
    Perez-Pueyo, R., et al. Morphology-Based Automated Baseline Removal for
    Raman Spectra of Artistic Pigments. Applied Spectroscopy, 2010, 64, 595-600.

    """
    y = np.asarray(data)
    if max_half_window is None:
        max_half_window = (y.shape[0] - 1) // 2
    if min_half_window is None:
        min_half_window = 1

    opening = grey_opening(y, [2 * min_half_window + 1])
    hits = 0
    best_half_window = min_half_window
    for half_window in range(min_half_window + increment, max_half_window, increment):
        new_opening = grey_opening(y, [half_window * 2 + 1])
        if relative_difference(opening, new_opening) < window_tol:
            if hits == 0:
                # keep just the first window that fits tolerance
                best_half_window = half_window - increment
            hits += 1
            if hits >= max_hits:
                half_window = best_half_window
                break
        elif hits:
            hits = 0
        opening = new_opening

    return max(half_window, 1)  # ensure half window is at least 1


def _check_scalar(data, desired_length, fill_scalar=False, **asarray_kwargs):
    """
    Checks if the input is scalar and potentially coerces it to the desired length.

    Only intended for one dimensional data.

    Parameters
    ----------
    data : array-like
        Either a scalar value or an array. Array-like inputs with only 1 item will also
        be considered scalar.
    desired_length : int
        If `data` is an array, `desired_length` is the length the array must have. If `data`
        is a scalar and `fill_scalar` is True, then `desired_length` is the length of the output.
    fill_scalar : bool, optional
        If True and `data` is a scalar, then will output an array with a length of
        `desired_length`. Default is False, which leaves scalar values unchanged.
    **asarray_kwargs : dict
        Additional keyword arguments to pass to :func:`numpy.asarray`.

    Returns
    -------
    output : numpy.ndarray
        The array of values with 0 or 1 dimensions depending on the input parameters.
    is_scalar : bool
        True if the input was a scalar value or had a length of 1; otherwise, is False.

    Raises
    ------
    ValueError
        Raised if `data` is not a scalar and its length is not equal to `desired_length`.

    """
    output = np.asarray(data, **asarray_kwargs)
    ndim = output.ndim
    if not ndim:
        is_scalar = True
    else:
        if ndim > 1:  # coerce to 1d shape
            output = output.reshape(-1)
        len_output = len(output)
        if len_output == 1:
            is_scalar = True
            output = np.asarray(output[0], **asarray_kwargs)
        else:
            is_scalar = False

    if is_scalar and fill_scalar:
        output = np.full(desired_length, output)
    elif not is_scalar and len_output != desired_length:
        raise ValueError(f'desired length was {desired_length} but instead got {len_output}')

    return output, is_scalar


def _inverted_sort(sort_order):
    """
    Finds the indices that invert a sorting.

    Given an array `a`, and the indices that sort the array, `sort_order`, the
    inverted sort is defined such that it gives the original index order of `a`,
    ie. ``a == a[sort_order][inverted_order]``.

    Parameters
    ----------
    sort_order : numpy.ndarray, shape (N,)
        The original index array for sorting.

    Returns
    -------
    inverted_order : numpy.ndarray, shape (N,)
        The array that inverts the sort given by `sort_order`.

    Notes
    -----
    This function is equivalent to doing::

        inverted_order = sort_order.argsort()

    but is faster for large arrays since no additional sorting is performed.

    """
    num_points = len(sort_order)
    inverted_order = np.empty(num_points, dtype=np.intp)
    inverted_order[sort_order] = np.arange(num_points, dtype=np.intp)

    return inverted_order
