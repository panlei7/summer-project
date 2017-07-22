import matplotlib.pyplot as plt
import yaml
import numpy as np


class Plot:

    def __init__(self, filename):
        self.__read_config(filename)


    def __read_config(self, filenm):
        with open(filenm, 'r') as stream:
            config = yaml.load(stream)
        self.nx_fg = config['nx']
        self.ny_fg = config['ny']
        self.vref = config['checkboard']['vref']
        self.vmax = config['checkboard']['vmax']
        nsampling = config['nsampling']
        self.nx_ig = int(self.nx_fg / nsampling)
        self.ny_ig = int(self.ny_fg / nsampling)
        self.x_ig = np.arange(self.nx_ig) * nsampling
        self.y_ig = np.arange(self.ny_ig) * nsampling
        self.x_fg = np.arange(self.nx_fg)
        self.y_fg = np.arange(self.ny_fg)

    def __plot2d(self, x, y, z, title):
        plt.pcolormesh(x, y, z, cmap='jet',
                       vmin=self.vref-self.vmax,
                       vmax=self.vref+self.vmax)
        plt.title(title)
        plt.xlim([0, self.nx_fg])
        plt.ylim([0, self.ny_fg])
        plt.colorbar()

    def plot_gradient(self, grad):
        grad_2d = grad.reshape(self.nx_ig, self.ny_ig)
        fig = plt.figure()
        self.__plot2d(self.x_ig, self.y_ig, grad_2d, "gradient")
        fig.savefig("gradient.png")


    def plot_result(self, model_data, model_inv):
        fig = plt.figure(figsize=(12, 4))
        plt.subplot(121)
        model_data_2d = model_data.reshape(self.nx_fg, self.ny_fg)
        self.__plot2d(self.x_fg, self.y_fg, model_data_2d, "data model")
        plt.subplot(122)
        model_inv_2d = model_inv.reshape(self.nx_ig, self.ny_ig)
        self.__plot2d(self.x_ig, self.y_ig, model_inv_2d, "inverted model")
        fig.savefig("model.png")

        np.save("model_inv", model_inv_2d)
