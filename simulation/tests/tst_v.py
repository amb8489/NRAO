import cmath
import time
from functools import cache
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np

from simulation.utills.constants import SPEED_OF_LIGHT, PI2
from simulation.utills.functions import micro_meters_to_meters, hertz_to_GHz, beta_unfold

from multiprocessing import Pool


# matrix multiplication of a list of 2x2 matrix
def mult_mats(mats):
    # input is an array of 2x2 matrices
    # does floquet_alpha matrix multiplication of all 2x2 matrices passed in,in array

    res = mats[0]
    for mat in mats[1:]:
        res = [
            [res[0][0] * mat[0][0] + res[0][1] * mat[1][0], res[0][0] * mat[0][1] + res[0][1] * mat[1][1]],
            [res[1][0] * mat[0][0] + res[1][1] * mat[1][0], res[1][0] * mat[0][1] + res[1][1] * mat[1][1]]
        ]
    return res



if __name__ == '__main__':

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

        if ZB.real<0:
            return - (B2 / (ADm - ADs2))
        return ZB


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

    D = sum(seg_lens)

    # to we can vectorize this into something real ugly but fast , dont think its needed tho
    fig, axs = plt.subplots(2)

    L1 = Wl
    L2 = Wl
    L3 = Wl
    gammas, ZBs = [], []

    CL_gammas = []

    V = (PI2 * frequency_range) / SPEED_OF_LIGHT


    seg_gamma = np.array([csv_data[Wu][2],csv_data[L1][2],csv_data[Wu][2],csv_data[L2][2],
                 csv_data[Wu][2],csv_data[L3][2],csv_data[Wu][2]])*1j

    seg_zc = np.array([csv_data[Wu][1],csv_data[L1][1],csv_data[Wu][1],csv_data[L2][1],
                 csv_data[Wu][1],csv_data[L3][1],csv_data[Wu][1]])+0j

    tot= 0
    start = time.time()

    for i, f in enumerate(frequency_range):

        seg_abcds = []
        for j in range(len(seg_gamma)):
            seg_abcds.append(ABCD_Mat(seg_zc[j], seg_gamma[j]*V[i], seg_lens[j]))

        unit_cell_mat = mult_mats(seg_abcds)
        gammas.append(gamma_d(unit_cell_mat))
        ZBs.append(bloch_impedance_Zb(unit_cell_mat))


    overall = time.time() - start
    print((tot / overall)*100,"%  ",overall)


    axs[0].plot(frequency_range, np.real(np.array(gammas)))
    # axs[0].plot(frequency_range, beta_unfold(np.imag(np.array(gammas))) - beta_unfold(np.imag(np.array(CL_gammas))))
    axs[0].plot(frequency_range, beta_unfold(np.imag(np.array(gammas))))
    axs[1].plot(frequency_range, np.real(np.array(ZBs)))
    axs[1].plot(frequency_range, np.imag(np.array(ZBs)))
    axs[1].set_ylim([-500, 500])
    plt.show()
