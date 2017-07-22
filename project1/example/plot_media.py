#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
# from model import fg2ig_2d, ig2fg_2d

model = 1./np.load('data_model.npy')
nsi = 4
# y = fg2ig_2d(model, nsi)

plt.figure()
plt.imshow(model, interpolation='nearest',
           vmin=0.14, vmax=0.16, cmap="seismic")
plt.colorbar()
plt.show()
