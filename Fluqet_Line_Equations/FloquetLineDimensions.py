'''

class to represent a floquet line

given:
 -D: the len of unit cell
 -D0: spacing between centers of loads
 -number_of_loads : the number of loads in unit cell
 -in_order_loads_widths: the lengths of each load from left to right in Floquet line
    ex: ===|<---L1--->|=====|<---L2--->|=====|<-L3->|===
    in_order_loads_widths = [L1,L2,L3]
'''
from Utills.Functions import micro_meters_to_meters


class FloquetLineDimensions():

    def __init__(self, D: float, D0: float, in_order_loads_widths: [float], thickness, load_line_models, central_line_model):

        # param checking for correctness
        if len(in_order_loads_widths) < 1:
            raise Exception(f"number of loads has to be >= 1: passed in {len(in_order_loads_widths) }")



        # saving usefull info
        self.D = D
        self.D0 = D0
        self.load_line_models, self.central_line_model = load_line_models, central_line_model
        self.number_of_loads = len(in_order_loads_widths)
        self.in_order_loads_widths = in_order_loads_widths
        self.thickness = thickness
        # array to hold lengths of line segments of the FL
        self.floquet_line_parts_lengths = []
        self.floquet_line_segments = []

        # add D0 widths loads to front and back to simplify code in calculating segments
        self.in_order_loads_widths = [D0] + self.in_order_loads_widths + [D0]

        # compute the lengths of the ccentral lines between the loads
        for i in range(self.number_of_loads + 1):

            self.floquet_line_segments.append(self.central_line_model)

            if i != self.number_of_loads:
                self.floquet_line_segments.append(self.load_line_models[i])


            # add the load length just not thr first 0
            if i != 0:self.floquet_line_parts_lengths.append(self.in_order_loads_widths[i])

            # compute and add length of the central line between load[i] and load[i+1]   [load i] ---CL--- [load i+1]
            # L = D0 - (1/2 * loadLen[i] ) - (1/2 * loadLen[i+1] )
            self.floquet_line_parts_lengths.append(
                D0 - (self.in_order_loads_widths[i] / 2) - (self.in_order_loads_widths[i + 1] / 2))

        # check to make sure sum of lengths adds up to unit cell length
        if abs(D - sum(self.floquet_line_parts_lengths)) > 0.001:
            raise Exception(
                f"sum of loads and central line lenths do not add to expected total length of line D {D - sum(self.floquet_line_parts_lengths)}")
        self.in_order_loads_widths = in_order_loads_widths

    # returns the length of the wanted segment in FL
    def get_segment_len(self, partNumber: int):
        return self.floquet_line_parts_lengths[partNumber]


    def get_Central_line_gamma_Zc(self, freq, zs):
        return self.central_line_model.get_propagation_constant_characteristic_impedance(freq, zs)

    def get_gamma_Zc(self, unit_cell_segment_idx, freq, zs):
        return self.floquet_line_segments[unit_cell_segment_idx].get_propagation_constant_characteristic_impedance(freq, zs)
