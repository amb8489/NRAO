import cmath
import numpy as np
import scipy
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.Abstract_Floquet_Line import AbstractFloquetLine
from Fluqet_Line_Equations.FloquetLineDimensions import FloquetLineDimensions
from Utills.Functions import mult_mats
from Utills.Constants import PI, PI2
import time


class SuperConductingFloquetLine(AbstractFloquetLine):

    def __init__(self, unit_cell_length, D0, load_lengths, load_line_models, central_line_model,
                 super_conductivity_model, central_line_width, load_widths, line_thickness, crit_current):

        # ---------------------------- unit cell inputs
        self.unit_cell_length = unit_cell_length
        self.central_Line_width = central_line_width
        self.load_widths = load_widths

        # model of FloquetLineDimensions dimensions
        self.FlLineDims = FloquetLineDimensions(unit_cell_length, D0, load_lengths, line_thickness,
                                                load_line_models, central_line_model)

        # ---------------------------- model of the Super conductor
        self.super_conductivity_model = super_conductivity_model

        self.target_pump_zone_start = 0
        self.target_pump_zone_end = 0

        # debug info
        self.tot = 0

    '''

    equations needed for making ABCD matrices and ZB and gamma


    '''

    # ABCD matrix of TLs
    # Z characteristic impedance; k wavenumber; l length
    def ABCD_TL(self, Z, Gamma, L):
        GL = Gamma * L
        coshGL = cmath.cosh(GL)
        sinhGL = cmath.sinh(GL)

        return [[coshGL, Z * sinhGL],
                [(1 / Z) * sinhGL, coshGL]]

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
     the calculation of a, b, b-unfolded, r, x
     '''

    def FindPumpZone(self, alphas):

        harmonic_number_to_filter = 3

        a = np.array(alphas)
        peaks, _ = scipy.signal.find_peaks(alphas)

        if len(peaks) < harmonic_number_to_filter:
            return

        peak_widths = scipy.signal.peak_widths(alphas, peaks, rel_height=0.95)

        peak_widths = [[a[harmonic_number_to_filter]] for a in peak_widths]

        plt.plot(a)
        plt.plot(peaks[3], a[3], "x")
        plt.hlines(*peak_widths[1:], color="C2")
        plt.show()
        # todo finish finding the target_pump_zone_start and target_pump_zone_end

        self.target_pump_zone_start = peak_widths[0]
        self.target_pump_zone_end = peak_widths[0]
        print(self.target_pump_zone_start, self.target_pump_zone_end)

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

    def abrx(self, freq):
        # frequency cant be too low
        freq = max(freq, 1e9)

        # opt would be to store after first run all conductivity values for a given  freq rannge for a given  self.op_temp, self.critical_Temp, self.normal_resistivity
        # calc surface impedence Zs for super conductor

        s = time.time()
        conductivity = self.super_conductivity_model.conductivity(freq)
        self.tot += time.time() - s

        zs = self.super_conductivity_model.Zs(freq, conductivity, self.FlLineDims.thickness)

        # making all the ABCD matrices for each subsection of unit cell
        abcd_mats = []
        for unit_cell_segment_idx in range(0, self.FlLineDims.number_of_loads * 2 + 1):
            # abcd mat
            gamma, Zc = self.FlLineDims.get_gamma_Zc(unit_cell_segment_idx, freq, zs)
            abcd_mats.append(self.ABCD_TL(Zc, gamma, self.FlLineDims.get_segment_len(unit_cell_segment_idx)))

        # ---- ABCD FOR UNIT CELL  - abcd1 * abcd2 * abcd3 ... abcdN
        Unitcell_ABCD_Mat = mult_mats(abcd_mats)

        # ---------------------------- calc bloch impedance and propagation const for unit cell

        Bloch_impedance1, Bloch_impedance2 = self.Bloch_impedance_Zb(Unitcell_ABCD_Mat)
        propagation_const = self.Pd(Unitcell_ABCD_Mat)

        # calculate circuit factors
        R, L, G, C = self.RLGC(propagation_const, Bloch_impedance1)

        t = self.Transmission(100, 50, Bloch_impedance1, Bloch_impedance2, self.unit_cell_length, propagation_const)

        a = propagation_const.real
        bta = propagation_const.imag
        r = Bloch_impedance1.real
        x = Bloch_impedance1.imag

        # CentralLineMat = self.ABCD_TL(Unloaded_Zc, Unloaded_propagation,self.unit_cell_length)
        # a =  Unloaded_propagation.imag

        return a, t, bta, r, x, R, L, G, C
