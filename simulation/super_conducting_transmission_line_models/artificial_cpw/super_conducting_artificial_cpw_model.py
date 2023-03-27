import cmath
import math

import numpy as np
import scipy.special as sp

from simulation.super_conducting_transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.super_conducting_transmission_line_models.artificial_cpw.artificial_cpw_capacitance_models import \
    capacitance_model_selector
from simulation.utills.constants import BOLTZMANN_CONSTev, PLANCK_CONST_REDUCEDev, PI, MU_0, SPEED_OF_LIGHT, epsilon_0, \
    PI2

"""


Artificial CPW MODEL FOR TRANSMISSION LINE


"""


def DELTA_O(sc_crit_temp):
    return 1.764 * BOLTZMANN_CONSTev * sc_crit_temp


def lambda_0(sigma_n, delta_o):
    return math.sqrt(PLANCK_CONST_REDUCEDev / (PI * MU_0 * sigma_n * delta_o))


class SuperConductingArtificialCPWLine(AbstractSCTL):

    def __init__(self,
                 central_line_length_LH: float,
                 central_line_width_WH: float,
                 load_length_LL: float,
                 load_width_WL: float,
                 S: float,
                 number_of_finger_sections: int,
                 epsilon_r: float,
                 thickness: float,
                 height: float, super_conductivity_model,
                 total_line_length=None,
                 ):
        self.central_line_length_LH = central_line_length_LH
        self.central_line_width_WH = central_line_width_WH
        self.load_length_LL = load_length_LL
        self.load_width_WL = load_width_WL
        self.S = S
        self.number_of_finger_sections = number_of_finger_sections
        self.epsilon_r = epsilon_r
        self.thickness = thickness
        self.height = height
        self.nfb = number_of_finger_sections
        self.Lu = self.central_line_length_LH + S + load_length_LL + S

        self.total_line_length = self.Lu * number_of_finger_sections

        self.lambda_O = lambda_0(super_conductivity_model.get_sigma(), DELTA_O(super_conductivity_model.crit_temp))

        if total_line_length:

            self.number_of_finger_sections = total_line_length // self.Lu
            self.total_line_length = (total_line_length // self.Lu) * self.Lu

            if self.number_of_finger_sections < 1:
                raise Exception("Lu is greater than total line length")

        lg = ((self.load_width_WL - self.central_line_width_WH) / 2) - self.S

        nf = 2 * self.nfb + 1

        sM = ((self.load_width_WL - self.central_line_width_WH) / 2) + self.S

        self.delta_z = (3 * self.S) + (2 * self.load_length_LL) + self.central_line_length_LH

        self.L1, self.L2 = self.__clac_L1_L2(self.central_line_length_LH, self.load_length_LL, self.load_width_WL,
                                             self.central_line_width_WH,
                                             sM, self.S, self.thickness)

        self.capacitance = self.calc_capacitance(nf, epsilon_r, S / 2, S / 2, S / 2, 10 * S, height, lg, thickness,
                                                 model_type=1)

    def get_length(self):
        pass

    def get_width(self):
        pass

    def __L_aprox(self, Zo, beta_so, l):
        return Zo * beta_so * (l / SPEED_OF_LIGHT)

    def __clac_L1_L2(self, lH, lL: float, wL: float, wH: float, sM: float, s: float, t: float):

        zH = self.characteristic_impedance_SC_cpw(self.lambda_O, self.epsilon_r, wH, s, t)
        beta_wtH = self.propagation_const_SC_cpw(self.lambda_O, self.epsilon_r, wH, s, t)
        LH = self.__L_aprox(zH, beta_wtH, lH)

        zL = self.characteristic_impedance_SC_cpw(self.lambda_O, self.epsilon_r, wL, s, t)
        beta_wtL = self.propagation_const_SC_cpw(self.lambda_O, self.epsilon_r, wL, s, t)
        LL = self.__L_aprox(zL, beta_wtL, lL)

        zM = self.characteristic_impedance_SC_cpw(self.lambda_O, self.epsilon_r, wH, sM, t)
        beta_wtM = self.propagation_const_SC_cpw(self.lambda_O, self.epsilon_r, wH, sM, t)
        LM = self.__L_aprox(zM, beta_wtM, s)

        return LL + LM, LH + LM

    def Cg(self, epsilon_r, w, s):
        k = w / (w + 2 * s)
        epsilon_eff = (epsilon_r + 1) / 2
        KK1m = self.KK1(k)
        return 4 * epsilon_0 * epsilon_eff * KK1m

    def Lg(self, w, s):
        k = w / (w + 2 * s)
        KK1m = self.KK1(k)
        return (MU_0 / 4) * (1 / KK1m)

    def KK1(self, k):
        k1 = math.sqrt(1 - k ** 2)
        return self.nK(k) / self.nK(k1)

    def nK(self, k):
        return sp.ellipk(k ** 2)

    def gtot(self, w, s, t):
        k = w / (w + 2 * s)
        k12 = 1 - k ** 2
        K2 = self.nK(k) ** 2
        gc = (1 / (4 * k12 * K2)) * (PI + cmath.log((4 * PI * w) / t) - k * cmath.log((1 + k) / (1 - k)))
        gg = (k / (4 * k12 * K2)) * (
                PI + cmath.log((4 * PI * (w + 2 * s)) / t) - (1 / k) * cmath.log((1 + k) / (1 - k)))
        return gc + gg

    def LkCPW(self, Lk, w, s, t):
        return Lk * self.gtot(w, s, t)

    def Lkopr(self, lambda0, w, t):
        return MU_0 * (lambda0 ** 2) / (t * w)

    def characteristic_impedance_SC_cpw(self, lambda0, epsilon_r, w, s, tss):
        lk = self.Lkopr(lambda0, w, tss)
        Lkc = self.LkCPW(lk, w, s, tss)
        Lg_ = self.Lg(w, s)
        Cg_ = self.Cg(epsilon_r, w, s)

        Ltot = Lkc + Lg_
        return np.sqrt(Ltot / Cg_)

    def propagation_const_SC_cpw(self, lambda0, epsilon_r, w, s, tss):
        Lkc = self.LkCPW(self.Lkopr(lambda0, w, tss), w, s, tss)
        Lg_ = self.Lg(w, s)
        Cg_ = self.Cg(epsilon_r, w, s)
        Ltot = Lkc + Lg_
        return SPEED_OF_LIGHT * np.sqrt(Ltot * Cg_)

    def propagation_constant(self, L1: float, L2: float, capacitance: float, omega: float):

        omega_omega = omega ** 2
        return 2 * np.arcsinh(
            .5 * cmath.sqrt(-capacitance * omega_omega * (-3 + capacitance * L1 * omega_omega) * (
                    -2 * L1 - L2 + capacitance * L1 * L2 * omega_omega)))

    def characteristic_impedance(self, L1: float, L2: float, capacitance: float, omega: float):

        omega_omega = omega ** 2

        return (2j * omega * (-1 + capacitance * L1 * omega_omega) * (
                -L2 + L1 * (-2 + capacitance * L2 * omega_omega))) / (
                       cmath.sqrt(-capacitance * omega_omega * (-3 + capacitance * L1 * omega_omega) * (
                               -L2 + L1 * (-2 + capacitance * L2 * omega_omega))) *
                       cmath.sqrt(-(-1 + capacitance * L1 * omega_omega) * (
                               4 + capacitance * omega_omega * (-3 * L2 + L1 * (-2 + capacitance * L2 * omega_omega)))))

    def calc_capacitance(self, n, epsilon_r, sg, s1, gg, gendg, h: float, l: float, t: float, model_type: int = 1):
        return capacitance_model_selector(n, epsilon_r, sg, s1, gg, gendg, h, l, t, model_type=model_type)

    def get_gamma_Zc(self, frequency: float, zs: complex = None):

        propagation_constant = self.propagation_constant(self.L1, self.L2, 2 * self.capacitance, PI2 * frequency)

        characteristic_impedance_Zc = self.characteristic_impedance(self.L1, self.L2, 2 * self.capacitance,
                                                                    PI2 * frequency)

        return (propagation_constant / self.delta_z), characteristic_impedance_Zc
