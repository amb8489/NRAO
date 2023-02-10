import math

import numpy as np

from transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL

"""


CPW MODEL FOR TRANSMISSION LINE


"""


class SuperConductingArtificialCPWLine(AbstractSCTL):

    def __init__(self, line_width, s_width, thickness, er, tand):
        pass

    def capacitance(self):
        pass

    # Zc
    def characteristic_impedance(self, Z, Y):
        pass

    # gamma
    def propagation_constant(self, L1, L2, C1, w):
        ww = w ** 2

        return 2 * np.arcsinh((math.sqrt(-C1 * ww * (-3 + C1 * L1 * ww) * (-2 * L1 - L2 + C1 * L1 * L2 * ww))) / 2)

    # this will need to be refactored to take some list of Zs to be made general
    def get_propagation_constant_characteristic_impedance(self, freq):
        propagation_constant = ...

        characteristic_impedance_Zc = ...

        return propagation_constant, characteristic_impedance_Zc
