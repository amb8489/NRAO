from Fluqet_Line_Equations.Line import Line
from Fluqet_Line_Equations.microStrip.Fluqet_line_equations import ABCD_TL, Bloch_impedance_Zb, Pd
from SuperConductivityEquations.SCE import SuperConductivity
from Supports.Support_Functions import MultMats
from Supports.constants import PI
from TransmissionLineEquations.microStrip.MicroStripModel import SuperConductingMicroStripModel


class SCFL_Model():

    def __init__(self, unit_Cell_Len, D0, In_Order_loads_Widths, number_of_loads, width_unloaded, width_loaded, er,
                 Height, line_thickness, ground_thickness, critical_Temp, pn, tanD, op_temp, Jc):

        # ---------------------------- unit cell inputs
        self.unit_Cell_Len = unit_Cell_Len
        self.width_unloaded = width_unloaded
        self.width_loaded = width_loaded
        self.numberOfLoads = number_of_loads

        # model of FL Line dimensions
        self.FlLine = Line(unit_Cell_Len, D0, number_of_loads, In_Order_loads_Widths)

        # ---------------------------- sce inputs
        self.er = er
        self.Height = Height
        self.line_thickness = line_thickness
        self.ground_thickness = ground_thickness
        self.critical_Temp = critical_Temp
        self.pn = pn
        self.tanD = tanD
        self.op_temp = op_temp

        # ---------------------------- models of the MicroStripModel - one for an unloaded line , one for a loaded line
        self.model_loaded = SuperConductingMicroStripModel(self.Height, self.width_loaded, self.line_thickness, self.er,
                                                           self.tanD, Jc)
        self.model_unloaded = SuperConductingMicroStripModel(self.Height, self.width_unloaded, self.line_thickness,
                                                             self.er, self.tanD, Jc)

        # ---------------------------- model of the Super conductor
        self.conductivity_model = SuperConductivity(op_temp, critical_Temp, pn)

        # used to unfolding beta
        self.region = 0
        self.PiMult = 0
        self.flipping = False
        self.looking = True

    '''
    the calculation of a, b, b-unfolded, r, x
    '''

    def abrx(self, freq):
        # frequency cant be too low
        freq = max(freq, 1000)

        # opt would be to store after first run all conductivity values for a given  freq rannge for a given  self.op_temp, self.critical_Temp, self.pn
        # calc surface impedence Zs for super conductor
        zs = self.conductivity_model.Zs(freq, self.conductivity_model.conductivity(freq), self.line_thickness)

        loaded_propagation, loaded_Zc = self.model_loaded.propagation_constant_characteristic_impedance(freq, zs)
        Unloaded_propagation, Unloaded_Zc = self.model_unloaded.propagation_constant_characteristic_impedance(freq, zs)

        # making all the ABCD matrices for each subsection of unit cell
        mats = []
        for i in range(self.numberOfLoads * 2 + 1):
            # every other is loaded
            if i % 2 == 0:
                mats.append(ABCD_TL(Unloaded_Zc, Unloaded_propagation, self.FlLine.get_L_number(i)))
            else:
                mats.append(ABCD_TL(loaded_Zc, loaded_propagation, self.FlLine.get_L_number(i)))

        # ---- ABCD FOR UNIT CELL  - abcd1 * abcd2 * abcd3 ... abcdN
        ABCD_Mat = MultMats(mats)

        # ---------------------------- calc bloch impedance and propagation const for unit cell

        ZB = Bloch_impedance_Zb(ABCD_Mat)[0]
        pb = Pd(ABCD_Mat)

        r = ZB.real
        x = ZB.imag
        a = pb.real
        bta = pb.imag

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

        return a, bta, unfoldedBeta, r, x
