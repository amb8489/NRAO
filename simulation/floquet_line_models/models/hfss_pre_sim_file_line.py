import numpy as np
from matplotlib import pyplot as plt

from simulation.floquet_line_models.models.abstract_floquet_line import floquet_base, floquet_abs
from simulation.floquet_line_models.unit_cell import UnitCell, mk_ABCD_Mat
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.constants import PI2, SPEED_OF_LIGHT
from simulation.utills.functions import Transmission_Db, micro_meters_to_meters, beta_unfold, mult_mats, ABCD_Mat, \
    gamma_d, bloch_impedance_Zb

# calc transmission todo add these inputs to UI
impedance = 50


class SuperConductingFloquetLine(floquet_abs, floquet_base):

    def __init__(self, csv_data_list, wl_microns:float,wu_microns:float,Lu_microns: float, dimensions: [[float]], is_art_cpw_line: bool, start_freq_GHz: float,
                 end_freq_GHz: float, resolution: int):
        # ---------------------------------------------------------

        self.csv_data = csv_data_list

        # FLOQUET DIMENSIONS

        # if we are doing an art cpw then dimensions will be the number of Lu segments
        # and need to multiply #lu segs by Lu to get line length
        self.Lu_length = Lu_microns
        if is_art_cpw_line:
            self.line_lengths = np.array([n[0] for n in dimensions])
            self.Lu = micro_meters_to_meters(self.Lu_length)
            self.line_lengths *= self.Lu
        else:
            #make sure the inuts line lengths are right dimensions
            self.line_lengths = np.array([micro_meters_to_meters(n[0]) for n in dimensions])

        self.unit_cell_length = sum(self.line_lengths)

        self.wu = wu_microns
        self.wl = wl_microns

        self.start_freq_GHz = start_freq_GHz
        self.end_freq_GHz = end_freq_GHz
        self.resolution = resolution

    def get_unit_cell_length(self):
        return self.unit_cell_length

    def get_resolution(self):
        return self.resolution

    def simulate_at_frequency(self, frequency):
        pass

    def simulate(self):

        fig, axs = plt.subplots(2)
        frequency_range = np.linspace(self.start_freq_GHz, self.end_freq_GHz, self.resolution)

        # index in data where the wanted widths are ... todo some type of interpolation if value not in list
        Wu_idx = self.csv_data[:, 0].index(self.wu)
        Wl_idx = self.csv_data[:, 0].index(self.wl)

        # getting the Zc and gammas for the central line width and load widths
        unit_cell_segment_gammas = np.array(
            [self.csv_data[Wu_idx][2], self.csv_data[Wl_idx][2], self.csv_data[Wu_idx][2],
             self.csv_data[Wl_idx][2], self.csv_data[Wu_idx][2], self.csv_data[Wl_idx][2],
             self.csv_data[Wu_idx][2]]) * 1j

        unit_cell_segment_zc = np.array(
            [self.csv_data[Wu_idx][1], self.csv_data[Wl_idx][1], self.csv_data[Wu_idx][1],
             self.csv_data[Wl_idx][1], self.csv_data[Wu_idx][1], self.csv_data[Wl_idx][1],
             self.csv_data[Wu_idx][1]]) + 0j

        CL_gammas = []
        gammas = []
        ZBs = []

        # facotors to turn Beta/C into beta
        Vs = (PI2 * frequency_range) / SPEED_OF_LIGHT

        for i, f in enumerate(frequency_range):

            # FOR EACH LINE SEGMENT IN THE UNIT CELL GET THE SEGMENTS ABCD MAT
            seg_abcds = []
            for j in range(len(unit_cell_segment_gammas)):
                seg_abcds.append(
                    ABCD_Mat(unit_cell_segment_zc[j], unit_cell_segment_gammas[j] * Vs[i], self.line_lengths[j]))

            unit_cell_mat = mult_mats(seg_abcds)
            gammas.append(gamma_d(unit_cell_mat))
            ZBs.append(bloch_impedance_Zb(unit_cell_mat))

            CL_gammas.append(
                gamma_d(ABCD_Mat(unit_cell_segment_zc[0], unit_cell_segment_gammas[0] * Vs[i], self.unit_cell_length)))

        axs[0].plot(frequency_range, np.real(np.array(gammas)))
        axs[0].plot(frequency_range, beta_unfold(np.imag(np.array(gammas))) - beta_unfold(np.imag(np.array(CL_gammas))))
        axs[1].plot(frequency_range, np.real(np.array(ZBs)))
        axs[1].plot(frequency_range, np.imag(np.array(ZBs)))
        axs[1].set_ylim([-500, 500])
        plt.show()
        exit(1)

    # floquet_transmission = Transmission_Db(150,impedance,ZB,floquet_gamma_d)
    # return frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, central_line_beta_d, floquet_transmission
