import math
from constants import PI, MU_0, PI2, z0, PI4
from functions import sech, coth


# todo name and comment all functions

# todo what is hr
def penitration_depth(sigma_Normilized, delta_O):
    hr = ...
    return math.sqrt(hr / (math.pi * MU_0 * sigma_Normilized * delta_O))


def z_slow(f, y0, t):
    return 1j * PI2 * f * MU_0 * y0


def surface_impedance(freq, conductivity, ts):
    a = math.sqrt((1j * PI2 * freq * MU_0) / conductivity)
    b = coth(math.sqrt(1j * PI2 * freq * MU_0 * conductivity) * ts)
    return a * b


# TODO DO WHERE IS THE T USED ??
def y(zs, f, t):
    return (zs / (PI2 * f * MU_0)).imag


# ----------  schneider   t = 0  ----------
def Fs(w, h):
    return math.sqrt(1 + 10 * (h / w))


def epsilon_effs(epsilon_r, w, h):
    return ((epsilon_r + 1) / 2) + ((epsilon_r - 1) / (2 * Fs(w, h)))


def zmss(epsilon_r, w, h):
    #TODO
    pass

# ----------  schneider   t > 0  ----------


def epsilon_effst(epsilon_r, w, h, t):
    u = w / h

    delta_w = None

    if u <= (1 / PI2):
        delta_w = (t / PI) * (1 + math.log((PI4 * w) / t))
    else:
        delta_w = (t / PI) * (1 + math.log((2 * h) / t))

    return epsilon_effs(epsilon_r, w + delta_w, h)



def zmsst(epsilon_r, w, h, t):
    u = w / h

    delta_w = None

    if u <= (1 / PI2):
        delta_w = (t / PI) * (1 + math.log((PI4 * w) / t))
    else:
        delta_w = (t / PI) * (1 + math.log((2 * h) / t))

    return zmss(epsilon_r, w + delta_w, h)


# ----------  Hammerstad   t = 0  ----------

def epsilon_effh(epsilon_r, w, h):
    u = w / h

    u4 = pow(u, 4)

    firstLog = math.log((u4 + pow(u / 52, 2)) / (u4 + .432))
    secondLog = math.log(1 + pow(u / 18.1, 3))

    a = 1 + (1 / 49) * firstLog + (1 / 18.7) * secondLog

    b = .564 * pow((epsilon_r - .9) / (epsilon_r + 3), .053)

    return ((epsilon_r + 1) / 2) + ((epsilon_r - 1) / 2) * pow(1 + (10 / u), -a * b)


def ZL1(w, h):
    u = w / h

    fu = 6 + (PI2 - 6) * math.exp(-pow(30.666 / u, .7528))

    return (z0 / PI2) * math.log((fu / u) + math.sqrt(1 + pow(u / 2, 2)))


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
    return epsilon_effh(epsilon_r, wr, h) * (zl1_up / zl1_low) ** 2


def Zmsht(epsilon_r, w, h, t):
    wr = w + delta_wr(epsilon_r, w, h, t)
    uper = ZL1(wr, h)
    lower = math.sqrt(epsilon_effht(epsilon_r, wr, h, t))

    return uper / lower

    return

# -------------------
