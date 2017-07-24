import numpy as np
import pygmo as pg
import matplotlib.pyplot as plt
import yaml
from forward_line import ForwardLine
from scipy.optimize import minimize, differential_evolution
from timer import Timer
import matplotlib.pyplot as plt
from utils import Plot
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="inversion procedure")
    parser.add_argument("-c",
                        "--config",
                        default="config.yml",
                        help="give the configure file")
    parser.add_argument("--plot_gradient",
                        action="store_true",
                        help="whether plotting the gradient of the first step")
    args = parser.parse_args()
    file_config = args.config
    flag_plot_gradient = args.plot_gradient

    forward = ForwardLine(file_config)
    model_data = forward.create_model()
    forward.create_data()
    # forward.load_data()

    func = forward.misfit
    jac = forward.gradient

    x0 = forward.create_x0()
    bounds = forward.create_bounds()

    with open(file_config, 'r') as stream:
        config = yaml.load(stream)
        gen = config['gen']
        alg = config['algorithm']


    timer = Timer()
    timer.start()

    if alg == 'CG':
        res = minimize(func, x0, method='CG', jac=jac,
                       callback=forward.callback_print,
                       options={'gtol': 1e-5})
        best_x = res.x
        best_f = res.fun
    elif alg == 'LBFGS':
        res = minimize(func, x0, method='L-BFGS-B', jac=jac,
                       callback=forward.callback_print,
                       options={'gtol': 1e-5})
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

    fig = Plot(file_config)
    if flag_plot_gradient:
        fig.plot_gradient(jac(x0))

    fig.plot_result(model_data, best_x)
    plt.show()
