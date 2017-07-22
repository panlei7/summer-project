"""convertion between 2d and 1d
"""

import numpy as np
from scipy.interpolate import interp2d, RectBivariateSpline

__all__ = ['loadmodel',
           'convert1dto2d',
           'convert2dto1d',
           'fg2ig_2d',
           'ig2fg_2d']


def loadmodel(filenm):
    try:
        return np.load(filenm)
    except IOError as e:
        print("Error in data file:", e)


def convert2dto1d(mat2d):
    return mat2d.flatten()


def convert1dto2d(mat1d, nx, ny):
    return mat1d.reshape(ny, nx)


def fg2ig_2d(fg2d, nsi):
    ny_ig, nx_ig = [int(x/nsi) for x in fg2d.shape]
    return np.einsum('ijkl->ik',
                     fg2d.reshape(ny_ig, nsi, nx_ig, nsi))/(nsi**2)


def ig2fg_2d(ig2d, nsi):
    ny, nx = ig2d.shape
    x_ig = np.arange(nx) * nsi
    y_ig = np.arange(ny) * nsi
    # f = interp2d(x_ig, y_ig, ig2d)
    f = RectBivariateSpline(y_ig, x_ig, ig2d)

    x_fg = np.arange(nx * nsi)
    y_fg = np.arange(ny * nsi)
    # return f(x_fg, y_fg)
    return f(y_fg, x_fg)
