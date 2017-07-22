import numpy as np
import pygmo as pg
import matplotlib.pyplot as plt
import yaml
from forward_line import ForwardLine
from scipy.optimize import minimize, differential_evolution
from timer import Timer
import matplotlib.pyplot as plt
from utils import Plot


if __name__ == "__main__":
    forward = ForwardLine('config.yml')
    model_data, _ = forward.create_data()

    func = forward.misfit
    jac = forward.gradient

    x0 = forward.create_x0()
    bounds = forward.create_bounds()

    with open("config.yml", 'r') as stream:
        config = yaml.load(stream)
        gen = config['gen']
        alg = config['algorithm']


    timer = Timer()
    timer.start()

    if alg == 'CG':
        res = minimize(func, x0, method='CG', jac=jac,
                       options={'gtol': 1e-5, 'disp': True})
        best_x = res.x
        best_f = res.fun
    elif alg == 'LBFGS':
        res = minimize(func, x0, method='L-BFGS-B', jac=jac,
                       options={'gtol': 1e-5, 'disp': True})
        best_x = res.x
        best_f = res.fun
    elif alg == 'DE1':
        # scipy's DE is too slow
        res = differential_evolution(func,
                                     bounds,
                                     strategy="best1bin",
                                     # strategy="randtobest1exp",
                                     maxiter=gen,
                                     popsize=5,
                                     disp=True)
        best_x = res.x
        best_f = res.fun
    elif alg == 'DE2':
        prob = pg.problem(forward)
        algo = pg.algorithm(pg.de1220(gen=gen,
                                      variant_adptv=2))
        algo.set_verbosity(10)
        isl = pg.island(algo=algo,
                        prob=prob,
                        size=x0.shape[0]*2)
        isl.evolve()
        isl.wait()
        best_f = isl.get_population().champion_f
        best_x = isl.get_population().champion_x


    timer.stop()
    print("elapsed time: {:14.3f} s".format(timer.elapsed))

    plot_gradient = 0
    plot_result = 1

    fig = Plot("config.yml")
    if plot_gradient:
        fig.plot_gradient(jac(x0))

    if plot_result:
        fig.plot_result(model_data, best_x)
    plt.show()
