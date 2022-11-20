import cmath
import time
import numpy as np
from Fluqet_Line_Equations.microStrip.Fluqet_line_equations import UnitCellABCD_mats, ABCD_TL, Bloch_impedance_Zb, Pd
from SuperConductivityEquations.SCE import SuperConductivity
from Supports.constants import PI
from TransmissionLineEquations.microStrip.MicroStripModel import SuperConductingMicroStripModel


class SCFL_Model():

    def __init__(self, unit_Cell_Len, l1, width_unloaded, a, b, er, Height, line_thickness,
                 ground_thickness,
                 critical_Temp, pn, tanD, op_temp, Ic=None):

        # ---------------------------- unit cell inputs
        self.unit_Cell_Len = unit_Cell_Len
        self.width_unloaded = width_unloaded


        self.width_loaded = width_unloaded * a

        # ---------------------------- sce inputs
        self.er = er
        self.Height = Height
        self.line_thickness = line_thickness
        self.ground_thickness = ground_thickness
        self.critical_Temp = critical_Temp
        self.pn = pn
        self.tanD = tanD
        self.op_temp = op_temp

        # todo is there a wat to make this general
        # ---------------------------- line dimensions

        self.L1 = .5 * ((unit_Cell_Len / 3) - l1)
        self.L2 = l1
        self.L3 = (unit_Cell_Len / 3) - .5 * (l1 + l1)
        self.L4 = l1
        self.L5 = (unit_Cell_Len / 3) - .5 * (3 * l1)
        self.L6 = 2 * l1
        self.L7 = .5 * ((unit_Cell_Len / 3) - (3 * l1))

        # todo go back to old line from other paper

        # self.L1 = (D0 / 2) - (D1 / 2)
        # self.L2 = D1
        # self.L3 = D0 - D1
        # self.L4 = D1
        # self.L5 = D0 - (D1 / 2) - (D2 / 2)
        # self.L6 = D2
        # self.L7 = (D0 / 2) - (D2 / 2)

        if abs(self.L1 + self.L2 + self.L3 + self.L4 + self.L5 + self.L6 + self.L7 - unit_Cell_Len) > .0001:
            print("EROOR parts of unit cell are NOT adding to the whole unit cell lenght")

        # ---------------------------- models of SuperConductingMicroStripModel
        # ---------------------------- one for unloaded , one for loaded
        self.model_loaded = SuperConductingMicroStripModel(self.Height, self.width_loaded, self.line_thickness, self.er,
                                                           self.tanD)
        self.model_unloaded = SuperConductingMicroStripModel(self.Height, self.width_unloaded, self.line_thickness,
                                                             self.er, self.tanD)

        self.conductivity_model = SuperConductivity(op_temp, critical_Temp, pn)

        # ------ globals for beta for when freq starting at close to 0
        self.region = 0
        self.PiMult = 0
        self.flipping = False
        self.looking = True
        # error check tp make sure that beta is run in in increasing frequnces
        self.prev_beta_freq = -1

        self.prev = 0

        self.tot = 0

        # zs = Zs(1, conductivity(1, self.op_temp, self.critical_Temp, self.pn), self.line_thickness)

        # loaded_propagation, loaded_Zc = self.model_loaded.propagation_constant_characteristic_impedance(freq, zs)
        # Unloaded_propagation, Unloaded_Zc = self.model_unloaded.propagation_constant_characteristic_impedance(freq, zs)




    def beta_unfolded(self, freq):
        freq = max(freq, 1000)

        # # todo fix this function so that these warning can go
        # if freq < 1000:
        #     print("------WARNING ! freq under 1000 could result in beta being 1 PI too high  ----")
        #     exit(1)
        # if freq < self.prev_beta_freq:
        #     print("------ERROR! need to reset calc_aplha_beta_r_x class before you can use to clac beta correctly-----")
        #     exit(1)

        # self.prev_beta_freq = freq

        # calc Zc for load and unloaded

        # calc surface impedence

        # opt would be to store after first run all conductivity values for a given  freq rannge for a given  self.op_temp, self.critical_Temp, self.pn
        zs = self.conductivity_model.Zs(freq, self.conductivity_model.conductivity(freq), self.line_thickness)

        loaded_propagation, loaded_Zc = self.model_loaded.propagation_constant_characteristic_impedance(freq, zs)
        Unloaded_propagation, Unloaded_Zc = self.model_unloaded.propagation_constant_characteristic_impedance(freq, zs)

        # ------------- ABCD 1 -------------
        mat1 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, self.L1)

        # ------------- ABCD 2 -------------
        mat2 = ABCD_TL(loaded_Zc, loaded_propagation, self.L2)

        # ------------- ABCD 3 -------------
        mat3 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, self.L3)

        # ------------- ABCD 4 -------------
        mat4 = ABCD_TL(loaded_Zc, loaded_propagation, self.L4)

        # ------------- ABCD 5 -------------
        mat5 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, self.L5)

        # ------------- ABCD 6 -------------
        mat6 = ABCD_TL(loaded_Zc, loaded_propagation, self.L6)

        # ------------- ABCD 7 -------------
        mat7 = ABCD_TL(Unloaded_Zc, Unloaded_propagation, self.L7)

        # ------------- ABCD UNIT CELL-------------
        st = time.time()

        ABCD_UC = UnitCellABCD_mats([mat1, mat2, mat3, mat4, mat5, mat6, mat7])
        self.tot+= time.time()-st

        # ---------------------------- calc bloch impedance and propagation const for UC

        ZB = Bloch_impedance_Zb(ABCD_UC)[0]
        pb = Pd(ABCD_UC)

        r = ZB.real
        x = ZB.imag
        a = pb.real
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

        # todo renme bta to btaUnfolded and b to btafolded and return other a ,r ,x
        return a, bta, b, r, x
