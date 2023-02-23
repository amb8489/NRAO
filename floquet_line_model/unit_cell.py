'''

class to represent alpha_plt floquet line

given:
 -unit_cell_length: the len of unit cell
 -D0: spacing between centers of loads
 -number_of_finger_sections : the number of loads in unit cell
 -in_order_loads_widths: the lengths of each load from left to right in Floquet line
    ex: ===|<---D1--->|=====|<---D2--->|=====|<-D3->|===

    in_order_loads_widths = [D1,D2,D3]

     ===CL-Len=== |<---D1 --->|=====CL-Len===== |<---D2 --->|=====CL-Len=====|<---D3 --->|===CL-Len===
    |--------D0/2-------|------------ D0 -------------|----------- D0 ------------ |-------D0/2-------|
     start special case                                                              end special case

Central line length equations:
        d0/2 - d1/2            d0 - d1/2 - d2/2               d0 - d2/2 - d3/2          d0/2 - d3/2
'''
import cmath

from utills.functions import mult_mats


def mk_ABCD_Mat(Z, Gamma, L):
    GL = Gamma * L
    coshGL = cmath.cosh(GL)
    sinhGL = cmath.sinh(GL)

    return [[coshGL, Z * sinhGL],
            [(1 / Z) * sinhGL, coshGL]]


# todo refactor and document all

class UnitCell():
    # todo remove thickness
    def __init__(self, unit_cell_length: float, D0: float, load_D_lengths: [float], central_line_model,
                 floquet_line_thickness,
                 load_line_models):
        self.central_line_model = central_line_model
        self.thickness = floquet_line_thickness
        self.load_segment_models = load_line_models
        self.unit_cell_length = unit_cell_length

        self.segment_line_models = [model for b in zip([central_line_model] * len(load_line_models), load_line_models)
                                    for model in b] + [central_line_model]

        self.segment_lengths = self.calculate_line_segment_lenghts(D0, load_D_lengths, unit_cell_length)

    def calculate_line_segment_lenghts(self, D0, load_D_lengths, unit_cell_length):

        central_line_lengths = []

        # first central line length (special case where D0 is = to : D0/2)
        central_line_lengths.append((D0 / 2) - (load_D_lengths[0] / 2))

        # normal case calculating central line length between two loads
        # [<---unit_cell_length-left-load--->] ====central line==== [<---unit_cell_length-right-load--->]
        # ---------|---------------------D0--------------------|-----------

        for i in range(len(load_D_lengths) - 1):
            left_load_D, right_load_D = load_D_lengths[i], load_D_lengths[i + 1]
            central_line_lengths.append(
                self.__calc_central_line_length_between_two_loads(left_load_D, D0, right_load_D))

        # last central line length (special case where D0 is = to : D0/2)
        central_line_lengths.append((D0 / 2) - (load_D_lengths[-1] / 2))

        # weaving the central line and loads lengths together into one list
        # load unit_cell_length's [D1, D2] , cental line lenghts = [cl1,cl2,cl3]
        # segment_lengths = [cl1,D1,cl2,D2,cl3]
        seg_lengths = [length for b in zip(central_line_lengths, load_D_lengths)
                       for length in b] + [central_line_lengths[-1]]

        if abs(unit_cell_length - sum(seg_lengths)) > .0001:
            raise Exception(f"sum of lengths != unit cell length -- off by: {abs(unit_cell_length - sum(seg_lengths))}")
        return seg_lengths

    def __calc_central_line_length_between_two_loads(self, left_load_D: float, D0: float, right_load_D: float):
        return D0 - (left_load_D / 2) - (right_load_D / 2)

    def get_segment_gamma_and_characteristic_impedance(self, segment_idx: int, frequency: float,
                                                       surface_impedance: complex):
        return self.segment_line_models[segment_idx].get_propagation_constant_characteristic_impedance(frequency,
                                                                                                       surface_impedance)

    # ABCD matrix of unit sell line segment
    def get_unit_cell_ABCD_mat(self, frequency: float, surface_impedance: complex):

        segment_abcd_mats = []
        # 3) for each  line segment of unit cell make sub ABCD matrix for that line segment
        for segment_idx in range(len(self.segment_lengths)):
            segment_gamma, segment_Zc = self.get_segment_gamma_and_characteristic_impedance(segment_idx, frequency,
                                                                                            surface_impedance)
            segment_abcd_mats.append(mk_ABCD_Mat(segment_Zc, segment_gamma, self.segment_lengths[segment_idx]))

        # 4) matrix multiply all the ABCD line segment matrices to get unit cell ABCD
        return mult_mats(segment_abcd_mats)
