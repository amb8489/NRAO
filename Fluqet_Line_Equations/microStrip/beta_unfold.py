import cmath
import time

import numpy as np

from Fluqet_Line_Equations.microStrip.Fluqet_line_equations import UnitCellABCD_mats, ABCD_TL
from Supports.constants import PI
from TransmissionLineEquations.microStrip.MicroStripModel import SuperConductingMicroStripModel


class calc_aplha_beta_r_x():

    def __init__(self,line):

        # todo add vars to init

        # ---------------------------- unit cell inputs
        self.d = 0.0023
        self.l1 = 5e-5
        # width of unloaded
        self.Wu = 1.49e-6
        self.A = 1.2
        self.B = 2
        # width of loads
        self.Wl = self.A * self.Wu

        # ---------------------------- sce inputs
        self.er = 10
        self.H = 2.5e-7
        self.ts = 6e-8
        self.tg = 3e-7
        self.Tc = 14.28
        self.pn = 1.008E-6
        self.tanD = 0

        self.op_temp = 0

        # ---------------------------- line dimensions

        self.Length1 = 0.5 * ((self.d / 3) - self.l1)
        self.length1 = self.l1
        self.length2 = self.l1
        self.Length2 = (self.d / 3) - 0.5 * (self.length1 + self.length2)
        self.length3 = 2 * self.length1
        self.Length3 = (self.d / 3) - 0.5 * (self.length2 + self.length3)
        self.Length4 = 0.5 * ((self.d / 3) - self.length3)

        # ---------------------------- models of SuperConductingMicroStripModel
        # ---------------------------- one for unloaded , one for loaded
        self.model_loaded = SuperConductingMicroStripModel(self.H, self.Wl, self.ts, self.er, self.tanD)
        self.model_unloaded = SuperConductingMicroStripModel(self.H, self.Wu, self.ts, self.er, self.tanD)

        # ------ globals for beta
        self.region = 0
        self.PiMult = 0
        self.flipping = False
        self.looking = True

        # error check tp make sure that beta is run in in increasing frequnces
        self.prev_beta_freq = -1

    def beta_unfolded(self, freq):
        freq = max(freq,1000)

        #todo fix this function so that these warning can go
        if freq < 1000:
            print("------WARNING ! freq under 1000 could result in beta being 1 PI too high  ----")
            exit(1)
        if freq < self.prev_beta_freq:
            print("------ERROR! need to reset calc_aplha_beta_r_x class before you can use to clac beta correctly-----")
            exit(1)


        self.prev_beta_freq = freq

        def Pd(mat):
            mat_A = mat[0][0]
            mat_D = mat[1][1]
            return np.arccosh((mat_A + mat_D) / 2)

        def Zb(mat):
            mat_A = mat[0][0]
            mat_B = mat[0][1]
            mat_D = mat[1][1]
            ADs2 = cmath.sqrt(pow(mat_A + mat_D, 2) - 4)
            B2 = 2 * mat_B
            ADm = mat_A - mat_D
            return [- (B2 / (ADm + ADs2)), - (B2 / (ADm - ADs2))]

        # s = time.time()

        # calc Zc for load and unloaded
        loaded_Zc = self.model_loaded.characteristic_impedance_auto(freq, self.op_temp, self.Tc, self.pn)
        Unloaded_Zc = self.model_unloaded.characteristic_impedance_auto(freq, self.op_temp, self.Tc, self.pn)

        # calc propagation const for loaded and unloaded
        loaded_propagation = self.model_loaded.propagation_constant_auto(freq, self.op_temp, self.Tc, self.pn)
        Unloaded_propagation = self.model_loaded.propagation_constant_auto(freq, self.op_temp, self.Tc, self.pn)

        # ------------- ABCD 1 -------------
        mat1 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, self.Length1)

        # ------------- ABCD 2 -------------
        mat2 = ABCD_TL(loaded_Zc, loaded_propagation, self.length1)

        # ------------- ABCD 3 -------------
        mat3 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, self.Length2)

        # ------------- ABCD 4 -------------
        mat4 = ABCD_TL(loaded_Zc, loaded_propagation, self.length2)

        # ------------- ABCD 5 -------------
        mat5 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, self.Length3)

        # ------------- ABCD 6 -------------
        mat6 = ABCD_TL(loaded_Zc, loaded_propagation, self.length3)

        # ------------- ABCD 7 -------------
        mat7 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, self.Length4)

        # ------------- ABCD UNIT CELL-------------
        ABCD_UC = UnitCellABCD_mats([mat1, mat2, mat3, mat4, mat5, mat6, mat7])

        # ---------------------------- calc bloch impedence and probagation const for UC
        ZB = Zb(ABCD_UC)[1]
        pb = Pd(ABCD_UC)

        bta = pb.imag

        # todo if we need a more general formulation of flat zones maybe calc min() / max() of beta also
        # todo if we need a more general formulation of flat zones just see when prev == current val could work or dist is within some delta thresh
        # todo could also do abs(beta) and do some translating
        b = bta
        bta = abs(bta)
        # at a top or bottom

        if self.looking and (bta <= 0.0000001 or bta >= PI):
            self.looking = False
        # on a slope
        else:
            if not self.looking and (bta > 0.0000001 and bta < PI):
                self.region += 1
                self.PiMult += PI
                self.flipping = not self.flipping
                self.looking = True

        if self.flipping:
            bta += 2 * abs(PI - bta) + (self.PiMult - PI)
        else:
            bta += self.PiMult

        # print(" time to unfold calc a b r x and unfold beta", time.time() - s)
        return bta, b
