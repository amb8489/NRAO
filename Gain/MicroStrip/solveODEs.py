import scipy
signal = 0
idler = 1
pump = 2


def Solve_ode(init_vals_arr, AmplitudeEquations, AmplitudeEquationsArgs, z, L):


    """
    :param z:
    :param init_vals_arr:
    :param L:
    :param AmplitudeEquations:
    :param AmplitudeEquationsArgs:
    :return:
    """
    return scipy.integrate.odeint(AmplitudeEquations, init_vals_arr, z, args=AmplitudeEquationsArgs)[:, signal][L]
