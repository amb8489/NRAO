import cmath

import numpy as np

from floquet_line_model.unit_cell import mk_ABCD_Mat
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from utills.functions import mult_mats, Transmission


class SuperConductingFloquetLine_art():

    # todo make the other floquet line follow this method od just putting all the line legments into one array
    def __init__(self, line_models: [AbstractSCTL], super_conductivity_model: SuperConductivity, thickness):
        # ---------------------------- model of the Super conductor

        self.thickness = thickness
        self.super_conductivity_model = super_conductivity_model

        # ---------------------------- unit cell inputs

        # todo are these even being used in any calculations

        self.line_models = line_models

    def get_unit_cell_length(self):
        return sum(line.total_line_length for line in self.line_models)

    def Bloch_impedance_Zb(self, ABCD_mat_2x2: [[float]]):
        A = ABCD_mat_2x2[0][0]
        B = ABCD_mat_2x2[0][1]
        D = ABCD_mat_2x2[1][1]

        ADs2 = cmath.sqrt(((A + D) ** 2) - 4)
        ADm = A - D

        B2 = 2 * B

        ZB = - (B2 / (ADm + ADs2))
        ZB2 = - (B2 / (ADm - ADs2))
        if ZB.real < 0:
            ZB = ZB2

        return ZB

    def gamma_d(self, ABCD_mat_2x2: [[float]]):
        A = ABCD_mat_2x2[0][0]
        D = ABCD_mat_2x2[1][1]

        return np.arccosh(((A + D) / 2))

    def simulate(self, frequency):
        # frequency cant be too low
        frequency = max(frequency, 1e7)

        # 1) calculate Zs
        conductivity = self.super_conductivity_model.conductivity(frequency)

        # 2) calculate Zs for given frequency, conductivity ,line thickness
        surface_impedance = self.super_conductivity_model.surface_impedance_Zs(frequency, conductivity,
                                                                               self.thickness)

        # get the sub ABCD mats for each line in the unit cell
        segment_abcd_mats = []
        unit_cell_length = 0
        for segment_idx in range(len(self.line_models)):
            # 3) for each  line segment of unit cell make sub ABCD matrices

            segment_gamma, segment_Zc = self.get_segment_gamma_and_characteristic_impedance(segment_idx, frequency,
                                                                                            surface_impedance)
            segment_abcd_mat = mk_ABCD_Mat(segment_Zc, segment_gamma, self.line_models[segment_idx].total_line_length)
            segment_abcd_mats.append(segment_abcd_mat)
            unit_cell_length += self.line_models[segment_idx].total_line_length

        # 4) matrix multiply all the sub abcd mats to make Unit cell ABCD mat
        unit_cell_abcd_mat = mult_mats(segment_abcd_mats)

        # 6) calculate all the needed outputs
        # calc bloch impedance and propagation const for unit cell
        ZB = self.Bloch_impedance_Zb(unit_cell_abcd_mat)
        floquet_gamma_d = self.gamma_d(unit_cell_abcd_mat)

        # get alpha beta r

        floquet_beta = floquet_gamma_d.imag
        floquet_alpha = floquet_gamma_d.real
        floquet_r = ZB.real
        floquet_x = ZB.imag

        floquet_transmission = Transmission(100,
                                            50,
                                            ZB,
                                            floquet_gamma_d)

        # calculate central line alpha and beta
        cental_line_gamma, cental_line_Zc = self.get_segment_gamma_and_characteristic_impedance(0, frequency,
                                                                                                surface_impedance)
        cental_line_ABCD = mk_ABCD_Mat(cental_line_Zc, cental_line_gamma, unit_cell_length)

        central_line_propagation_const = self.gamma_d(cental_line_ABCD)
        central_line_beta = central_line_propagation_const.imag
        central_line_alpha = central_line_propagation_const.real

        # retuning outputs
        return floquet_alpha, floquet_beta, central_line_alpha, central_line_beta, floquet_r, floquet_x, \
               floquet_transmission

    def get_segment_gamma_and_characteristic_impedance(self, segment_idx, frequency, zs):
        return self.line_models[segment_idx].get_propagation_constant_characteristic_impedance(frequency, zs)
