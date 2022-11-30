import cmath
import time
import numpy as np

from Fluqet_Line_Equations.Line import Line
from Fluqet_Line_Equations.microStrip.Fluqet_line_equations import MultMats, ABCD_TL, Bloch_impedance_Zb, Pd
from SuperConductivityEquations.SCE import SuperConductivity
from Supports.constants import PI
from TransmissionLineEquations.microStrip.MicroStripModel import SuperConductingMicroStripModel


class SCFL_Model():

    def __init__(self, unit_Cell_Len, l1, width_unloaded, a, b, er, Height, line_thickness,
                 ground_thickness,
                 critical_Temp, pn, tanD, op_temp, Jc,numberOfLoads = 3):

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

        # ---------------------------- line dimensions


        # #todo generlize this
        self.L1 = .5 * ((unit_Cell_Len / 3) - l1)
        self.L2 = l1
        self.L3 = (unit_Cell_Len / 3) - .5 * (l1 + l1)
        self.L4 = l1
        self.L5 = (unit_Cell_Len / 3) - .5 * (3 * l1)
        self.L6 = 2 * l1
        self.L7 = .5 * ((unit_Cell_Len / 3) - (3 * l1))

        # L = Line(D, D0, number_of_loads, In_Order_loads_Widths)

        if abs(self.L1 + self.L2 + self.L3 + self.L4 + self.L5 + self.L6 + self.L7 - unit_Cell_Len) > .0001:
            print("EROOR parts of unit cell are NOT adding to the whole unit cell lenght")

        # ---------------------------- models of SuperConductingMicroStripModel
        # ---------------------------- one for unloaded , one for loaded

        self.model_loaded = SuperConductingMicroStripModel(self.Height, self.width_loaded, self.line_thickness, self.er,
                                                           self.tanD, Jc)
        self.model_unloaded = SuperConductingMicroStripModel(self.Height, self.width_unloaded, self.line_thickness,
                                                             self.er, self.tanD, Jc)
        self.conductivity_model = SuperConductivity(op_temp, critical_Temp, pn)

        # ------ globals for beta for when freq starting at close to 0
        self.region = 0
        self.PiMult = 0
        self.flipping = False
        self.looking = True
        self.tot = 0


    def abrx(self, freq):
        freq = max(freq, 1000)


        # calc surface impedence
        st = time.time()
        # opt would be to store after first run all conductivity values for a given  freq rannge for a given  self.op_temp, self.critical_Temp, self.pn
        zs = self.conductivity_model.Zs(freq, self.conductivity_model.conductivity(freq), self.line_thickness)
        self.tot += time.time() - st


        loaded_propagation, loaded_Zc = self.model_loaded.propagation_constant_characteristic_impedance(freq, zs)
        Unloaded_propagation, Unloaded_Zc = self.model_unloaded.propagation_constant_characteristic_impedance(freq, zs)


        # cental line

        # CL = ABCD_TL(Unloaded_Zc, Unloaded_propagation, self.unit_Cell_Len)

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

        ABCD_Mat = MultMats([mat1, mat2, mat3, mat4, mat5, mat6, mat7])

        # ---------------------------- calc bloch impedance and propagation const for UC

        ZB = Bloch_impedance_Zb(ABCD_Mat)[0]
        pb = Pd(ABCD_Mat)

        r = ZB.real
        x = ZB.imag
        a = pb.real
        bta = pb.imag

        #
        # # todo if we need a more general formulation of flat zones maybe calc min() / max() of beta also
        #         # todo if we need a more general formulation of flat zones just see when prev == current val could work or dist is within some delta thresh
        #         # todo could also do abs(beta) and do some translating

        unfolded = bta

        if self.looking and (unfolded <= 0.0000001 or unfolded >= PI):
            self.looking = False
        # on a slope
        else:
            if not self.looking and (unfolded > 0.0000001 and unfolded < PI):
                self.region += 1
                self.PiMult += PI
                self.flipping = not self.flipping
                self.looking = True

        if self.flipping:
            unfolded += 2 * abs(PI - unfolded) + (self.PiMult - PI)
        else:
            unfolded += self.PiMult

        #         # todo renme bta to btaUnfolded and b to btafolded and return other a ,r ,x

        return a, bta,unfolded, r, x

    def unfold(self, data):

        pass
