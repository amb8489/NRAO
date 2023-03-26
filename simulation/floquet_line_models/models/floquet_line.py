
"""




"""


import numpy as np
from simulation.floquet_line_models.models.abstract_floquet_line import floquet_base, floquet_abs
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.super_conducting_transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.functions import mult_mats, Transmission_Db


class FloquetLine(floquet_abs, floquet_base):


    def __init__(self, line_models: [AbstractSCTL], super_conductivity_model: SuperConductivity, n_repeated_cells):

        self.__n_repeated_cells = n_repeated_cells

        ####################### model of the Super conductor #######################
        self.__super_conductivity_model = super_conductivity_model

        ######################## unit cell details #######################
        self.__unit_cell_segments = line_models
        self.__unit_cell_length = sum([line.get_length() for line in line_models])

    def get_unit_cell_length(self):
        return self.__unit_cell_length

    def __simulate_at_frequency(self, frequency):

        # some equations start to fail when frequency is low
        frequency = max(frequency, 1e7)

        # 2) calculate Zs for given frequency, conductivity ,line thickness
        surface_impedance = self.__super_conductivity_model.surface_impedance_Zs(frequency)

        # get the sub ABCD mats for each line in the unit cell
        segment_abcd_mats = []

        # todo vectorize?
        for idx in range(len(self.__unit_cell_segments)):
            # 3) for each  line segment of unit cell make sub ABCD matrices

            segment_gamma, segment_Zc = self.get_segment_gamma_and_Zc(idx, frequency,
                                                                      surface_impedance)
            segment_abcd_mat = self.ABCD_Mat(segment_Zc, segment_gamma, self.__unit_cell_segments[idx].get_length())
            segment_abcd_mats.append(segment_abcd_mat)

        # 4) matrix multiply all the sub abcd mats to make Unit cell ABCD mat
        unit_cell_abcd_mat = mult_mats(segment_abcd_mats)

        # 6) calculate all the needed outputs
        # calc bloch impedance and propagation const for unit cell
        ZB = self.bloch_impedance_Zb(unit_cell_abcd_mat)
        floquet_gamma_d = self.gamma_d(unit_cell_abcd_mat)

        # todo 100 needs to be brought in via GUI
        floquet_transmission = Transmission_Db(self.__n_repeated_cells, 50, ZB, floquet_gamma_d)

        # calculate central line alpha and beta
        central_line_gamma, central_line_Zc = self.get_segment_gamma_and_Zc(0, frequency, surface_impedance)
        central_line_ABCD = self.ABCD_Mat(central_line_Zc, central_line_gamma, self.__unit_cell_length)

        central_line_gamma = self.gamma_d(central_line_ABCD)
        alpha_d_CL = central_line_gamma.real
        beta_d_CL = central_line_gamma.imag

        return floquet_gamma_d, ZB, alpha_d_CL, beta_d_CL, floquet_transmission

    def get_segment_gamma_and_Zc(self, segment_idx, frequency, zs):
        return self.__unit_cell_segments[segment_idx].get_propagation_constant_characteristic_impedance(
            frequency, zs)

    # TODO move this into base class ???
    def simulate_over_frequency_range(self, start_frequency: float, end_frequency: float, delta_frequency: int):
        '''

        :param start_frequency: frequency to start simulating at
        :param end_freq_GHz: frequency to end simulating at
        :param delta_f: step amount between simulation frequency's

        :return: list of siulated outputs
        '''

        # ---------------------------- storage -------------------
        # could make this a pandas df
        gamma_d = []
        bloch_impedance = []
        central_line_beta_d = []
        central_line_alpha_d = []
        floquet_transmission = []

        # ---------------------------- simulation over frequency's-------------------

        frequency_range = np.arange(start_frequency, end_frequency, delta_frequency)

        for frequency in frequency_range:
            floquet_gamma_d, floquet_bloch_impedance, alpha_d_CL, beta_d_CL, transmission = self.__simulate_at_frequency(
                frequency)
            central_line_alpha_d.append(alpha_d_CL)
            central_line_beta_d.append(beta_d_CL)
            gamma_d.append(floquet_gamma_d)
            bloch_impedance.append(floquet_bloch_impedance)
            floquet_transmission.append(transmission)

        return frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, central_line_beta_d, floquet_transmission
