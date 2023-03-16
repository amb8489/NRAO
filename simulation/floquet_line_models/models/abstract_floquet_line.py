import cmath
from abc import ABC, abstractmethod

import numpy as np
from scipy.signal import find_peaks, peak_widths


# todo all need a simulate function... what else?

class floquet_abs(ABC):

    # sc transmissioin line outputs
    @abstractmethod
    def simulate(self, *args, **kwargs):
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
        return max(ZB, ZB2,key = lambda c:c.real)

    def gamma_d(self, ABCD_mat_2x2: [[float]]):
        A = ABCD_mat_2x2[0][0]
        D = ABCD_mat_2x2[1][1]
        return cmath.acosh(((A + D) / 2))



    def FindPumpZone(self, peak_number: int, alphas: [float]):
        x = np.array(alphas)
        peaks, _ = find_peaks(x, prominence=.005)

        if len(peaks) < peak_number:
            self.target_pump_zone_start, self.target_pump_zone_end = 0, 0
            return

        y, self.target_pump_zone_start, self.target_pump_zone_end = \
            list(zip(*peak_widths(x, peaks, rel_height=.95)[1:]))[max(peak_number - 1, 0)]
