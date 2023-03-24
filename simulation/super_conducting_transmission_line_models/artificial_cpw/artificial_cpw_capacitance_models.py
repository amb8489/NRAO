import math

from scipy.special import ellipk

from simulation.utills.constants import epsilon_0
from simulation.utills.functions import printDb

'''

where to put different capacitance models for artificial lines


'''

def __kp(k):
    return math.sqrt(1 - k ** 2)


def __KKp(k):
    return ellipk(k) / ellipk(__kp(k))


def __KpK(k):
    return ellipk(__kp(k)) / ellipk(k)


def __CapacitanceModel1(n, ep_r, sg, s1, gg, gendg, h, l, t):


    delta_s = 0 if t == 0 else (t / (2 * math.pi * ep_r)) * (1 + math.log((8 * math.pi * sg) / t))
    s = sg + delta_s
    g = gg - delta_s
    gend = 2 * gendg

    # Calculating capacitance

    k01 = math.sqrt(1 - ((g / (g + s)) ** 2))

    k11 = math.sqrt(1 - ((math.sinh((math.pi * g) / (2 * h))) ** 2 / (math.sinh((math.pi * (s + g)) / (2 * h))) ** 2))

    q11 = __KKp(k11) * __KpK(k01)

    Ep_e1 = 1 + q11 * ((ep_r - 1) / 2)

    C1 = epsilon_0 * Ep_e1 * __KKp(k01) * l

    # Calculating C3
    k02 = math.sqrt((s1 * s) / ((2 * g + s1) * (2 * g + s)))

    Esgs1 = math.exp((2 * math.pi * (s + 2 * g + s1)) / h)

    Egs = math.exp((2 * math.pi * (2 * g + s)) / h)

    Es = math.exp((2 * math.pi * s) / h)

    k12 = (((Esgs1 - Egs) * (Es - 1) * ((Esgs1 - Es) ** -1) * ((Egs - 1) ** -1)) ** .5)

    q12 = (__KKp(k12) * __KpK(k02))

    ep_e2 = (1 + q12 * ((ep_r - 1) / 2))

    C3 = (4 * epsilon_0 * ep_e2 * __KpK(k02) * l)

    # Calculating C2
    A = ((2 * s + 4 * g) / 4)

    Lext = ((A / (12.5 * 10 ** -6)) * ((-4 * 10 ** -6) * ((s / A) ** 2) + (9 * 10 ** -6) * (s / A) + (8 * 10 ** -6)) * (
            1 + (A / (gend + A)) ** 3))

    C2 = 2 * epsilon_0 * Ep_e1 * __KKp(k01) * Lext

    Ctot = ((n - 3) * C1 + n * C2 + C3)

    return Ctot / (n - 1)


def capacitance_model_selector(n, er, sg, s1, gg, g_end_g, h, l, t, model_type=1):
    printDb("artificial capacitance model chosen: ", model_type)
    match model_type:
        case 1:
            return __CapacitanceModel1(n, er, sg, s1, gg, g_end_g, h, l, t)
        case default:
            raise NotImplementedError(f"Capacitance model {default} not implemented")
