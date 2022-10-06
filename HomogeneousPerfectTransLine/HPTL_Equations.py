"""
NRAO
Aaron Berghash

Formulas from https://qucs.sourceforge.net/tech/node75.html#SECTION001211200000000000000
"""

import math
import cmath
from constants import PI, MU_0, PI2, z0, PI4, PLANCK_CONST_REDUCEDev
from Support_Functions import sech, coth, ccoth


def Lambda0(sigma_N, delta_O):
    # TODO ask about the complex square root should just the real part be rooted or both re and im parts
    # AND sigma_N is 1/ Pn
    return math.sqrt(PLANCK_CONST_REDUCEDev / (PI * MU_0 * sigma_N * delta_O))


def Zs(freq, conductivity, ts):
    # TODO ask about the complex square root should just the real part be rooted or both re and im parts
    a = cmath.sqrt((1j * PI2 * freq * MU_0) / conductivity)
    b = ccoth(cmath.sqrt(1j * PI2 * freq * MU_0 * conductivity) * ts)
    return a * b


# todo what is t used for
def z_slow(f, yO, t):
    return 1j * PI2 * f * MU_0 * yO


# TODO DO WHERE IS THE T USED ??
def Lambda(zs, f, t):
    return (zs / (PI2 * f * MU_0)).imag


# ----------  schneider   t = 0  ----------
def Fs(w, h):
    return math.sqrt(1 + (10 * (h / w)))


def epsilon_effs(epsilon_r, w, h):
    return ((epsilon_r + 1) / 2) + ((epsilon_r - 1) / (2 * Fs(w, h)))


def zmss(epsilon_r, w, h):
    z0eff = z0 / (math.sqrt(epsilon_effs(epsilon_r, w, h)))

    if w / h <= 1:

        return z0eff * (1 / PI2) * math.log(((8 * h) / w) + (w / (4 * h)))

    return z0eff / ((w / h) + 2.42 - (0.44 * (h / w)) + pow(1 - (h / w), 6))


# ----------  schneider   t > 0  ----------


def epsilon_effst(epsilon_r, w, h, t):
    u = w / h

    if u <= (1 / PI2):
        delta_w = (t / PI) * (1 + math.log((PI4 * w) / t))
    else:
        delta_w = (t / PI) * (1 + math.log((2 * h) / t))

    return epsilon_effs(epsilon_r, w + delta_w, h)


def zmsst(epsilon_r, w, h, t):
    u = w / h

    if u <= (1 / PI2):
        delta_w = (t / PI) * (1 + math.log((PI4 * w) / t))
    else:
        delta_w = (t / PI) * (1 + math.log((2 * h) / t))

    return zmss(epsilon_r, w + delta_w, h)


# ----------  Hammerstad   t = 0  ----------

def epsilon_effh(epsilon_r, w, h):
    u = w / h

    u4 = pow(u, 4)

    firstLog = math.log((u4 + pow(u / 52, 2)) / (u4 + 0.432))
    secondLog = math.log(1 + pow(u / 18.1, 3))

    a = 1 + (1 / 49) * firstLog + (1 / 18.7) * secondLog

    b = 0.564 * pow((epsilon_r - .9) / (epsilon_r + 3), 0.053)

    return ((epsilon_r + 1) / 2) + ((epsilon_r - 1) / 2) * pow(1 + (10 / u), -a * b)


def ZL1(w, h):
    u = w / h

    fu = 6 + (PI2 - 6) * math.exp(-pow(30.666 / u, 0.7528))

    return (z0 / PI2) * math.log((fu / u) + math.sqrt(1 + pow(2 / u, 2)))


# ----------  Hammerstad   t > 0  ----------


def delta_wr(epsilon_r, w, h, t):
    return (delta_w1(w, h, t) * (1 + sech(math.sqrt(epsilon_r - 1)))) / 2


def delta_w1(w, h, t):
    u = w / h
    th = t / h

    upper = 4 * math.e
    lower = th * pow(coth(math.sqrt(6.517 * u)), 2)

    return (t / PI) * math.log(1 + (upper / lower))


def epsilon_effht(epsilon_r, w, h, t):
    w1 = w + delta_w1(w, h, t)
    wr = w + delta_wr(epsilon_r, w, h, t)

    zl1_up = ZL1(w1, h)
    zl1_low = ZL1(wr, h)
    return epsilon_effh(epsilon_r, wr, h) * pow(zl1_up / zl1_low, 2)


def Zmsht(epsilon_r, w, h, t):
    wr = w + delta_wr(epsilon_r, w, h, t)
    upper = ZL1(wr, h)
    lower = math.sqrt(epsilon_effht(epsilon_r, wr, h, t))

    return upper / lower

# -------------------
