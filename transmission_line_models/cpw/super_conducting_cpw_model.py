import math

import scipy

from transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from utills.constants import PI, MU_0, SPEED_OF_LIGHT, epsilono

"""

    cpw MODEL FOR TRANSMISSION LINE

    
    
"""


class SuperConductingCPWLine(AbstractSCTL):

    def __init__(self, central_line_width, s_width, thickness):
        self.central_line_width = central_line_width
        self.s_width = s_width
        self.thickness = thickness

    # geo factors ??
    def gtot(self, width, ground_spacing, thickness):
        k = width / (width + (2 * ground_spacing))

        k2 = self.nK(k) ** 2

        first = (1 / (4 * (1 - (k ** 2)) * k2))

        gc = first * (PI + math.log((4 * PI * width) / thickness) - k * math.log((1 + k) / (1 - k)))

        gg = (first * k) * (PI + math.log((4 * PI * (width + 2 * ground_spacing)) / thickness) - (1 / k) * math.log(
            (1 + k) / (1 - k)))

        return gc + gg

    def kinetic_inductance_CPW(self, lk, width, ground_spacing, thickness):
        return lk * self.gtot(width, ground_spacing, thickness)

    # todo what are the real name of the inputs
    def impedance_SC(self, Lkc, Lg, Cg):
        return math.sqrt((Lkc + Lg) / Cg)

    # todo what are the real name of the inputs
    def phase_velocity(self, Lkc, Lg, Cg):
        return math.sqrt(1 / ((Lkc + Lg) * Cg)) / SPEED_OF_LIGHT

    # todo what are the real name of the inputs and function
    def beta_ocpwsc(self, Lkc, Lg, Cg):
        return SPEED_OF_LIGHT * math.sqrt(((Lkc + Lg) * Cg))

    # todo what are the real name of the inputs and function
    def alpha_ocpwsc(self, Lkc, Lg):
        return Lkc / (Lkc + Lg)

    # -------------------------- PEC cpw ------------------------------

    #  elliptic integral redefined to contemplate Jochems change
    def nK(self, k):
        ncpw = 2
        return scipy.special.ellipk(k ** ncpw)

    def KK1(self, k):
        k1 = math.sqrt(1 - k ** 2)
        return self.nK(k) / self.nK(k1)

    # geometrical capacitance
    def Cg(self, er, width, ground_spacing):
        k = width / (width + 2 * ground_spacing)

        epsilon_eff = (er + 1) / 2

        KK1m = self.KK1(k)

        return 4 * epsilono * epsilon_eff * KK1m

    # geometrical inductance per unit length
    def Lg(self, width, ground_spacing):
        k = width / (width + 2 * ground_spacing)
        KK1m = self.KK1(k)

        # todo make sure this is MU_0
        return (MU_0 / 4) * (1 / KK1m)

    def impedance_PEC(self, er, width, ground_spacing):
        Lgm = self.Lg(width, ground_spacing)
        Cgm = self.Cg(er, width, ground_spacing)

        return math.sqrt(Lgm / Cgm)

    # todo
    # def G1(self, *args, **kwargs):
    #     pass
    #
    # def G2(self, *args, **kwargs):
    #     pass
    #
    # def series_impedance_Z(self, *args, **kwargs):
    #     pass
    #
    # def shunt_admittance_Y(self, *args, **kwargs):
    #     pass
    #
    # def characteristic_impedance(self, *args, **kwargs):
    #     pass
    #
    # def propagation_constant(self, *args, **kwargs):
    #     pass
    #
    # def get_propagation_constant_characteristic_impedance(self, *args, **kwargs):
    #     pass
