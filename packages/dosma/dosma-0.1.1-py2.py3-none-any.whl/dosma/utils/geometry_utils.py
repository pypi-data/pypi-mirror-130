import numpy as np
import scipy.ndimage as sni
from scipy import optimize

from dosma.core.device import get_array_module
from dosma.utils import env

__all__ = ["circle_fit", "cart2pol"]


def circle_fit(x: np.ndarray, y: np.ndarray):
    """Fit a circle given (x, y) scatter points in a plane.

    Args:
      x (np.ndarray): x-coordinates of scatter points.
      y (np.ndarray): y-coordinates of scatter points.

    Returns:
        tuple[float]: Coordinates and radius of circle (center x, center y, radius).
    """
    ###
    # this function fit a circle given (x,y) scatter points in a plane.
    #
    # INPUT:
    #
    #   x................numpy array (n,) where n is the length of the array
    #   y................numpy array (n,) where n is the length of the array
    #
    # OUTPUT:
    #
    #   xc_2.............scalar, it is the coordinate x of the fitted circle
    #   yc_2.............scalar, it is the coordinate y of the fitted circle
    #   R_2..............scalar, it is the radius of the fitted circle
    ###

    # initialize the coordinate for the fitting procedure
    x_m = np.mean(x)
    y_m = np.mean(y)

    def calc_R(xc, yc):
        """
        Calculate the distance of each 2D points from the center (xc, yc).

        Args:
            xc: Center x.
            yc: Center y.
        """
        return np.sqrt((x - xc) ** 2 + (y - yc) ** 2)

    def f_2(c):
        """
        Calculate the algebraic distance between the 2D points
        and the mean circle centered at :math:`c=(xc, yc)`.

        Args:
            c (float): Circle center.
        """
        Ri = calc_R(*c)
        return Ri - Ri.mean()

    center_estimate = x_m, y_m
    center_2, ier = optimize.leastsq(f_2, center_estimate)

    xc_2, yc_2 = center_2
    Ri_2 = calc_R(xc_2, yc_2)
    R_2 = Ri_2.mean()
    # residu_2   = sum((Ri_2 - R_2)**2)
    # residu2_2  = sum((Ri_2**2-R_2**2)**2)

    return xc_2, yc_2, R_2


def cart2pol(x, y):
    """Convert cartesian coordinates to polar coordinates.

    Args:
        x: x-coordinate.
        y: y-coordinate.

    Returns:
        tuple[float, float]: radius (rho) and angle (phi).
    """
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)

    phi = phi * (180 / np.pi)  # degrees
    phi[phi == 180] = -180

    return rho, phi


def center_of_mass(input, labels=None, index=None):
    """
    Calculate the center of mass of the values of an array at labels.

    Args:
        input : ndarray
            Data from which to calculate center-of-mass. The masses can either
            be positive or negative.
        labels : ndarray, optional
            Labels for objects in `input`, as generated by `ndimage.label`.
            Only used with `index`. Dimensions must be the same as `input`.
        index : int or sequence of ints, optional
            Labels for which to calculate centers-of-mass. If not specified,
            all labels greater than zero are used. Only used with `labels`.

    Returns
    -------
    center_of_mass : tuple, or list of tuples
        Coordinates of centers-of-mass.

    Note:
        This is adapted from scipy.ndimage to support cupy.
    """
    _sni = sni
    if env.cupy_available():
        import cupy as cp

        if get_array_module(input) == cp:
            import cupyx.scipy.ndimage as csni

            _sni = csni

    return _sni.center_of_mass(input, labels=labels, index=index)
