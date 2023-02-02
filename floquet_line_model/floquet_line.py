import cmath

import numpy as np
from scipy.signal import find_peaks, peak_widths

from floquet_line_model.floquet_line_dimensions import UnitCellLineSegments
from utills.constants import PI, PI2
from utills.functions import mult_mats


class SuperConductingFloquetLine():

    def __init__(self, unit_cell_length, D0, load_lengths, load_line_models, central_line_model,
                 super_conductivity_model, central_line_width, load_widths, line_thickness, crit_current):

        # ---------------------------- unit cell inputs
        self.unit_cell_length = unit_cell_length
        self.central_Line_width = central_line_width
        self.load_widths = load_widths

        # model of the dimensions for the floquet line
        self.unit_cell_segments = UnitCellLineSegments(unit_cell_length, D0, load_lengths, central_line_model,
                                                       line_thickness, load_line_models)

        # ---------------------------- model of the Super conductor
        self.super_conductivity_model = super_conductivity_model

        self.target_pump_zone_start = 0
        self.target_pump_zone_end = 0

        # debug info
        self.tot = 0

    '''

    equations needed for making ABCD matrices and ZB and gamma


    '''


    def Pd(self, ABCD_mat):
        A = ABCD_mat[0][0]
        D = ABCD_mat[1][1]

        return np.arccosh(((A + D) / 2))

    def Bloch_impedance_Zb(self, ABCD_mat):
        A = ABCD_mat[0][0]
        B = ABCD_mat[0][1]
        D = ABCD_mat[1][1]

        ADs2 = cmath.sqrt(pow(A + D, 2) - 4)
        B2 = 2 * B
        ADm = A - D

        # positive dir             # neg dir
        return [- (B2 / (ADm + ADs2)), - (B2 / (ADm - ADs2))]

    def RLGC(self, propagationConst, Zb):
        Z = propagationConst * Zb
        Y = propagationConst / Zb

        R = Z.real
        L = Z.imag

        G = Y.real
        C = Y.imag
        return R, L, G, C

    def Transmission(self, Ncells, z0, zb1, zb2, Unit_Cell_Len, pb):

        return ((2 * cmath.exp(Unit_Cell_Len * Ncells * pb) * (zb1 - zb2) * z0) /
                ((1 + cmath.exp(2 * Unit_Cell_Len * Ncells * pb)) * (zb1 - zb2) * z0 -
                 (- 1 + cmath.exp(2 * Unit_Cell_Len * Ncells * pb)) * (zb1 * zb2 - (z0 ** 2))))

    '''
     the calculation of alpha_plt, b, b-unfolded, r, x
     '''

    def FindPumpZone(self, peak_number, alphas):

        x = np.array(alphas)
        peaks, _ = find_peaks(x, prominence=.005)

        if len(peaks) < peak_number:
            self.target_pump_zone_start, self.target_pump_zone_end = 0, 0
            return

        y, self.target_pump_zone_start, self.target_pump_zone_end = \
            list(zip(*peak_widths(x, peaks, rel_height=.95)[1:]))[max(peak_number - 1, 0)]

        # plt.axvspan(self.target_pump_zone_start, self.target_pump_zone_end, facecolor='r', alpha=0.5)
        # plt.axvspan(self.target_pump_zone_start // 3, self.target_pump_zone_end // 3, facecolor='g', alpha=0.5)
        # plt.plot(x)
        # plt.plot(betas)
        # plt.plot(peaks, x[peaks], "x")
        # plt.show()

    def unfold(self, betas):

        betas = np.abs(betas)
        prev_beta = 0
        scale_factor = -PI2
        should_flip = False
        res = []
        for b in betas:

            temp = b

            if b <= prev_beta:
                # REFLACTION OVER Y = PI
                b += 2 * (PI - b)

                if should_flip:
                    should_flip = not should_flip

            elif b > prev_beta:
                if not should_flip:
                    # TRANSLATE UP NO REFLECTION
                    scale_factor += PI2
                    should_flip = not should_flip

            res.append(b + scale_factor)

            prev_beta = temp

        return res

    def calc_factors(self, freq):
        # frequency cant be too low
        freq = max(freq, 1e9)

        # calculate Zs for given frequency and line thickness
        zs = self.super_conductivity_model.Zs(freq, self.super_conductivity_model.conductivity(freq),
                                              self.unit_cell_segments.thickness)

        # making all the ABCD matrices for each subsection line of unit cell
        abcd_mats = []
        for unit_cell_segment_idx in range(len(self.unit_cell_segments.floquet_line_segment_lengths)):

            abcd_mat = self.unit_cell_segments.get_segment_ABCD_mat(unit_cell_segment_idx, freq, zs)
            abcd_mats.append(abcd_mat)

        # matrix multiply all the abcd mats
        unit_cell_abcd_mat = mult_mats(abcd_mats)

        # calc bloch impedance and propagation const for unit cell
        bloch_impedance1, bloch_impedance2 = self.Bloch_impedance_Zb(unit_cell_abcd_mat)
        propagation_const = self.Pd(unit_cell_abcd_mat)


        # get alpha beta r x
        bta = propagation_const.imag
        alpha = propagation_const.real
        r = bloch_impedance1.real
        x = bloch_impedance1.imag

        # calculate circuit factors
        circuit_R, circuit_L, circuit_G, circuit_C = self.RLGC(propagation_const, bloch_impedance1)

        # calc transmission todo 100 50  v     v
        transmission = self.Transmission(100, 50, bloch_impedance1, bloch_impedance2, self.unit_cell_length,
                                         propagation_const)

        # CentralLineMat = self.ABCD_TL(Unloaded_Zc, Unloaded_propagation,self.unit_cell_length)
        # alpha_plt =  Unloaded_propagation.imag

        return alpha, transmission, bta, r, x, circuit_R, circuit_L, circuit_G, circuit_C
