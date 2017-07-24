from model import convert1dto2d, convert2dto1d, ig2fg_2d, fg2ig_2d
import numpy as np
from bresenham import get_line
import pyximport
pyximport.install(setup_args={'include_dirs': np.get_include()})
import travel_time
import yaml
import matplotlib.pyplot as plt
import pickle

__all__ = ['ForwardLine']


class ForwardLine:

    def __init__(self, filenm):
        with open(filenm, 'r') as stream:
            self.config = yaml.load(stream)
        self.__read_config()
        self.nforward = 0


    def __read_config(self):

        self.nx = self.config['nx']
        self.ny = self.config['ny']
        self.nsampling = self.config['nsampling']
        self.nx_ig = int(self.nx / self.nsampling)
        self.ny_ig = int(self.ny / self.nsampling)

        self.bounds = self.config['bounds_percentage']


    def create_model(self):
        type_model = self.config['model']
        if type_model == 'checkboard':
            checkboard = self.config['checkboard']
            self.nx_cb = checkboard['nx']
            self.ny_cb = checkboard['ny']
            self.vref = checkboard['vref']
            self.vmax_cb = checkboard['vmax']
            x = np.arange(self.nx)
            y = np.arange(self.ny)
            X, Y = np.meshgrid(x, y)
            self.model_data = (
                self.vmax_cb *
                np.sin(np.pi * X / self.nx * self.nx_cb) *
                np.sin(np.pi * Y / self.ny * self.ny_cb)
                + self.vref)
            model_ref = self.vref * np.ones_like(self.model_data)
            model_ref = fg2ig_2d(model_ref, self.nsampling)
            self.ref = convert2dto1d(model_ref)

            np.save('model_data.npy', self.model_data)
        elif type_model == 'user-defined':
            user_defined = self.config['user-defined']
            self.vref = user_defined['vref']
            file_model = user_defined['file_model']
            self.model_data = np.load(file_model)
            model_ref = self.vref * np.ones_like(self.model_data)
            model_ref = fg2ig_2d(model_ref, self.nsampling)
            self.ref = convert2dto1d(model_ref)

        return self.model_data.flatten()


    def __find_ray_path(self):
        # read source and receiver location
        type_sr = self.config['type_sr']
        if type_sr == 'line':
            bs, es, ds = self.config['source']
            if ds[0] == 0:
                self.loc_src = [(bs[0], y) for y in range(bs[1], es[1], ds[1])]
            elif ds[1] == 0:
                self.loc_src = [(x, bs[1]) for x in range(bs[0], es[0], ds[0])]
            else:
                self.loc_src = [(x, y) for x in range(bs[0], es[0], ds[0])
                                for y in range(bs[1], es[1], ds[1])]
            br, er, dr = self.config['receiver']
            if dr[0] == 0:
                self.loc_rec = [(br[0], y) for y in range(br[1], er[1], dr[1])]
            elif dr[1] == 0:
                self.loc_rec = [(x, br[1]) for x in range(br[0], er[0], dr[0])]
            else:
                self.loc_rec = [(x, y) for x in range(br[0], er[0], dr[0])
                                for y in range(br[1], er[1], dr[1])]
        elif type_sr == 'point':
            file_src = self.config['file_src']
            with open(file_src, 'r') as f:
                self.loc_src = []
                for line in f:
                    loc1, loc2 = [float(x) for x in line.split()]
                    self.loc_src.append((loc1, loc2))
            file_rec = self.config['file_rec']
            with open(file_rec, 'r') as f:
                self.loc_rec = []
                for line in f:
                    loc1, loc2 = [float(x) for x in line.split()]
                    self.loc_rec.append((loc1, loc2))

        # find points along the path
        self.points_ray = {}
        for id_src, ls in enumerate(self.loc_src):
            for id_rec, lr in enumerate(self.loc_rec):
                # find the points that the ray travels from source to receiver
                self.points_ray[(id_src, id_rec)] = np.array(get_line(ls, lr))


    def create_data(self):
        self.__find_ray_path()
        self.data = {}
        for id_src, ls in enumerate(self.loc_src):
            for id_rec, lr in enumerate(self.loc_rec):
                self.data[(id_src, id_rec)] \
                    = travel_time.travel_time(
                        1./self.model_data,
                        self.points_ray[(id_src, id_rec)])

        file_data = self.config['file_data']
        with open(file_data, "wb") as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)


    def load_data(self):
        self.__find_ray_path()
        file_data = self.config['file_data']
        with open(file_data, "rb") as f:
            self.data = pickle.load(f)


    def create_x0(self):
        """create the inital model"""
        return np.ones(self.nx_ig*self.ny_ig) * self.vref


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
        self.nforward += 1

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


    def callback_print(self, x):
        misfit = self.misfit(x)
        print("{:5d} {:12.4e}".format(self.nforward, misfit))


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
        self.nforward += 1

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
