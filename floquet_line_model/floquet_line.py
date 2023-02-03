import cmath

import numpy as np
from scipy.signal import find_peaks, peak_widths

from floquet_line_model.unit_cell import UnitCell, ABCD_Mat
from utills.constants import PI, PI2


def Bloch_impedance_Zb(ABCD_mat):
    A = ABCD_mat[0][0]
    B = ABCD_mat[0][1]
    D = ABCD_mat[1][1]

    ADs2 = cmath.sqrt(pow(A + D, 2) - 4)
    B2 = 2 * B
    ADm = A - D

    # positive dir             # neg dir
    return [- (B2 / (ADm + ADs2)), - (B2 / (ADm - ADs2))]


def Pd(ABCD_mat):
    A = ABCD_mat[0][0]
    D = ABCD_mat[1][1]

    return np.arccosh(((A + D) / 2))


def RLGC(propagationConst, Zb):
    Z = propagationConst * Zb
    Y = propagationConst / Zb

    R = Z.real
    L = Z.imag

    G = Y.real
    C = Y.imag
    return R, L, G, C


def Transmission(Ncells, z0, zb1, zb2, Unit_Cell_Len, pb):
    return ((2 * cmath.exp(Unit_Cell_Len * Ncells * pb) * (zb1 - zb2) * z0) /
            ((1 + cmath.exp(2 * Unit_Cell_Len * Ncells * pb)) * (zb1 - zb2) * z0 -
             (- 1 + cmath.exp(2 * Unit_Cell_Len * Ncells * pb)) * (zb1 * zb2 - (z0 ** 2))))


def unfold(betas):
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


class SuperConductingFloquetLine():

    def __init__(self, unit_cell_length, D0, load_lengths, load_line_models, central_line_model,
                 super_conductivity_model, central_line_width, load_widths, line_thickness, crit_current):
        # ---------------------------- model of the Super conductor

        self.super_conductivity_model = super_conductivity_model

        # ---------------------------- unit cell inputs
        self.central_Line_width = central_line_width

        # todo are these even being used in any calculations
        self.load_widths = load_widths
        print("-----> ", self.load_widths)

        # model of the dimensions for the floquet line
        self.unit_cell = UnitCell(unit_cell_length, D0, load_lengths, central_line_model,
                                  line_thickness, load_line_models)

        self.target_pump_zone_start = 0
        self.target_pump_zone_end = 0

        # debug info
        self.tot = 0

    def FindPumpZone(self, peak_number, alphas):
        x = np.array(alphas)
        peaks, _ = find_peaks(x, prominence=.005)

        if len(peaks) < peak_number:
            self.target_pump_zone_start, self.target_pump_zone_end = 0, 0
            return

        y, self.target_pump_zone_start, self.target_pump_zone_end = \
            list(zip(*peak_widths(x, peaks, rel_height=.95)[1:]))[max(peak_number - 1, 0)]

    def simulate(self, freq):
        # frequency cant be too low
        freq = max(freq, 1e7)

        # 1) calculate Zs
        conductivity = self.super_conductivity_model.conductivity(freq)

        # 2) calculate Zs for given frequency, conductivity ,line thickness
        zs = self.super_conductivity_model.Zs(freq, conductivity, self.unit_cell.thickness)

        # 5) get unit cell ABCD -- steps 3 - 4 inside get_unit_cell_ABCD_mat()
        unit_cell_abcd_mat = self.unit_cell.get_unit_cell_ABCD_mat(freq, zs)


        # 6) calculate all the needed outputs
        # calc bloch impedance and propagation const for unit cell
        bloch_impedance1, bloch_impedance2 = Bloch_impedance_Zb(unit_cell_abcd_mat)
        propagation_const = Pd(unit_cell_abcd_mat)

        # get alpha beta r x
        beta = propagation_const.imag
        alpha = propagation_const.real
        r = bloch_impedance1.real
        x = bloch_impedance1.imag

        # calculate circuit factors
        circuit_R, circuit_L, circuit_G, circuit_C = RLGC(propagation_const, bloch_impedance1)

        # calc transmission todo 100 50  v     v
        transmission = Transmission(100, 50, bloch_impedance1, bloch_impedance2, self.unit_cell.unit_cell_length,
                                    propagation_const)





        segment_gamma, segment_Zc = self.unit_cell.get_segment_gamma_Zc(0, freq, zs)
        CentralLineMat = ABCD_Mat(segment_Zc, segment_gamma, self.unit_cell.unit_cell_length)
        propagation_constcl = Pd(CentralLineMat)
        beta_cl = propagation_constcl.imag
        alpha_cl = propagation_constcl.real

        return alpha - alpha_cl, beta - beta_cl, r, x
