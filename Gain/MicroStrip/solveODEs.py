from scipy.integrate import odeint

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
    # todo look at gain in mathimatica where L is use

    return odeint(AmplitudeEquations, init_vals_arr, z, args=AmplitudeEquationsArgs)[:, signal][L]
