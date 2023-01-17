import scipy
signal = 0
idler = 1
pump = 2


def Solve_ode(init_amplitudes, AmplitudeEquations, AmplitudeEquationsArgs, z, L):


    """
    :param z:
    :param init_amplitudes:
    :param L:
    :param AmplitudeEquations:
    :param AmplitudeEquationsArgs:
    :return:
    """

    return scipy.integrate.odeint(AmplitudeEquations, init_amplitudes, z, AmplitudeEquationsArgs)[:, signal][L]
