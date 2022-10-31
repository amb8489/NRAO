from BlockTwoTransmissionLineModels.lineModels.MicroStripModel import *
from SuperConductivityEquations.SCE import *
from Supports.constants import *

Epsilonr = 3.8  # Permitivitty substrate
tss = 3 / 10_000_000  # Thickness strip in m
tgg = 1 / 1_000_000  # Thickness ground in m
Tc = 14.28  # Critical temperature
Jc = 2000000000  # Critical current
Rho = 6.17E-8  # Resistivity in \[CapitalOmega].m
Sigma = 1 / Rho  # Normal state conductivity
fopr = 7000000000
Topr = 1
TanD = 0
w = .25
H = 1
f = fopr
T = Topr

model = SuperConductingMicroStripModel(H, w, tss, Epsilonr, TanD)

ZP = model.Zmsht  # Zmsst -- Schneider; Zmsht -- Hammerstad;
EpsiloneffP = model.epsilon_effht

"""
tests for first two main blocks 
"""


def Sigma_scn(FF, TT):
    print(f"delta {calc_delta(TT, Tc)}")
    return sigma_N(0.00217067, PLANCK_CONSTev * FF, KB * TT)


def Sigma_sc(FF, TT):

    print(f"sigma {Sigma}")
    print(f"f     {FF}")
    print(f"t     {TT}")
    return Sigma * Sigma_scn(FF, TT)


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


def akwyas(w, H, f):
    return model.apha_ky(zs(f), f, w, H, tss)


# print("Delta_O: good", Delta_O(Tc))
# print("Lambda0: good", model.Lambda0(Sigma, Delta_O(Tc)))
# print("calc_delta: good", calc_delta(T, Tc))
# print("Sigma_scn: good ", Sigma_scn(f, T))

print("\nSigma_sc: ", Sigma_sc(f, T))
print("conductivity: ", conductivity(f, T, Tc, Rho))


# print("zs: good", zs(f))
#
# print("zwyas: good", zwyas(w, H, f))
#
# print("bwyas:good ", bwyas(w, H, f))
#
# print("vwyas: good", vwyas(w, H, f))
#
# print("awyas: good", awyas(w, H, f))
#
# print("akwyas: good", akwyas(w, H, f))

exit(1)

# testing Geometrical factors #checked
w = 1
h = 1
t = 1
epsilon_fm = model.epsilon_effst(Epsilonr, w, h, t)
Zs = zs(f)

g1 = model.gg1(w, h, t)
g2 = model.gg2(w, h, t)
Z = model.series_impedance_Z(Zs, g1, g2, f)

print(g1)

print(g2)

print(Z)

Y = model.shunt_admittance_Y(epsilon_fm, g1, f)
print(Y)

print(model.characteristic_impedance(Z, Y))

print(model.propagation_constant(Z, Y))








