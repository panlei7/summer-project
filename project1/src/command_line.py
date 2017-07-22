import numpy as np
import matplotlib.pyplot as plt
from forward_line import ForwardLine
from scipy.optimize import minimize, differential_evolution
from timer import Timer
import matplotlib.pyplot as plt
from utils import Plot


if __name__ == "__main__":
    forward = ForwardLine('config.yml')
    model_data, _ = forward.create_data()

    func = forward.get_obj
    jac = forward.get_grad

    x0 = forward.create_x0()
    bounds = forward.create_bounds(0.1)

    # plot the initial gradient


    timer = Timer()
    timer.start()

    alg = 3
    if alg == 1:
        res = minimize(func, x0, method='CG', jac=jac,
                       options={'gtol': 1e-5})
    elif alg == 2:
        res = minimize(func, x0, method='L-BFGS-B', jac=jac,
                       options={'gtol': 1e-5})
    elif alg == 3:
        res = differential_evolution(func,
                                     bounds,
                                     strategy="best1bin",
                                     # strategy="randtobest1exp",
                                     maxiter=2000,
                                     popsize=5,
                                     disp=True)

    print(res.message)
    # print(res.fun)
    timer.stop()
    print("elapsed time: {:14.3f} s".format(timer.elapsed))

    plot_gradient = 0
    plot_result = 1

    fig = Plot("config.yml")
    if plot_gradient:
        fig.plot_gradient(jac(x0))

    if plot_result:
        fig.plot_result(model_data, res.x)
    plt.show()
