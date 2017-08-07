import cython
cimport cython

import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

@cython.wraparound(False)
@cython.cdivision(True)
@cython.nonecheck(False)
def travel_time(np.ndarray[DTYPE_t, ndim=2] slowness,
                 np.ndarray[long, ndim=2] points_ray):

    cdef int N = points_ray.shape[0]
    cdef double ret
    for x in xrange(0, N):
        ret += slowness[points_ray[x,1], points_ray[x,0]]
    return ret
