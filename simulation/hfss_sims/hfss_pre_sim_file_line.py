import numpy as np
from matplotlib import pyplot as plt

from simulation.floquet_line_models.models.abstract_floquet_line import floquet_base, floquet_abs
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.super_conducting_transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.constants import PI2, SPEED_OF_LIGHT
from simulation.utills.functions import Transmission_Db, microns_to_meters, beta_unfold, mult_mats

# calc transmission todo add these inputs to UI
impedance = 50


class pre_sim_floquet_line(floquet_abs, floquet_base):

    def __init__(self, csv_data_list, wl_microns: float, wu_microns: float, Lu_microns: float, dimensions: [[float]],
                 is_art_cpw_line: bool, start_freq_GHz: float,
                 end_freq_GHz: float, resolution: int, n_repeated_cells: int):
        # ---------------------------------------------------------

        self.csv_data = csv_data_list
        self.n_repeated_cells = n_repeated_cells

        # FLOQUET DIMENSIONS

        # if we are doing an art cpw then dimensions will be the number of Lu segments
        # and need to multiply #lu segs by Lu to get line length
        self.Lu_length = Lu_microns
        if is_art_cpw_line:
            self.line_lengths = np.array([float(n[0]) for n in dimensions])
            self.Lu = microns_to_meters(self.Lu_length)
            self.line_lengths *= self.Lu
        else:
            # make sure the inuts line lengths are right dimensions
            self.line_lengths = np.array([microns_to_meters(float(n[0])) for n in dimensions])

        self.unit_cell_length = sum(self.line_lengths)

        self.wu = wu_microns
        self.wl = wl_microns

        self.start_frequency = start_freq_GHz
        self.end_frequency = end_freq_GHz
        self.resolution = resolution

    def get_unit_cell_length(self):
        return self.unit_cell_length

    def get_resolution(self):
        return self.resolution

    def simulate_at_frequency(self, frequency):
        pass

    def simulate_over_frequency_range(self):

        frequency_range = np.linspace(self.start_frequency, self.end_frequency, self.resolution)

        # index in data where the wanted widths are ... todo some type of interpolation if value not in list
        Wu_idx = self.csv_data[:, 0].tolist().index(self.wu)
        Wl_idx = self.csv_data[:, 0].tolist().index(self.wl)





        # getting the Zc and gammas for the central line width and load widths
        unit_cell_segment_gammas = 1 / np.array(
            [self.csv_data[Wu_idx][2], self.csv_data[Wl_idx][2], self.csv_data[Wu_idx][2],
             self.csv_data[Wl_idx][2], self.csv_data[Wu_idx][2], self.csv_data[Wl_idx][2],
             self.csv_data[Wu_idx][2]]) * 1j

        unit_cell_segment_zc = np.array(
            [self.csv_data[Wu_idx][1], self.csv_data[Wl_idx][1], self.csv_data[Wu_idx][1],
             self.csv_data[Wl_idx][1], self.csv_data[Wu_idx][1], self.csv_data[Wl_idx][1],
             self.csv_data[Wu_idx][1]]) + 0j



        print(self.csv_data[Wu_idx][2],self.csv_data[Wl_idx][2])

        gammas_d = []
        ZBs = []
        floquet_transmissions = []
        central_line_alpha_d = []
        central_line_beta_d = []

        # facotors to turn Beta/C into beta
        Vs = ((PI2 * frequency_range) / SPEED_OF_LIGHT)

        for i, f in enumerate(frequency_range):

            # FOR EACH LINE SEGMENT IN THE UNIT CELL GET THE SEGMENTS ABCD MAT
            seg_abcds = []
            for j in range(len(unit_cell_segment_gammas)):
                seg_abcds.append(
                    self.ABCD_Mat(unit_cell_segment_zc[j], (unit_cell_segment_gammas[j]) * Vs[i], self.line_lengths[j]))

            unit_cell_mat = mult_mats(seg_abcds)

            # todo is this gamma or gamma_d

            floquet_gamma_d = self.gamma_d(unit_cell_mat)
            gammas_d.append(floquet_gamma_d)

            ZB = self.bloch_impedance_Zb(unit_cell_mat)
            ZBs.append(ZB)

            CL_gamma = self.gamma_d(
                self.ABCD_Mat(unit_cell_segment_zc[0], unit_cell_segment_gammas[0] * Vs[i], self.unit_cell_length))

            floquet_transmission = Transmission_Db(self.n_repeated_cells, impedance, ZB, floquet_gamma_d)
            floquet_transmissions.append(floquet_transmission)

            central_line_alpha_d.append(CL_gamma.real)
            central_line_beta_d.append(CL_gamma.imag)

        return frequency_range, gammas_d, ZBs, central_line_alpha_d, central_line_beta_d, floquet_transmissions
