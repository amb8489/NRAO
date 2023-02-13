import numpy as np
import scipy.optimize as optimize
from scipy.constants import c

from transmission_line_models.artificial_cpw.artificial_cpw_capacitance import capacitance_model_selector
from utills.constants import C

"""


CPW MODEL FOR TRANSMISSION LINE


"""


class SuperConductingArtificialCPWLine:

    def __init__(self, finger_width, finger_length, finger_spacing, central_line_width, number_of_fingers,
                 ground_spacing):
        self.finger_width = finger_width
        self.finger_length = finger_length
        self.finger_spacing = finger_spacing
        self.central_line_width = central_line_width
        self.number_of_fingers = number_of_fingers
        self.ground_spacing = ground_spacing

    # step 1
    def dimension_to_circuit(self):
        pass

    # todo check
    def propagation_const(self, L1, L2, C1, omega):
        return 2 * np.arcsinh(
            1 / 2 * np.sqrt(
                -C1 * omega ** 2 * (-3 + C1 * L1 * omega ** 2) * (-2 * L1 - L2 + C1 * L1 * L2 * omega ** 2)))

    # todo check
    def characteristic_impedance(self, L1, L2, C1, omega):
        return (2j * omega * (-1 + C1 * L1 * omega ** 2) * (-L2 + L1 * (-2 + C1 * L2 * omega ** 2))) / (
                np.sqrt(-C1 * omega ** 2 * (-3 + C1 * L1 * omega ** 2) * (-L2 + L1 * (-2 + C1 * L2 * omega ** 2))) *
                np.sqrt(-(-1 + C1 * L1 * omega ** 2) * (
                        4 + C1 * omega ** 2 * (-3 * L2 + L1 * (-2 + C1 * L2 * omega ** 2)))))

    # todo check for correctness
    def cutoff_freq(self, L1, L2, C1):
        return np.min([np.sqrt(1 / (C1 * L1)),
                       optimize.root(lambda x: 4 + (-2 * C1 * L1 - 3 * C1 * L2) * x ** 2 + C1 ** 2 * L1 * L2 * x ** 4,
                                     3)])

    def Laprox(self, Zo, beta_so, l):
        return (Zo * beta_so * l) / C

    def capacitance(self, n, epsilon_r, sg, s1, gg, gendg, h, l, t, model_type=1):
        return capacitance_model_selector(model_type, n, epsilon_r, sg, s1, gg, gendg, h, l, t)

    # what is this --------VVVV

    def z_CapitalGamma_fcartificial(nfb, epsilon_r, s, wH, lH, wL, lL, h, t, fopr, model=1):
        sM = 0.5 * (wL - wH) + s
        lg = 0.5 * (wL - wH) - s
        delta_z = 3 * s + 2 * lL + lH

        Omega_opr = 2 * np.pi * fopr
        nf = 2 * nfb + 1
        zH = zwt(wH, s, t)
        zHpec = zwtpec(wH, s, t)
        beta_wtH = betawt(wH, s, t)
        beta_wtHpec = betawtpec(wH, s, t)
        LH = Laprox(zH, beta_wtH, lH)
        LHpec = Laprox(zHpec, beta_wtHpec, lH)
        zL = zwt(wL, s, t)
        zLpec = zwtpec(wL, s, t)
        beta_wtL = betawt(wL, s, t)
        beta_wtLpec = betawtpec(wL, s, t)
        LL = Laprox(zL, beta_wtL, lL)
        LLpec = Laprox(zLpec, beta_wtLpec, lL)
        zM = zwt(wH, sM, t)
        zMpec = zwtpec(wH, sM, t)
        beta_wtM = betawt(wH, sM, t)
        beta_wtMpec = betawtpec(wH, sM, t)
        LM = Laprox(zM, beta_wtM, s)
        LMpec = Laprox(zMpec, beta_wtMpec, s)

        cgap = CIDC(model, nf, epsilon_r, s / 2, s / 2, s / 2, 10 * s, h, lg, t)
        zart = Zoart12(LL + LM, LH + LM, 2 * cgap, Omega_opr)
        zartpec = Zoart12(LLpec + LMpec, LHpec + LMpec, 2 * cgap, Omega_opr)
        Gamma_art = Gamma_art12(LL + LM, LH + LM, 2 * cgap, Omega_opr)
        Gamma_artpec = Gamma_art12(LLpec + LMpec, LHpec + LMpec, 2 * cgap, Omega_opr)

        Gamma_art = Gamma_art / delta_z
        Gamma_artpec = Gamma_artpec / delta_z
        vart = Omega_opr / np.imag(Gamma_art)
        vartpec = Omega_opr / np.imag(Gamma_artpec)
        zv = np.real(zart) / vart
        zvpec = np.real(zartpec) / vartpec

        wcart = wcart12(LL + LM, LH + LM, 2 * cgap)

        return (zart, Gamma_art, vart / c, 1 - zvpec / zv, wcart / (2 * np.pi))

    def get_propagation_constant_characteristic_impedance(self, freq):
        propagation_constant = ...

        characteristic_impedance_Zc = ...

        return propagation_constant, characteristic_impedance_Zc
