import numpy as np
from matplotlib import pyplot as plt

from simulation.floquet_line_models.models.abstract_floquet_line import floquet_base, floquet_abs
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.super_conducting_transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.constants import PI2, SPEED_OF_LIGHT
from simulation.utills.functions import Transmission_Db, microns_to_meters, beta_unfold, mult_mats

# calc transmission todo add these inputs to UI
impedance = 50


class PreSimFloquetLine(floquet_abs, floquet_base):

    def __init__(self, csv_data_list, wl: float, wu: float, lu_length: float, line_dimension: [[float]],
                 is_art_cpw_line: bool, n_repeated_cells: int):
        # ---------------------------------------------------------

        self.csv_data = csv_data_list
        self.n_repeated_cells = n_repeated_cells

        # FLOQUET DIMENSIONS

        # if we are doing an art cpw then dimensions will be the number of Lu segments
        # and need to multiply #lu segs by Lu to get line length
        self.lu_length = lu_length
        self.line_lengths = np.array(line_dimension)

        if is_art_cpw_line:
            self.line_lengths *= self.lu_length
        else:
            self.line_dimension = [microns_to_meters(len) for len in line_dimension]

        self.unit_cell_length = sum(self.line_lengths)
        self.wu = wu
        self.wl = wl

    def get_unit_cell_length(self):
        return self.unit_cell_length

    def simulate_at_frequency(self, frequency):
        pass

    def simulate_over_frequency_range(self, frequency_range):

        # todo could do some type of interpolation if value not in list

        gammas_d = []
        ZBs = []
        floquet_transmissions = []
        central_line_alpha_d = []
        central_line_beta_d = []

        # index in data where the wanted widths are ...
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

        # facotors to turn Beta/C into beta
        Vs = ((PI2 * frequency_range) / SPEED_OF_LIGHT)

        for i in range(len(frequency_range)):

            # FOR EACH LINE SEGMENT IN THE UNIT CELL GET THE SEGMENTS ABCD MAT
            seg_abcds = []
            for j in range(len(unit_cell_segment_gammas)):
                seg_abcds.append(
                    self.ABCD_Mat(unit_cell_segment_zc[j], (unit_cell_segment_gammas[j]) * Vs[i], self.line_lengths[j]))

            unit_cell_mat = mult_mats(seg_abcds)

            floquet_gamma_d = self.gamma_d(unit_cell_mat)
            ZB = self.bloch_impedance_Zb(unit_cell_mat)

            CL_gamma = self.gamma_d(
                self.ABCD_Mat(unit_cell_segment_zc[0], unit_cell_segment_gammas[0] * Vs[i], self.unit_cell_length))

            floquet_transmission = Transmission_Db(self.n_repeated_cells, impedance, ZB, floquet_gamma_d)

            gammas_d.append(floquet_gamma_d)
            ZBs.append(ZB)
            floquet_transmissions.append(floquet_transmission)
            central_line_alpha_d.append(CL_gamma.real)
            central_line_beta_d.append(CL_gamma.imag)

        return frequency_range, gammas_d, ZBs, central_line_alpha_d, central_line_beta_d, floquet_transmissions
