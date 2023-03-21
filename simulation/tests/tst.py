import cmath
import time

import matplotlib.pyplot as plt
import numpy as np

from simulation.utills.constants import SPEED_OF_LIGHT, PI2
from simulation.utills.functions import micro_meters_to_meters, hertz_to_GHz, mult_mats, beta_unfold


# todo enforce some standard format and file type
# todo needs to be a csv file with n cols each col is in consisant units
# todo same with unit cell length
# todo using loadtxt()


def ABCD_Mat(zc, gamma, line_length):
    gl = gamma * line_length
    coshGL = cmath.cosh(gl)
    sinhGL = cmath.sinh(gl)

    return [[coshGL, zc * sinhGL],
            [(1 / zc) * sinhGL, coshGL]]


def bloch_impedance_Zb(ABCD_mat_2x2: [[float]]):
    A = ABCD_mat_2x2[0][0]
    B = ABCD_mat_2x2[0][1]
    D = ABCD_mat_2x2[1][1]

    ADs2 = cmath.sqrt(((A + D) ** 2) - 4)
    ADm = A - D

    B2 = 2 * B

    ZB = - (B2 / (ADm + ADs2))
    ZB2 = - (B2 / (ADm - ADs2))

    return max(ZB, ZB2, key=lambda c: c.real)


def gamma_d(ABCD_mat_2x2: [[float]]):
    A = ABCD_mat_2x2[0][0]
    D = ABCD_mat_2x2[1][1]
    return cmath.acosh(((A + D) / 2))


csv_data = np.loadtxt("/Users/aaron/Desktop/wL(um)-Zc(ohm)-bbo.csv",
                      delimiter="	", dtype=float)

sf = .1
ef = 25

frequency_range = np.linspace(hertz_to_GHz(sf), hertz_to_GHz(ef), 10000)

# plt.plot(csv_data[:, 2])
# plt.show()


# FLOQUET DIMENSIONS

Lu = micro_meters_to_meters(4)

line_1_len = Lu * 110
line_2_len = Lu * 40
line_3_len = Lu * 221
line_4_len = Lu * 40
line_5_len = Lu * 201
line_6_len = Lu * 80
line_7_len = Lu * 93

# pick line widths
Wu = 14
Wl = 31

seg_lens = [
    line_1_len,
    line_2_len,
    line_3_len,
    line_4_len,
    line_5_len,
    line_6_len,
    line_7_len
]

# to we can vectorize this into something real ugly but fast , dont think its needed tho
fig, axs = plt.subplots(2)

L1 = Wl
L2 = Wl
L3 = Wl
gammas, ZBs = [], []

CL_gammas = []

V = (PI2 * frequency_range) / SPEED_OF_LIGHT
start = time.time()
for i,f in enumerate(frequency_range):
    seg_abcds = []


    seg_gamma, seg_Zc = complex(0, csv_data[:, 2][Wu] * V[i]), complex(csv_data[:, 1][Wu], 0)
    seg_abcds.append(ABCD_Mat(seg_Zc, seg_gamma, seg_lens[0]))

    seg_gamma, seg_Zc = complex(0, csv_data[:, 2][L1] * V[i]), complex(csv_data[:, 1][L1], 0)
    seg_abcds.append(ABCD_Mat(seg_Zc, seg_gamma, seg_lens[1]))

    seg_gamma, seg_Zc = complex(0, csv_data[:, 2][Wu] * V[i]), complex(csv_data[:, 1][Wu], 0)
    seg_abcds.append(ABCD_Mat(seg_Zc, seg_gamma, seg_lens[2]))

    seg_gamma, seg_Zc = complex(0, csv_data[:, 2][L2] * V[i]), complex(csv_data[:, 1][L2], 0)
    seg_abcds.append(ABCD_Mat(seg_Zc, seg_gamma, seg_lens[3]))

    seg_gamma, seg_Zc = complex(0, csv_data[:, 2][Wu] * V[i]), complex(csv_data[:, 1][Wu], 0)
    seg_abcds.append(ABCD_Mat(seg_Zc, seg_gamma, seg_lens[4]))

    seg_gamma, seg_Zc = complex(0, csv_data[:, 2][L3] * V[i]), complex(csv_data[:, 1][L3], 0)
    seg_abcds.append(ABCD_Mat(seg_Zc, seg_gamma, seg_lens[5]))

    seg_gamma, seg_Zc = complex(0, csv_data[:, 2][Wu] * V[i]), complex(csv_data[:, 1][Wu], 0)
    seg_abcds.append(ABCD_Mat(seg_Zc, seg_gamma, seg_lens[6]))

    unit_cell_mat = mult_mats(seg_abcds)
    gammas.append(gamma_d(unit_cell_mat))
    ZBs.append(bloch_impedance_Zb(unit_cell_mat))

    seg_gamma, seg_Zc = complex(0, csv_data[:, 2][Wu] * V[i]), complex(csv_data[:, 1][Wu], 0)
    CL_unit_cell_mat = ABCD_Mat(seg_Zc, seg_gamma, sum(seg_lens))
    CL_gammas.append(gamma_d(CL_unit_cell_mat))

print(time.time() - start)
axs[0].plot(frequency_range, np.real(np.array(gammas)))
axs[0].plot(frequency_range, beta_unfold(np.imag(np.array(gammas))) - beta_unfold(np.imag(np.array(CL_gammas))))
axs[1].plot(frequency_range, np.real(np.array(ZBs)))
axs[1].plot(frequency_range, np.imag(np.array(ZBs)))
axs[1].set_ylim([-500, 500])
plt.show()
