import math

from scipy.special import ellipk

from utills.constants import epsilon_0


def kp(k):
    return math.sqrt(1 - k ** 2)


def KKp(k):
    return ellipk(k) / ellipk(kp(k))


def KpK(k):
    return ellipk(kp(k)) / ellipk(k)


def CapacitanceModel1(n, ep_r, sg, s1, gg, gendg, h, l, t):
    delta_s = 0 if t == 0 else (t / (2 * math.pi * ep_r)) * (1 + math.log((8 * math.pi * sg) / t))
    s = sg + delta_s
    g = gg - delta_s
    gend = 2 * gendg

    # Calculating C1
    k01 = math.sqrt(1 - ((g) / (g + s)) ** 2)

    k11 = math.sqrt(1 - ((math.sinh((math.pi * g) / (2 * h))) ** 2 / (math.sinh((math.pi * (s + g)) / (2 * h))) ** 2))

    q11 = KKp(k11) * KpK(k01)

    Ep_e1 = 1 + q11 * ((ep_r - 1) / 2)

    C1 = epsilon_0 * Ep_e1 * KKp(k01) * l

    # Calculating C3
    k02 = math.sqrt((s1 * s) / ((2 * g + s1) * (2 * g + s)))

    Esgs1 = math.exp((2 * math.pi * (s + 2 * g + s1)) / h)

    Egs = math.exp((2 * math.pi * (2 * g + s)) / h)

    Es = math.exp((2 * math.pi * s) / h)

    k12 = (((Esgs1 - Egs) * (Es - 1) * ((Esgs1 - Es) ** -1) * ((Egs - 1) ** -1)) ** .5)

    q12 = (KKp(k12) * KpK(k02))

    ep_e2 = (1 + q12 * ((ep_r - 1) / 2))

    C3 = (4 * epsilon_0 * ep_e2 * KpK(k02) * l)

    # Calculating C2
    A = ((2 * s + 4 * g) / 4)

    Lext = ((A / (12.5 * 10 ** -6)) * ((-4 * 10 ** -6) * ((s / A) ** 2) + (9 * 10 ** -6) * (s / A) + (8 * 10 ** -6)) * (
            1 + (A / (gend + A)) ** 3))

    C2 = 2 * epsilon_0 * Ep_e1 * KKp(k01) * Lext

    # Final result

    return ((n - 3) * C1 + n * C2 + C3) / (n - 1)


def capacitance_model_selector(model, n, epsilonr, sg, s1, gg, gendg, h, l, t=0):
    match model:
        case 1:
            return CapacitanceModel1(n, epsilonr, sg, s1, gg, gendg, h, l, t)
        case default:
            raise NotImplementedError(f"capacitance model {default} not implemented")
