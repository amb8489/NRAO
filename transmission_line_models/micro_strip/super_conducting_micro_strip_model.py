import cmath

import numpy as np
from scipy.constants import c

from transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from utills.constants import K0, Z0, PI

"""
    MICRO STRIP MODEL FOR TRANSMISSION LINE


    Formulas from https://qucs.sourceforge.net/tech/node75.html#SECTION001211200000000000000


"""


#
# class SuperConductingMicroStripModel(AbstractSCTL):
#
#     def __init__(self, height, width, thickness, epsilon_r, tan_delta, crit_current):
#
#         self.height = height
#         self.width = width
#         self.thickness = thickness
#         self.epsilon_r = epsilon_r
#         self.tan_delta = tan_delta
#
#         self.ic = thickness * width * crit_current
#
#         # calc geometric factors
#         self.g1 = self.G1(self.width, self.height, self.thickness)
#         self.g2 = self.G2(self.width, self.height, self.thickness)
#
#         # calc dialectic constant
#         self.epsilon_fm = self.epsilon_effst(self.epsilon_r, self.width, self.height, self.thickness)
#
#     # ----------  schneider   thickness = 0  ----------
#     def Fs(self, w, h):
#
#         return cmath.sqrt(1 + (10 * (h / w)))
#
#     def epsilon_effs(self, epsilon_r, w, h):
#
#         return ((epsilon_r + 1) / 2) + ((epsilon_r - 1) / (2 * self.Fs(w, h)))
#
#     def zmss(self, epsilon_r, w, h):
#
#         z0eff = Z0 / (math.sqrt(self.epsilon_effs(epsilon_r, w, h)))
#
#         if w / h <= 1:
#             return z0eff * (1 / PI2) * math.log(((8 * h) / w) + (w / (4 * h)))
#
#         return z0eff / ((w / h) + 2.42 - (0.44 * (h / w)) + pow(1 - (h / w), 6))
#
#     # ----------  schneider   thickness > 0  ----------
#
#     def epsilon_effst(self, epsilon_r, w, h, thickness):
#
#         # return ((epsilon_r+1)/2) + ((epsilon_r-1)/2)*(1/(math.sqrt(1+12*(h/w))))
#
#         u = w / h
#         if u <= (1 / PI2):
#             delta_w = (thickness / PI) * (1 + math.log((PI4 * w) / thickness))
#         else:
#             delta_w = (thickness / PI) * (1 + math.log((2 * h) / thickness))
#
#         return self.epsilon_effs(epsilon_r, w + delta_w, h)
#
#     def zmsst(self, epsilon_r, w, h, thickness):
#         u = w / h
#
#         if u <= (1 / PI2):
#             delta_w = (thickness / PI) * (1 + math.log((PI4 * w) / thickness))
#         else:
#             delta_w = (thickness / PI) * (1 + math.log((2 * h) / thickness))
#
#         return self.zmss(epsilon_r, w + delta_w, h)
#
#     # ----------  Hammerstad   thickness = 0  ----------
#
#     def epsilon_effh(self, epsilon_r, w, h):
#         u = w / h
#
#         u4 = pow(u, 4)
#
#         firstLog = math.log((u4 + pow(u / 52, 2)) / (u4 + 0.432))
#         secondLog = math.log(1 + pow(u / 18.1, 3))
#
#         a = 1 + (1 / 49) * firstLog + (1 / 18.7) * secondLog
#
#         b = 0.564 * pow((epsilon_r - .9) / (epsilon_r + 3), 0.053)
#
#         return ((epsilon_r + 1) / 2) + ((epsilon_r - 1) / 2) * pow(1 + (10 / u), -a * b)
#
#     def ZL1(self, w, h):
#         u = w / h
#
#         fu = 6 + (PI2 - 6) * math.exp(-pow(30.666 / u, 0.7528))
#
#         return (Z0 / PI2) * math.log((fu / u) + math.sqrt(1 + pow(2 / u, 2)))
#
#     # ----------  Hammerstad   thickness > 0  ----------
#
#     def delta_wr(self, epsilon_r, w, h, thickness):
#         return (self.delta_w1(w, h, thickness) * (1 + sech(math.sqrt(epsilon_r - 1)))) / 2
#
#     def delta_w1(self, w, h, thickness):
#         u = w / h
#         th = thickness / h
#
#         upper = 4 * math.e
#         lower = th * pow(coth(math.sqrt(6.517 * u)), 2)
#
#         return (thickness / PI) * math.log(1 + (upper / lower))
#
#     def epsilon_effht(self, epsilon_r, w, h, thickness):
#         w1 = w + self.delta_w1(w, h, thickness)
#         wr = w + self.delta_wr(epsilon_r, w, h, thickness)
#
#         zl1_up = self.ZL1(w1, h)
#         zl1_low = self.ZL1(wr, h)
#         return self.epsilon_effh(epsilon_r, wr, h) * pow(zl1_up / zl1_low, 2)
#
#     def Zmsht(self, epsilon_r, w, h, thickness):
#         wr = w + self.delta_wr(epsilon_r, w, h, thickness)
#         upper = self.ZL1(wr, h)
#         lower = math.sqrt(self.epsilon_effht(epsilon_r, wr, h, thickness))
#
#         return upper / lower
#
#     # -------------------
#
#     def Lambda0(self, sigma, delta_o):
#
#         # AND sigma_N is 1/ Pn
#         return math.sqrt(PLANCK_CONST_REDUCEDev / (PI * MU_0 * sigma * delta_o))
#
#     def z_slow(self, f, yO, thickness):
#         return 1j * PI2 * f * MU_0 * yO
#
#     def Lambda(self, surface_impedance, f, thickness):
#         return (surface_impedance / (PI2 * f * MU_0)).imag
#
#     """
#
#
#
#
#
#                     super conducting trans line equations for miro strip
#
#              Implementation of the paper of Yassin
#              Electromagnetic models for superconducting millimetre-wave and
#              sub-milLimetre-wave microstrip transmission_plt lines
#     """
#
#     # ------ helper functions ----------
#     # checked
#     def ra(self, w, h, p):
#         sqrtP = math.sqrt(p)
#
#         return cmath.exp(
#             -1 - ((PI * w) / (2 * h)) - ((p + 1) / sqrtP) * cmath.atanh(1 / sqrtP) - cmath.log((p - 1) / (4 * p)))
#
#     # checked
#     def rb(self, w, h, rbo, p):
#         if w / h >= 5:
#             return rbo
#
#         sqrtP = math.sqrt(p)
#         return rbo - math.sqrt((rbo - 1) * (rbo - p)) + (p + 1) * math.atanh(
#             math.sqrt((rbo - p) / (rbo - 1))) - 2 * sqrtP * math.atanh((rbo - p) / (p * (rbo - 1))) + (
#                        (PI * w) / (2 * h)) * sqrtP
#
#     # checked
#     def Eta(self, w, h, p):
#         sqrtP = math.sqrt(p)
#
#         return sqrtP * (((PI * w) / (2 * h)) + ((p + 1) / (2 * sqrtP)) * (1 + math.log(4 / (p - 1))) - 2 * math.atanh(
#             1 / sqrtP))
#
#     # checked
#     def b(self, h, thickness):
#         return 1 + (thickness / h)
#
#     # checked
#     def p(self, b):
#
#         bsqrd = b ** 2
#
#         return 2 * bsqrd - 1 + (2 * b * math.sqrt(bsqrd - 1))
#
#     # checked
#     def rbo(self, eta, p, deta_y):
#         return eta + ((p + 1) / 2) * math.log(deta_y)
#
#     # checked
#
#     def DeltaY(self, eta, p):
#
#         return max(eta, p)
#
#     # checked
#     def Kl(self, w, h, thickness):
#         return self.Chi(w, h, thickness) / self.Kf(w, h, thickness)
#
#     # checkd
#     def Kf(self, w, h, thickness):
#
#         bc = self.b(h, thickness)
#
#         pc = self.p(bc)
#
#         rac = self.ra(w, h, pc)
#
#         EtaC = self.Eta(w, h, pc)
#
#         DeltaYC = self.DeltaY(EtaC, pc)
#
#         rboc = self.rbo(EtaC, pc, DeltaYC)
#
#         rbc = self.rb(w, h, rboc, pc)
#
#         return (h / w) * (2 / PI) * cmath.log((2 * rbc) / rac)
#
#     # Functions to calculate Chi all checked
#     def Is1(self, p, ra, Ra):
#         return cmath.log((2 * p - (p + 1) * ra + 2 * cmath.sqrt(p * Ra)) / (ra * (p - 1)))
#
#     def Ra(self, p, ra):
#         return (1 - ra) * (p - ra)
#
#     def Is2(self, p, rb, Rb):
#         return - math.log(((p + 1) * rb - 2 * p - 2 * math.sqrt(p * Rb)) / (rb * (p - 1)))
#
#     def Rb(self, p, rb):
#         return (rb - 1) * (rb - p)
#
#     def Ig1(self, p, rb, Rb1):
#         return -cmath.log(((p + 1) * rb + 2 * p + 2 * cmath.sqrt(p * Rb1)) / (rb * (p - 1)))
#
#     def Rb1(self, p, rb):
#         return (rb + 1) * (rb + p)
#
#     def Ig2(self, p, ra, Ra1):
#         return cmath.log(((p + 1) * ra + 2 * p + 2 * cmath.sqrt(p * Ra1)) / (ra * (p - 1)))
#
#     def Ra1(self, p, ra):
#         return (ra + 1) * (ra + p)
#
#     # checked
#     def Chi(self, w, h, thickness):
#         bc = self.b(h, thickness)
#         pc = self.p(bc)
#         rac = self.ra(w, h, pc)
#         EtaC = self.Eta(w, h, pc)
#         DeltaYC = self.DeltaY(EtaC, pc)
#         rboc = self.rbo(EtaC, pc, DeltaYC)
#         rbc = self.rb(w, h, rboc, pc)
#         Rac = self.Ra(pc, rac)
#         Is1c = self.Is1(pc, rac, Rac)
#         Rbc = self.Rb(pc, rbc)
#         Is2c = self.Is2(pc, rbc, Rbc)
#         Rb1c = self.Ra(pc, rbc)
#         Ig1c = self.Ig1(pc, rbc, Rb1c)
#         Ra1c = self.Ra(pc, rac)
#         Ig2c = self.Ig2(pc, rac, Ra1c)
#
#         if (w / h) < 2:
#             return (Is1c + Is2c + Ig1c + Ig2c + PI) / (2 * cmath.log(rbc / rac))
#         return (Is1c + Is2c + Ig1c + Ig2c + PI) / (2 * cmath.log(2 * rbc / rac))
#
#     # An important expression for calculating impedance and complex propagation constant
#     # defined in this way mainly to calculate tan_Delta from Alpha
#     # checked
#     def X(self, surface_impedance, f, w, h, ts):
#
#         ChiC = self.Chi(w, h, ts)
#         ko = (PI2 * f) / C
#         return (2 * ChiC * surface_impedance) / (ko * Z0 * h)
#
#     # Superconducting impedance of the microstrip
#     # Note that in this version I have used the suface impedance as parameter
#     # Surface impedance can be determined with functions Zs and Zslow
#     # zt is the fucntion to determine the PCE microstip impedance
#     # checkd
#     def ZSy(self, zt, surface_impedance, f, epsilon_r, w, H, ts):
#         zmst = zt(epsilon_r, w, H, ts)
#         return zmst * (cmath.sqrt(1 - 1j * self.X(surface_impedance, f, w, H, ts))).real
#
#     # Superconducting wavenumber Beta_S / ko
#     # It requires the model for the PCE stripline
#     # Schneider --> Epsilon_effst, Hammerstad --> Epsilon_effht
#     # checked
#     def beta_Soy(self, est, surface_impedance, f, epsilon_r, w, H, ts):
#         epsilon_fm = est(epsilon_r, w, H, ts)
#         return cmath.sqrt(epsilon_fm) * (cmath.sqrt(1 - 1j * self.X(surface_impedance, f, w, H, ts))).real
#
#     # Superconducting attenuation Alpha_S ko
#     # It requires the model for the PCE stripline
#     # Schneider --> Epsilon_effst, Hammerstad --> Epsilon_effht
#     # checked
#     def aplha_Sy(self, est, surface_impedance, f, epsilon_r, w, H, ts):
#         epsilon_fm = est(epsilon_r, w, H, ts)
#         return - cmath.sqrt(epsilon_fm) * (cmath.sqrt(1 - 1j * self.X(surface_impedance, f, w, H, ts))).imag
#
#     # Fraction of kinetic inductance
#     # checked
#     def apha_ky(self, surface_impedance, f, w, H, ts):
#         CF = (cmath.sqrt(1 - 1j * self.X(surface_impedance, f, w, H, ts))).real
#         return 1 - (1 / CF ** 2)
#
#     def I_star(self, surface_impedance, f, w, H, ts):
#         return self.ic / math.sqrt(self.apha_ky(surface_impedance, f, w, H, ts))
#
#     # Phase velocity respect to vo = C
#     # checked
#     def vSy(self, est, surface_impedance, f, epsilon_r, w, H, ts):
#         epsilon_fm = est(epsilon_r, w, H, ts)
#         CF = (cmath.sqrt(1 - 1j * self.X(surface_impedance, f, w, H, ts))).real
#         return 1 / (math.sqrt(epsilon_fm) * CF)
#
#     # Including losses
#     # Superconducting wave number Beta_S / ko
#     # It requires the model for the PCE stripline
#     # Schneider --> Epsilon_effst, Hammerstad --> Epsilon_effht
#     # checked
#
#     def Beta_Syloss(self, est, surface_impedance, f, epsilon_r, tan_d, w, H, ts):
#         epsilon_fm = est(epsilon_r, w, H, ts)
#
#         epsilon_t = epsilon_fm - 1j * epsilon_r * tan_d
#
#         return (cmath.sqrt(epsilon_t) * cmath.sqrt(1 - 1j * self.X(surface_impedance, f, w, H, ts))).real
#
#     # Attenuation AlphaS / ko due to superconducting strip (negligible) and dielectric
#     # It requires the model for the PCE stripline
#     # Schneider --> Epsilon_effst, Hammerstad --> Epsilon_effht
#
#     # checked
#     def AlphaSyloss(self, est, surface_impedance, f, epsilon_r, tan_d, w, H, ts):
#         epsilon_fm = est(epsilon_r, w, H, ts)
#
#         epsilon_t = epsilon_fm - 1j * epsilon_r * tan_d
#
#         return -(cmath.sqrt(epsilon_t) * cmath.sqrt(1 - 1j * self.X(surface_impedance, f, w, H, ts))).imag
#
#     # ------------------  OUTPUTS ------------------
#
#     # todo should we swap these to JAVIER paper Geometrical factors
#     def G1(self, w, h, thickness):
#         return h / (w * self.Kf(w, h, thickness))
#
#     def G2(self, w, h, thickness):
#         return self.Kl(w, h, thickness) / w
#
#     """
#     series impedance of alpha_plt TEM transmission_plt line
#     ko is the free-space wavenumber
#     No is the impedance of free space
#     Zs, is the surface impedance of the conductors
#     g1 and g2 are geometrical factors, which characterize the particular transmission_plt line being used.
#     """
#
#     def series_impedance_Z(self, Zs, g1, g2, f):
#         return (1j * (K0(f) * Z0) * g1) + (2 * g2 * Zs)
#
#     """
#     shunt admittance of alpha_plt TEM transmission_plt line
#     ko is the free-space wavenumber
#     No is the impedance of free space
#     epsilon_fm the effective dielectric constant -- in the modal sense.
#     g1 is alpha_plt geometrical factor, which characterize the particular transmission_plt line being used.
#     """
#
#     def shunt_admittance_Y(self, epsilon_fm, g1, f):
#         return 1j * (K0(f) / Z0) * (epsilon_fm / g1)
#
#     # Zc
#     def characteristic_impedance(self, Z, Y):
#         return cmath.sqrt(Z / Y)
#
#     def propagation_constant(self, Z, Y):
#         return cmath.sqrt(Z * Y)
#
#     def get_propagation_constant_characteristic_impedance(self, frequency, surface_impedance):
#
#         Z = self.series_impedance_Z(surface_impedance, self.g1, self.g2, frequency)
#         Y = self.shunt_admittance_Y(self.epsilon_fm, self.g1, frequency)
#
#         propagation_constant = self.propagation_constant(Z, Y)
#         characteristic_impedance_Zc = self.characteristic_impedance(Z, Y)
#         return propagation_constant, characteristic_impedance_Zc


# ------------------------ JAVIER Paper model

class SuperConductingMicroStripModel(AbstractSCTL):

    def __init__(self, height, width, thickness, epsilon_r, tan_delta, crit_current):
        self.sc_height = height
        self.sc_width = width
        self.sc_thickness = thickness
        self.epsilon_r = epsilon_r
        self.tan_delta = tan_delta

        # calc geometric factors
        self.g1 = self.__G1(self.sc_width, self.sc_height, self.sc_thickness)
        self.g2 = self.__G2(self.sc_width, self.sc_height, self.sc_thickness, self.g1)

    def __G1(self, sc_width, sc_height, sc_thickness):
        b = 1 + (sc_thickness / sc_height)
        p = 2 * (b ** 2) - 1 + (2 * b) * cmath.sqrt((b ** 2) - 1)

        Lambda = cmath.sqrt(p) * (((PI * sc_width) / (2 * sc_height)) + ((p + 1) / (2 * cmath.sqrt(p))) * (
                1 + cmath.log(4 / (p - 1))) - 2 * np.arctanh(1 / cmath.sqrt(p)))

        Gamma = max(Lambda, p)

        rbo1 = Lambda + ((p + 1) / 2) * cmath.log(Gamma)

        rbo2 = (rbo1 - cmath.sqrt((rbo1 - 1) * (rbo1 - p)) + (p + 1) * np.arctanh(
            cmath.sqrt((rbo1 - p) / (rbo1 - 1))) - 2 * cmath.sqrt(p) * np.arctanh(
            cmath.sqrt((rbo1 - p) / (p * (rbo1 - 1))))
                + ((PI * sc_width) / (2 * sc_height)) * cmath.sqrt(p))

        ra = -1 - ((PI * sc_width) / (2 * sc_height)) - ((p + 1) / cmath.sqrt(p)) * np.arctanh(
            1 / cmath.sqrt(p)) - cmath.log((p - 1) / (4 * p))

        rb = rbo1 if sc_width / sc_height >= 5 else rbo2

        return (PI / 2) * (1 / (cmath.log((2 * rb) / ra)))

    def __G2(self, sc_width, sc_height, sc_thickness, g1):
        b = 1 + (sc_thickness / sc_height)
        p = 2 * (b ** 2) - 1 + (2 * b) * cmath.sqrt((b ** 2) - 1)

        Lambda = cmath.sqrt(p) * (((PI * sc_width) / (2 * sc_height)) + ((p + 1) / (2 * cmath.sqrt(p))) * (
                1 + cmath.log(4 / (p - 1))) - 2 * np.arctanh(1 / cmath.sqrt(p)))

        Gamma = max(Lambda, p)

        rbo1 = Lambda + ((p + 1) / 2) * cmath.log(Gamma)

        rbo2 = (rbo1 - cmath.sqrt((rbo1 - 1) * (rbo1 - p)) + (p + 1) * np.arctanh(
            cmath.sqrt((rbo1 - p) / (rbo1 - 1))) - 2 * cmath.sqrt(p) * np.arctanh(
            cmath.sqrt((rbo1 - p) / (p * (rbo1 - 1))))
                + ((PI * sc_width) / (2 * sc_height)) * cmath.sqrt(p))

        ra = -1 - ((PI * sc_width) / (2 * sc_height)) - ((p + 1) / cmath.sqrt(p)) * np.arctanh(
            1 / cmath.sqrt(p)) - cmath.log((p - 1) / (4 * p))

        rb = rbo1 if sc_width / sc_height >= 5 else rbo2

        if sc_width / sc_height < 2:
            K_ms = (2 * sc_height * cmath.log(rb / ra))
        else:
            K_ms = (2 * sc_height * cmath.log((2 * rb) / ra))

        I = cmath.log(((2 * p) + 2 * cmath.sqrt(p * (1 - ra) * (p - ra)) - (p + 1) * ra) / (ra * (p - 1)))

        return g1 * (1 / K_ms) * (I + (PI / 2))

    # --------------------------------------------------------------------------------------------------------------
    def efm(self, frequency, er, tand, sc_height, sc_width):
        F1Freq = ((4 * sc_height * frequency) / c) * cmath.sqrt(er - 1) * \
                 (.5 + (1 + 2 * cmath.log(1 + (sc_width / sc_height))) ** 2)

        ep_s = ((er + 1) / 2) + ((er - 1) / (2 * cmath.sqrt(1 + (12 * (sc_height / sc_width)))))

        ep_v = (((cmath.sqrt(er) - cmath.sqrt(ep_s)) / (1 + 4 * (F1Freq ** -1.5))) + cmath.sqrt(ep_s)) ** 2

        return ep_v * (1 - (1j * tand))

    def series_impedance_Z(self, Zs, g1, g2, f):
        return (1j * (K0(f) * Z0) * g1) + (2 * g2 * Zs)

    def shunt_admittance_Y(self, g1, f, er, tand, sc_hight, sc_width):
        return 1j * (K0(f) / Z0) * (self.efm(f, er, tand, sc_hight, sc_width) / g1)

    def characteristic_impedance(self, Z, Y):
        return cmath.sqrt(Z / Y)

    def propagation_constant(self, Z, Y):
        return cmath.sqrt(Z * Y)

    def get_propagation_constant_characteristic_impedance(self, frequency, surface_impedance):
        Z = self.series_impedance_Z(surface_impedance, self.g1, self.g2, frequency)
        Y = self.shunt_admittance_Y(self.g1, frequency, self.epsilon_r, self.tan_delta, self.sc_height, self.sc_width)

        propagation_constant = self.propagation_constant(Z, Y)
        characteristic_impedance_Zc = self.characteristic_impedance(Z, Y)
        return propagation_constant, characteristic_impedance_Zc
