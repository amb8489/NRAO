import numpy as np
import scipy.special as sp

from utills.constants import C

epsilon_r = ...
lambda0 = ...
c = C
mu_0 = ...
epsilon_0 = ...


def Cg(epsilon_r, w, s):
    k = w / (w + 2 * s)
    epsilon_eff = (epsilon_r + 1) / 2
    KK1m = KK1(k)
    return 4 * epsilon_0 * epsilon_eff * KK1m


def Lg(w, s):
    k = w / (w + 2 * s)
    KK1m = KK1(k)
    return (mu_0 / 4) * (1 / KK1m)


def KK1(k):
    k1 = np.sqrt(1 - k ** 2)
    return nK(k) / nK(k1)


def nK(k):
    return sp.ellipk(k ** 2)


def gtot(w, s, t):
    k = w / (w + 2 * s)
    k12 = 1 - k ** 2
    K2 = nK(k) ** 2
    gc = (1 / (4 * k12 * K2)) * (np.pi + np.log((4 * np.pi * w) / t) - k * np.log((1 + k) / (1 - k)))
    gg = (k / (4 * k12 * K2)) * (np.pi + np.log((4 * np.pi * (w + 2 * s)) / t) - (1 / k) * np.log((1 + k) / (1 - k)))
    return gc + gg


def LkCPW(Lk, w, s, t):
    return Lk * gtot(w, s, t)


def Lk(lambda0, w, t):
    return mu_0 * (lambda0 ** 2) / (t * w)


def beta_ocpwsc(Lkc, Lg, Cg):
    Ltot = Lkc + Lg
    return c * np.sqrt(Ltot * Cg)


def Zcpwsc(Lkc, Lg, Cg):
    Ltot = Lkc + Lg
    return np.sqrt(Ltot / Cg)


def zwt(w, s, tss):
    Lkc = LkCPW(Lk(lambda0, w, tss), w, s, tss)
    Lg_ = Lg(w, s)
    Cg_ = Cg(epsilon_r, w, s)
    return Zcpwsc(Lkc, Lg_, Cg_)


def gamma_wt(w, s, tss):
    Lkc = LkCPW(Lk(lambda0, w, tss), w, s, tss)
    Lg_ = Lg(w, s)
    Cg_ = Cg(epsilon_r, w, s)
    return beta_ocpwsc(Lkc, Lg_, Cg_)
