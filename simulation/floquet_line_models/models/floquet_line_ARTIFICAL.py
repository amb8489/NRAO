import numpy as np

from simulation.floquet_line_models.models.abstract_floquet_line import floquet_base, floquet_abs
from simulation.floquet_line_models.unit_cell import mk_ABCD_Mat
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.functions import mult_mats, Transmission_Db


class SuperConductingFloquetLine_art(floquet_abs, floquet_base):

    # todo make the other floquet line follow this method od just putting all the line legments into one array
    def __init__(self, line_models: [AbstractSCTL], super_conductivity_model: SuperConductivity, thickness:float,
                 start_freq_GHz: float, end_freq_GHz: float, resoultion: int):
        # ---------------------------- model of the Super conductor

        self.thickness = thickness
        self.super_conductivity_model = super_conductivity_model

        self.start_freq_GHz = start_freq_GHz
        self.end_freq_GHz = end_freq_GHz
        self.resoultion = resoultion

        # ---------------------------- unit cell inputs

        # todo are these even being used in any calculations

        self.line_models = line_models

    def get_unit_cell_length(self):
        return sum(line.total_line_length for line in self.line_models)

    def simulate_at_frequency(self, frequency):
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
        ZB = self.bloch_impedance_Zb(unit_cell_abcd_mat)
        floquet_gamma_d = self.gamma_d(unit_cell_abcd_mat)

        # get alpha beta r

        floquet_beta = floquet_gamma_d.imag
        floquet_alpha = floquet_gamma_d.real
        floquet_r = ZB.real
        floquet_x = ZB.imag

        floquet_transmission = Transmission_Db(100,
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



    def get_resolution(self):
        return self.resoultion
    # TODO move this into base class ???
    def simulate(self):

        # ---------------------------- storage -------------------
        # could make this a pandas df
        floquet_alpha_d = []
        floquet_beta_d = []
        floquet_r = []
        floquet_x = []
        floquet_transmission = []
        central_line_beta = []
        central_line_alpha = []

        # ---------------------------- simulation -------------------

        frequency_range = np.linspace(self.start_freq_GHz, self.end_freq_GHz, self.resoultion)
        for frequency in frequency_range:
            alpha_d, beta_d, alpha_d_CL, beta_d_CL, r, x, transmission_ = self.simulate_at_frequency(frequency)
            central_line_beta.append(beta_d_CL)
            central_line_alpha.append(alpha_d_CL)
            floquet_beta_d.append(beta_d)
            floquet_alpha_d.append(alpha_d)
            floquet_r.append(r)
            floquet_x.append(x)
            floquet_transmission.append(transmission_)

        return frequency_range,\
               floquet_alpha_d, \
               central_line_alpha, \
               floquet_beta_d, \
               central_line_beta, \
               floquet_r, \
               floquet_x, \
               floquet_transmission
