import cmath
import math
from Utills.Functions import sech, coth
from Utills.Constants import PI, MU_0, PI2, PI4, PLANCK_CONST_REDUCEDev, K0, C, Z0, SPEED_OF_LIGHT
from TransmissionLineEquations.Abstract_SCTL import AbstractSCTL

"""

    MICRO STRIP MODEL FOR TRANSMISSION LINE
    
    
    NRAO

    Formulas from https://qucs.sourceforge.net/tech/node75.html#SECTION001211200000000000000

    Penetration depth <----where is this used ?
    Surface Impedance _ kautz "picoseconds pulses on super conducting strip lines"
        
        
    
    
"""


# todo somehwere i use 1/cos for arc cos not sure if thats right ....


class SuperConductingMicroStripModel(AbstractSCTL):

    def __init__(self, width, ground_spacing, thickness):
        self.width = width
        self.ground_spacing = ground_spacing
        self.thickness = thickness
    #todo
    def nK(self, k):
        pass

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
    def impedance(self, Lkc, Lg, Cg):
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

    def KK1(self, k):
        k1 = math.sqrt(1 - k ** 2)
        return self.nK(k) / self.nK(k1)

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
