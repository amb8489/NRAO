import cmath
from abc import ABC, abstractmethod

import numpy as np
from scipy.signal import find_peaks, peak_widths


# todo all need a simulate function... what else?

class floquet_abs(ABC):

    # sc transmissioin line outputs
    @abstractmethod
    def simulate_over_frequency_range(self, *args, **kwargs):
        '''

        :param args:
        :param kwargs:
        :returns:

        returns the outputs simulated over a given frequency range
        [
        floquetgamma_d : [],
        floquet_ZB: [],
        central_line_alpha: [],
        central_line_beta: [],
        floquet_transmission: []
        ]


        '''
        pass

    @abstractmethod
    def get_unit_cell_length(self):
        '''
        :return: the length of the unit cell in meters
        '''
        pass


class floquet_base():

    def bloch_impedance_Zb(self, ABCD_mat_2x2: [[float]]):
        A = ABCD_mat_2x2[0][0]
        B = ABCD_mat_2x2[0][1]
        D = ABCD_mat_2x2[1][1]

        ADs2 = cmath.sqrt(((A + D) ** 2) - 4)
        ADm = A - D

        B2 = 2 * B

        ZB = - (B2 / (ADm + ADs2))
        ZB2 = - (B2 / (ADm - ADs2))

        # todo test that this works
        return max(ZB, ZB2, key=lambda c: c.real)

    def gamma_d(self, ABCD_mat_2x2: [[float]]):
        A = ABCD_mat_2x2[0][0]
        D = ABCD_mat_2x2[1][1]
        return cmath.acosh(((A + D) / 2))

    def ABCD_Mat(self,zc, gamma, line_length):
        gl = gamma * line_length
        coshGL = cmath.cosh(gl)
        sinhGL = cmath.sinh(gl)

        return [[coshGL, zc * sinhGL],
                [(1 / zc) * sinhGL, coshGL]]
