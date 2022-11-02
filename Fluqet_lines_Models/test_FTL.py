import cmath
import math

import numpy as np
from matplotlib import pyplot as plt

from BlockTwoTransmissionLineModels.lineModels.MicroStripModel import SuperConductingMicroStripModel
from Fluqet_lines_Models.Fluqet_line_equations import ABCD_TL, GammaDZBN, UnitCellABCD_mats, S21Ncell, S12


def Pd(mat):
    mat_A = mat[0][0]
    mat_D = mat[1][1]

    return np.arccosh((mat_A + mat_D) / 2)


def Zb(mat, Z):
    mat_A = mat[0][0]
    mat_B = mat[0][1]
    mat_D = mat[1][1]

    ADs2 = cmath.sqrt(pow(mat_A + mat_D, 2) - 4)

    B2 = 2 * mat_B

    ADm = mat_A - mat_D

    return [- ((B2 * Z) / (ADm + ADs2)), - ((B2 * Z) / (ADm - ADs2))]


# ---------------------------- unit cell inputs
d = 0.0023
l1 = 5e-5
# width of unloaded
Wu = 1.49e-6
A = 1.2
B = 2
# width of loads
Wl = A * Wu

# ---------------------------- sce inputs
er = 10
H = 2.5e-7
ts = 6e-8
tg = 3e-7
Tc = 14.28
pn = 1.008E-6
tanD = 0

# TODO temp is > 0 things get weird in beta
op_temp = 0
N = 100

# ---------------------------- lengths of matrix
Length1 = 0.5 * ((d / 3) - l1)
length1 = l1
length2 = l1
Length2 = (d / 3) - 0.5 * (length1 + length2)
length3 = 2 * length1
Length3 = (d / 3) - 0.5 * (length2 + length3)
Length4 = 0.5 * ((d / 3) - length3)

# ---------------------------- models of SuperConductingMicroStripModel
# ---------------------------- one for unloaded , one for loaded

model_unloaded = SuperConductingMicroStripModel(H, Wu, ts, er, tanD)
model_loaded = SuperConductingMicroStripModel(H, Wl, ts, er, tanD)

StartFreq, EndFreq, step = 6.7e9, 6.9e9, 1e5
s12, FLminusCL, a, b, r, x, freqs = [], [], [], [], [], [], []
F = StartFreq
while F < EndFreq:
    # calc Zc for load and unloaded
    loaded_Zc = model_loaded.characteristic_impedance_auto(F, op_temp, Tc, pn)
    Unloaded_Zc = model_unloaded.characteristic_impedance_auto(F, op_temp, Tc, pn)

    # calc propagation const for loaded and unloaded
    loaded_propagation = model_loaded.propagation_constant_auto(F, op_temp, Tc, pn)
    Unloaded_propagation = model_loaded.propagation_constant_auto(F, op_temp, Tc, pn)

    # ------------- ABCD 1 -------------
    mat1 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, Length1)

    # ------------- ABCD 2 -------------
    mat2 = ABCD_TL(loaded_Zc, loaded_propagation, length1)

    # ------------- ABCD 3 -------------
    mat3 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, Length2)

    # ------------- ABCD 4 -------------
    mat4 = ABCD_TL(loaded_Zc, loaded_propagation, length2)

    # ------------- ABCD 5 -------------
    mat5 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, Length3)

    # ------------- ABCD 6 -------------
    mat6 = ABCD_TL(loaded_Zc, loaded_propagation, length3)

    # ------------- ABCD 7 -------------
    mat7 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, Length4)

    # ------------- ABCD UNIT CELL-------------
    ABCD_UC = UnitCellABCD_mats([mat1, mat2, mat3, mat4, mat5, mat6, mat7])

    # ---------------------------- calc bloch impedence and probagation const for UC
    ZB = Zb(ABCD_UC, 1)[1]
    pb = Pd(ABCD_UC)



# ---------------------------- plots ----------------------------
    a.append(pb.real)
    b.append(pb.imag)
    r.append(ZB.real)
    x.append(ZB.imag)
    freqs.append(F)

    F += step

fig, axs = plt.subplots(4)
fig.suptitle('a  b  r  x')
axs[0].plot(freqs, a)
axs[1].plot(freqs, b)
axs[2].plot(freqs, r)
axs[3].plot(freqs, x)
plt.show()
