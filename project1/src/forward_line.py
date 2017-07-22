from model import convert1dto2d, convert2dto1d, ig2fg_2d, fg2ig_2d
import numpy as np
from bresenham import get_line
import pyximport
pyximport.install(setup_args={'include_dirs': np.get_include()})
import travel_time
import yaml
import matplotlib.pyplot as plt

__all__ = ['ForwardLine']


class ForwardLine:

    def __init__(self, filename):
        self.__read_config(filename)
        self.create_data()

    def __read_config(self, filenm):
        with open(filenm, 'r') as stream:
            config = yaml.load(stream)

        self.nx = config['nx']
        self.ny = config['ny']
        self.nsampling = config['nsampling']
        self.nx_ig = int(self.nx / self.nsampling)
        self.ny_ig = int(self.ny / self.nsampling)

        # source and receiver
        type_sr = config['type_sr']
        if type_sr == 'line':
            bs, es, ds = config['source']
            if ds[0] == 0:
                self.loc_src = [(bs[0], y) for y in range(bs[1], es[1], ds[1])]
            elif ds[1] == 0:
                self.loc_src = [(x, bs[1]) for x in range(bs[0], es[0], ds[0])]
            else:
                self.loc_src = [(x, y) for x in range(bs[0], es[0], ds[0])
                                for y in range(bs[1], es[1], ds[1])]
            br, er, dr = config['receiver']
            if dr[0] == 0:
                self.loc_rec = [(br[0], y) for y in range(br[1], er[1], dr[1])]
            elif dr[1] == 0:
                self.loc_rec = [(x, br[1]) for x in range(br[0], er[0], dr[0])]
            else:
                self.loc_rec = [(x, y) for x in range(br[0], er[0], dr[0])
                                for y in range(br[1], er[1], dr[1])]
        elif type_sr == 'point':
            file_src = config['file_src']
            with open(file_src, 'r') as f:
                self.loc_src = []
                for line in f:
                    loc1, loc2 = [float(x) for x in line.split()]
                    self.loc_src.append((loc1, loc2))
            file_rec = config['file_rec']
            with open(file_rec, 'r') as f:
                self.loc_rec = []
                for line in f:
                    loc1, loc2 = [float(x) for x in line.split()]
                    self.loc_rec.append((loc1, loc2))
        self.points_ray = {}
        for id_src, ls in enumerate(self.loc_src):
            for id_rec, lr in enumerate(self.loc_rec):
                # find the points that the ray travels from source to receiver
                self.points_ray[(id_src, id_rec)] = np.array(get_line(ls, lr))

        self.model = config['model']
        if self.model == 'checkboard':
            checkboard = config['checkboard']
            self.nx_cb = checkboard['nx']
            self.ny_cb = checkboard['ny']
            self.vref_cb = checkboard['vref']
            self.vmax_cb = checkboard['vmax']
        self.bounds = config['bounds_percentage']


    def create_data(self):

        # create model
        x = np.arange(self.nx)
        y = np.arange(self.ny)
        X, Y = np.meshgrid(x, y)
        if self.model == 'checkboard':
            self.model_data = (
                self.vmax_cb *
                np.sin(np.pi * X / self.nx * self.nx_cb) *
                np.sin(np.pi * Y / self.ny * self.ny_cb)
                + self.vref_cb)
            model_ref = self.vref_cb * np.ones_like(self.model_data)
            model_ref = fg2ig_2d(model_ref, self.nsampling)
            self.ref = convert2dto1d(model_ref)

        np.save('data_model.npy', self.model_data)

        # create data
        self.data = {}
        for id_src, ls in enumerate(self.loc_src):
            for id_rec, lr in enumerate(self.loc_rec):
                self.data[(id_src, id_rec)] \
                    = travel_time.travel_time(
                        1./self.model_data,
                        self.points_ray[(id_src, id_rec)])
        return self.model_data.flatten(), self.ref


    def create_x0(self):
        """create the inital model"""
        return np.ones(self.nx_ig*self.ny_ig) * self.vref_cb

    def create_bounds(self):
        """for scipy.optimize.differential_evolution
        """
        x0 = self.create_x0()
        vmin = x0 * (1 - self.bounds)
        vmax = x0 * (1 + self.bounds)
        return [(x1, x2) for (x1, x2) in zip(vmin, vmax)]


    def misfit(self, ig1d):
        """calculate the misfit function
        """
        ig1d_tmp = np.array(ig1d)
        ig2d = convert1dto2d(ig1d_tmp, self.nx_ig, self.ny_ig)
        fg2d = ig2fg_2d(ig2d, self.nsampling)
        slowness = 1./fg2d

        obj = 0.
        for id_src, ls in enumerate(self.loc_src):
            for id_rec, lr in enumerate(self.loc_rec):
                points = self.points_ray[(id_src, id_rec)]
                t = travel_time.travel_time(slowness, points)
                obj += (t - self.data[(id_src, id_rec)])**2
        return obj

    def fitness(self, ig1d):
        """for pygmo
        """
        return (self.misfit(ig1d), )

    def get_bounds(self):
        """for pygmo
        """
        x0 = self.create_x0()
        vmin = x0 * (1 - self.bounds)
        vmax = x0 * (1 + self.bounds)
        return (list(vmin), list(vmax))


    def gradient(self, ig1d):
        ig1d_tmp = np.array(ig1d)
        ig2d = convert1dto2d(ig1d_tmp, self.nx_ig, self.ny_ig)
        fg2d = ig2fg_2d(ig2d, self.nsampling)
        slowness = 1. / fg2d

        grad2d = np.zeros_like(fg2d)
        for id_src, ls in enumerate(self.loc_src):
            for id_rec, lr in enumerate(self.loc_rec):
                points = self.points_ray[(id_src, id_rec)]
                t = travel_time.travel_time(slowness, points)
                diff = t - self.data[(id_src, id_rec)]
                idx, idy = points[:, 0], points[:, 1]
                grad2d[idx, idy] -= diff * slowness[idx, idy]**2

        grad2d = fg2ig_2d(grad2d, self.nsampling)
        grad = convert2dto1d(grad2d)
        return grad
