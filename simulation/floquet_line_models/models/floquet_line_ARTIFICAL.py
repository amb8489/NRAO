import numpy as np

from simulation.floquet_line_models.models.abstract_floquet_line import floquet_base, floquet_abs
from simulation.floquet_line_models.unit_cell import mk_ABCD_Mat
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.functions import mult_mats, Transmission_Db


class SuperConductingFloquetLine_art(floquet_abs, floquet_base):

    # todo make the other floquet line follow this method od just putting all the line legments into one array
    def __init__(self, line_models: [AbstractSCTL], super_conductivity_model: SuperConductivity, thickness: float,
                 start_freq_GHz: float, end_freq_GHz: float, resoultion: int):
        # ---------------------------- model of the Super conductor

        self.thickness = thickness
        self.super_conductivity_model = super_conductivity_model

        self.start_freq_GHz = start_freq_GHz
        self.end_freq_GHz = end_freq_GHz
        self.resolution = resoultion

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

        # todo 100 needs to be brought in via GUI
        floquet_transmission = Transmission_Db(100, 50, ZB, floquet_gamma_d)

        # calculate central line alpha and beta
        cental_line_gamma, cental_line_Zc = self.get_segment_gamma_and_characteristic_impedance(0, frequency,
                                                                                                surface_impedance)
        cental_line_ABCD = mk_ABCD_Mat(cental_line_Zc, cental_line_gamma, unit_cell_length)

        central_line_propagation_const = self.gamma_d(cental_line_ABCD)
        alpha_d_CL = central_line_propagation_const.real
        beta_d_CL = central_line_propagation_const.imag

        # retuning outputs
        return floquet_gamma_d, ZB, alpha_d_CL, beta_d_CL, floquet_transmission

    def get_segment_gamma_and_characteristic_impedance(self, segment_idx, frequency, zs):
        return self.line_models[segment_idx].get_propagation_constant_characteristic_impedance(frequency, zs)

    def get_resolution(self):
        return self.resolution

    # TODO move this into base class ???
    def simulate(self):

        # ---------------------------- storage -------------------
        # could make this a pandas df
        gamma_d = []
        bloch_impedance = []
        central_line_beta_d = []
        central_line_alpha_d = []

        floquet_transmission = []

        # ---------------------------- simulation -------------------

        frequency_range = np.linspace(self.start_freq_GHz, self.end_freq_GHz, self.resolution)
        for frequency in frequency_range:
            floquet_gamma_d, floquet_bloch_impedance, alpha_d_CL, beta_d_CL, transmission = self.simulate_at_frequency(
                frequency)
            central_line_alpha_d.append(alpha_d_CL)
            central_line_beta_d.append(beta_d_CL)
            gamma_d.append(floquet_gamma_d)
            bloch_impedance.append(floquet_bloch_impedance)
            floquet_transmission.append(transmission)

        return frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, central_line_beta_d, floquet_transmission
