'''

class to represent alpha_plt floquet line

given:
 -D: the len of unit cell
 -D0: spacing between centers of loads
 -number_of_loads : the number of loads in unit cell
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


def ABCD_Mat(Z, Gamma, L):
    GL = Gamma * L
    coshGL = cmath.cosh(GL)
    sinhGL = cmath.sinh(GL)

    return [[coshGL, Z * sinhGL],
            [(1 / Z) * sinhGL, coshGL]]


class UnitCell():
    # todo remove thickness
    def __init__(self, D: float, D0: float, load_D_lengths: [float], central_line_model, floquet_line_thickness,
                 load_line_models):
        self.central_line_model = central_line_model
        self.thickness = floquet_line_thickness
        self.load_segment_models = load_line_models
        self.unit_cell_length = D

        central_line_lengths = []

        # first central line length (special case where D0 is = to : D0/2)
        central_line_lengths.append((D0 / 2) - (load_D_lengths[0] / 2))

        # normal case calculating central line length between two loads
        # [<---D-left-load--->] ====central line==== [<---D-right-load--->]
        # ---------|---------------------D0--------------------|-----------

        for i in range(len(load_D_lengths) - 1):
            left_load_D, right_load_D = load_D_lengths[i], load_D_lengths[i + 1]
            central_line_lengths.append(self.calc_central_line_length_between_two_loads(left_load_D, D0, right_load_D))

        # last central line length (special case where D0 is = to : D0/2)
        central_line_lengths.append((D0 / 2) - (load_D_lengths[-1] / 2))

        # weaving the central line and loads lengths together into one list
        # load D's [D1, D2] , cental line lenghts = [cl1,cl2,cl3]
        # segment_lengths = [cl1,D1,cl2,D2,cl3]
        self.segment_lengths = [length for b in zip(central_line_lengths, load_D_lengths)
                                for length in b] + [central_line_lengths[-1]]

        self.segment_models = [model for b in zip([central_line_model] * len(load_line_models), load_line_models)
                               for model in b] + [central_line_model]



        print(len(self.segment_models))
        assert abs(D - sum(
            self.segment_lengths)) <= .0001, f"sum of parts lengths != total line length {abs(D - sum(self.segment_lengths))}"

    def calc_central_line_length_between_two_loads(self, left_load_D, D0, right_load_D):
        return D0 - (left_load_D / 2) - (right_load_D / 2)

    # returns the length of the wanted segment in floquet line
    def get_segment_len(self, segment_idx: int):
        return self.segment_lengths[segment_idx]

    def get_central_line_gamma_Zc(self, freq, zs):
        return self.central_line_model.get_propagation_constant_characteristic_impedance(freq, zs)

    def get_segment_gamma_Zc(self, segment_idx, freq, zs):
        return self.segment_models[segment_idx].get_propagation_constant_characteristic_impedance(freq, zs)

    # todo checjk this matrix is correct with the inputs params
    # ABCD matrix of unit sell line segment
    # Z characteristic impedance; k wavenumber; l length

    def get_segment_ABCD_mat(self, unit_cell_segment_idx, freq, zs):
        segment_gamma, segment_Zc = self.get_segment_gamma_Zc(unit_cell_segment_idx, freq, zs)
        segment_length = self.get_segment_len(unit_cell_segment_idx)
        return ABCD_Mat(segment_Zc, segment_gamma, segment_length)

    def get_unit_cell_ABCD_mat(self, freq, zs):

        segment_abcd_mats = []
        for segment_idx in range(len(self.segment_lengths)):
            # 3) for each  line segment of unit cell make ABCD matrices
            segment_gamma, segment_Zc = self.get_segment_gamma_Zc(segment_idx, freq, zs)
            segment_abcd_mats.append(ABCD_Mat(segment_Zc, segment_gamma, self.segment_lengths[segment_idx]))
        # 4) matrix multiply all the abcd mats to make Unit cell ABCD mat
        return mult_mats(segment_abcd_mats)


if __name__ == '__main__':
    D = 6
    D0 = 2
    load_D_lengths = [1, 1, .5]
    central_line_model = []
    floquet_line_thickness = 0
    load_line_models = []

    d = UnitCell(D, D0, load_D_lengths, [], 0, [])
    print(d.segment_lengths)
