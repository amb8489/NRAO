from BlockTwoTransmissionLineModels.lineModels.MicroStripModel import *
from SuperConductivityEquations.SCE import *
from Supports.constants import *
from Supports.Support_Functions import *

Epsilonr = 3.8  # Permitivitty substrate
tss = 300E-9  # Thickness strip in m
tgg = 1000E-9  # Thickness ground in m
Tc = 8.7  # Critical temperature
Jc = 200000E4  # Critical current
Rho = 6.17E-8  # Resistivity in \[CapitalOmega].m
Sigma = 1 / Rho  # Normal state conductivity
fopr = 7E9
Topr = 1
TanD = 0
w = .25
H = 1
f = fopr
T = Topr

model = SuperConductingMicroStripModel(H, w, tss, Epsilonr, TanD)

ZP = model.Zmsht  # Zmsst -- Schneider; Zmsht -- Hammerstad;
EpsiloneffP = model.epsilon_effht














def Sigma_scn(f, T):
    return sigma_N(calc_delta(T, Tc), PLANCK_CONSTev * f, KB * T)


def Sigma_sc(f, T):
    return Sigma * Sigma_scn(f, T)


def zs(f):
    return Zs(fopr, Sigma_sc(f, Topr), tss)


def zwyas(w, H, f):
    return model.ZSy(ZP, zs(f), f, Epsilonr, w, H, tss)


def bwyas(w, H, f):
    return model.beta_Soy(EpsiloneffP, zs(f), f, Epsilonr, w, H, tss)


def vwyas(w, H, f):
    return model.vSy(EpsiloneffP, zs(f), f, Epsilonr, w, H, tss)


def awyas(w, H, f):
    return model.aplha_Sy(EpsiloneffP, zs(f), f, Epsilonr, w, H, tss)


def zkwyas(w, H, f):
    return model.apha_ky(zs(f), f, w, H, tss)


# (*Extra funcions to check variation with t strip*)


def zwyasT(w, H, f, tss):
    return model.ZSy(ZP, zs(f), f, Epsilonr, w, H, tss)


def bwyasT(w, H, f, tss):
    return model.beta_Soy(EpsiloneffP, zs(f), f, Epsilonr, w, H, tss)


def vwyasT(w, H, f, tss):
    return model.vSy(EpsiloneffP, zs(f), f, Epsilonr, w, H, tss)


def awyasT(w, H, f, tss):
    return model.aplha_Sy(EpsiloneffP, zs(f), f, Epsilonr, w, H, tss)


def zkwyasT(w, H, f, tss):
    return model.apha_ky(zs(f), f, w, H, tss)


def Alphaktwyas(w, H, tss, f):
    return model.apha_ky(zs(f), f, w, H, tss)  # (*Kinetic inductance fraction*);


# print("Delta_O: ", Delta_O(8.7))
# print("Lambda0: ", model.Lambda0(1.6207455429497568E7, Delta_O(8.7)))
# print("calc_delta: ",calc_delta(T, Tc))


print("Sigma_scn: ", Sigma_scn(f, T))

print("Sigma_sc: ", Sigma_sc(f, T))

print("zs: ", zs(f))

print("zwyas: ", zwyas(w, H, f))

print("bwyas: ", bwyas(w, H, f))

print("vwyas: ", vwyas(w, H, f))

print("awyas: ", awyas(w, H, f))

print("zkwyas: ", zkwyas(w, H, f))
