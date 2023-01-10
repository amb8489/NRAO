'''

class to represent a floquet line

given:
 -D: the len of unit cell
 -D0: spacing between centers of loads
 -number_of_loads : the number of loads in unit cell
 -In_Order_loads_Widths: the lengths of each load from left to right in Floquet line
    ex: ===|<---L1--->|=====|<---L2--->|=====|<-L3->|===
    In_Order_loads_Widths = [L1,L2,L3]
'''
from Utills.Functions import microMeters_to_Meters


class FloquetLineDimensions():

    def __init__(self, D: float, D0: float, In_Order_loads_Widths: [float],thickness,Load_line_models, Central_line_model):

        # param checking for correctness
        if len(In_Order_loads_Widths) < 1:
            raise Exception(f"number of loads has to be >= 1: passed in {len(In_Order_loads_Widths) }")



        # saving usefull info
        self.D = D
        self.D0 = D0
        self.Load_line_models, self.Central_line_model = Load_line_models, Central_line_model
        self.number_of_loads = len(In_Order_loads_Widths)
        self.In_Order_loads_Widths = In_Order_loads_Widths
        self.thickness = thickness
        # array to hold lengths of line segments of the FL
        self.Floquet_Line_Parts_Lengths = []
        self.Floquet_Line_segments = []

        # add D0 widths loads to front and back to simplify code in calculating segments
        self.In_Order_loads_Widths = [D0] + self.In_Order_loads_Widths + [D0]

        # compute the lengths of the ccentral lines between the loads
        for i in range(self.number_of_loads + 1):

            self.Floquet_Line_segments.append(self.Central_line_model)

            if i != self.number_of_loads:
                self.Floquet_Line_segments.append(self.Load_line_models[i])


            # add the load length just not thr first 0
            if i != 0:self.Floquet_Line_Parts_Lengths.append(self.In_Order_loads_Widths[i])

            # compute and add length of the central line between load[i] and load[i+1]   [load i] ---CL--- [load i+1]
            # L = D0 - (1/2 * loadLen[i] ) - (1/2 * loadLen[i+1] )
            self.Floquet_Line_Parts_Lengths.append(
                D0 - (self.In_Order_loads_Widths[i] / 2) - (self.In_Order_loads_Widths[i + 1] / 2))

        # check to make sure sum of lengths adds up to unit cell length
        if abs(D - sum(self.Floquet_Line_Parts_Lengths)) > 0.001:
            raise Exception(
                f"sum of loads and central line lenths do not add to expected total length of line D {D - sum(self.Floquet_Line_Parts_Lengths)}")
        self.In_Order_loads_Widths = In_Order_loads_Widths

    # returns the length of the wanted segment in FL
    def get_segment_len(self, partNumber: int):
        return self.Floquet_Line_Parts_Lengths[partNumber]


    def get_Central_line_gamma_Zc(self, freq, zs):
        return self.Central_line_model.get_propagation_constant_characteristic_impedance(freq, zs)

    def get_gamma_Zc(self, unit_cell_segment_idx, freq, zs):
        return self.Floquet_Line_segments[unit_cell_segment_idx].get_propagation_constant_characteristic_impedance(freq, zs)