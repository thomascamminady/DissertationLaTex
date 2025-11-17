import numpy as np


def duplicate(x,y,z,w):
    """
    Takes quadrature points in the first octant
    via x,y,w,w as numpy arrays of the same length
    and returns the duplicated points on all octants,
    i.e., they are 8 times that long.
    """
    
    X = np.hstack([ x, x, x, x,-x,-x,-x,-x])
    Y = np.hstack([ y,-y, y,-y, y,-y, y,-y])
    Z = np.hstack([ z, z,-z,-z, z, z,-z,-z])
    W = np.hstack([ w, w, w, w, w, w, w, w])
    return X,Y,Z,W
    
