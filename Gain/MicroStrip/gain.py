import numpy as np
from scipy.integrate import odeint

signal = 0
idler = 1
pump = 2


def fun(a,b,c,d,e,f):
    return a + b + c + d

def Gain(init_vals_arr, AmplitudeEquations, AmplitudeEquationsArgs,z,L):
    """

    :param z:
    :param init_vals_arr:
    :param L:
    :param AmplitudeEquations:
    :param AmplitudeEquationsArgs:
    :return:
    """
    soln = odeint(AmplitudeEquations, init_vals_arr, z, args=AmplitudeEquationsArgs)
    # todo look at gain in mathimatica where L is use
    return soln[:, signal][L]
