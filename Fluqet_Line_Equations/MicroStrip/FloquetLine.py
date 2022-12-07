import cmath

import numpy as np

from Fluqet_Line_Equations.Abstract_Floquet_Line import AbstractFloquetLine
from Fluqet_Line_Equations.FloquetLineDimensions import FloquetLineDimensions
from Utills.Functions import MultMats
from Utills.Constants import PI
import time


class SuperConductingFloquetLine(AbstractFloquetLine):

    def __init__(self, unit_Cell_Len, D0, In_Order_loads_Widths, loaded_line_model, unloaded_line_model,
                 super_conductivity_model, width_unloaded, width_loaded, line_thickness, Jc):

        # ---------------------------- unit cell inputs
        self.unit_Cell_Len = unit_Cell_Len
        self.width_unloaded = width_unloaded
        self.width_loaded = width_loaded

        # model of FloquetLineDimensions dimensions
        self.FlLineDims = FloquetLineDimensions(unit_Cell_Len, D0, In_Order_loads_Widths, line_thickness)

        # ---------------------------- models of the MicroStripModel - one for an unloaded line , one for a loaded line
        self.loaded_line_model = loaded_line_model
        self.unloaded_line_model = unloaded_line_model

        # ---------------------------- model of the Super conductor
        self.super_conductivity_model = super_conductivity_model

        # used to unfolding beta
        self.region = 0
        self.PiMult = 0
        self.flipping = False
        self.looking = True
        self.ChoosePumpZoneA = 0
        self.ChoosePumpZoneB = 0
        self.findA = True
        self.bump = 0
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
        return np.arccosh((A + D) / 2)

    def Bloch_impedance_Zb(self, ABCD_mat):
        A = ABCD_mat[0][0]
        B = ABCD_mat[0][1]
        D = ABCD_mat[1][1]

        ADs2 = cmath.sqrt(pow(A + D, 2) - 4)
        B2 = 2 * B
        ADm = A - D

        # positive dir             # neg dir
        return [- (B2 / (ADm + ADs2)), - (B2 / (ADm - ADs2))]

    # todo this is Zb and not Zc?
    def RLGC(self, propagationConst, Zb):
        Z = propagationConst * Zb
        Y = propagationConst / Zb

        R = Z.real
        L = Z.imag

        G = Y.real
        C = Y.imag
        return R, L, G, C

    def Transmission(self):
        pass

    '''
     the calculation of a, b, b-unfolded, r, x
     '''

    def abrx(self, freq):
        # frequency cant be too low
        freq = max(freq, 1e9)

        # opt would be to store after first run all conductivity values for a given  freq rannge for a given  self.op_temp, self.critical_Temp, self.pn
        # calc surface impedence Zs for super conductor

        s = time.time()
        conductivity = self.super_conductivity_model.conductivity(freq)
        self.tot += time.time() - s

        zs = self.super_conductivity_model.Zs(freq, conductivity, self.FlLineDims.thickness)

        loaded_propagation, loaded_Zc = self.loaded_line_model.get_propagation_constant_characteristic_impedance(freq,
                                                                                                                 zs)
        Unloaded_propagation, Unloaded_Zc = self.unloaded_line_model.get_propagation_constant_characteristic_impedance(
            freq,
            zs)

        # making all the ABCD matrices for each subsection of unit cell

        abcd_mats = []
        for i in range(0, self.FlLineDims.number_of_loads * 2, 2):
            # unloaded_mat
            abcd_mats.append(self.ABCD_TL(Unloaded_Zc, Unloaded_propagation, self.FlLineDims.get_L_number(i)))
            # loaded_mat
            abcd_mats.append(self.ABCD_TL(loaded_Zc, loaded_propagation, self.FlLineDims.get_L_number(i + 1)))
        abcd_mats.append(
            self.ABCD_TL(Unloaded_Zc, Unloaded_propagation,
                    self.FlLineDims.get_L_number(self.FlLineDims.number_of_loads * 2)))

        # ---- ABCD FOR UNIT CELL  - abcd1 * abcd2 * abcd3 ... abcdN
        Unitcell_ABCD_Mat = MultMats(abcd_mats)

        # ---------------------------- calc bloch impedance and propagation const for unit cell

        ZB = self.Bloch_impedance_Zb(Unitcell_ABCD_Mat)[0]
        pb = self.Pd(Unitcell_ABCD_Mat)

        R, L, G, C = self.RLGC(pb, ZB)

        r = ZB.real
        x = ZB.imag
        a = pb.real
        bta = pb.imag

        # find good pump zone

        if self.findA and a > 0.0007:
            self.bump += 1

            if self.bump == 3:
                self.ChoosePumpZoneA = freq

            self.findA = False

        elif a < 0.001 and not self.findA:
            if self.bump == 3:
                self.ChoosePumpZoneB = freq

            self.findA = True

        # ------- un-folding beta
        unfoldedBeta = bta

        if self.looking and (unfoldedBeta <= 0.0000001 or unfoldedBeta >= PI):
            self.looking = False



        # on a slope
        else:
            if not self.looking and (unfoldedBeta > 0.0000001 and unfoldedBeta < PI):
                self.region += 1
                self.PiMult += PI
                self.flipping = not self.flipping
                self.looking = True

        if self.flipping:
            unfoldedBeta += 2 * abs(PI - unfoldedBeta) + (self.PiMult - PI)
        else:
            unfoldedBeta += self.PiMult

        return a, unfoldedBeta, bta, r, x, R, L, G, C
