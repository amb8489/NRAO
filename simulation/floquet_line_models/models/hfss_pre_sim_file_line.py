import numpy as np

from simulation.floquet_line_models.models.abstract_floquet_line import floquet_base, floquet_abs
from simulation.floquet_line_models.unit_cell import UnitCell, mk_ABCD_Mat
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.functions import Transmission_Db, micro_meters_to_meters

# calc transmission todo add these inputs to UI
impedance = 50





class SuperConductingFloquetLine(floquet_abs, floquet_base):

    def __init__(self, unit_cell_length: float, D0: float, load_lengths: [float], load_line_models: [AbstractSCTL],
                 central_line_model: AbstractSCTL, super_conductivity_model: SuperConductivity,
                 central_line_width: float, load_widths: [float], line_thickness: float, start_freq_GHz: float,
                 end_freq_GHz: float, resolution: int):
        # ---------------------------------------------------------

        self.resolution = resolution
        self.start_freq_GHz = start_freq_GHz
        self.end_freq_GHz = end_freq_GHz






    def get_unit_cell_length(self):
        return self.unit_cell.unit_cell_length


    def get_resolution(self):
        return self.resolution

    def simulate_at_frequency(self, frequency):
        # frequency cant be too low
        frequency = max(frequency, 1e6)

        # todo move the conductivity model into the line model
        # 1) calculate Zs
        conductivity = self.super_conductivity_model.conductivity(frequency)

        # 2) calculate Zs for given frequency, conductivity ,line thickness
        surface_impedance = self.super_conductivity_model.surface_impedance_Zs(frequency, conductivity,
                                                                               self.unit_cell.thickness)

        # 5) get unit cell ABCD -- steps 3 - 4 inside get_unit_cell_ABCD_mat()
        unit_cell_abcd_mat = self.unit_cell.get_unit_cell_ABCD_mat(frequency, surface_impedance)

        # 6) calculate all the needed outputs
        # calc bloch impedance and propagation const for unit cell
        ZB = self.bloch_impedance_Zb(unit_cell_abcd_mat)
        floquet_gamma_d = self.gamma_d(unit_cell_abcd_mat)

        floquet_transmission = Transmission_Db(N_unit_cells,
                                               impedance,
                                               ZB,
                                               floquet_gamma_d)


        # calculate central line alpha and beta
        central_line_gamma, central_line_characteristic_impedance = self.unit_cell.get_segment_gamma_and_characteristic_impedance(
            0, frequency, surface_impedance)

        central_line_mat = mk_ABCD_Mat(central_line_characteristic_impedance, central_line_gamma,
                                       self.unit_cell.unit_cell_length)
        central_line_propagation_const = self.gamma_d(central_line_mat)
        beta_d_CL = central_line_propagation_const.imag
        alpha_d_CL = central_line_propagation_const.real

        # retuning outputs
        return floquet_gamma_d, ZB, alpha_d_CL, beta_d_CL, floquet_transmission

    def simulate(self):
        frequency_range = np.linspace(self.start_freq_GHz, self.end_freq_GHz, self.resolution)

        # plt.plot(csv_data[:, 2])
        # plt.show()

        # FLOQUET DIMENSIONS
        if self.is_art_cpw_line:
            Lu = micro_meters_to_meters(self.lu_length)

            seg_lens = []
            for n_lu_repeating in self.dimensions:
                seg_lens.append(Lu * n_lu_repeating)

        # pick line widths
        Wu = self.wu_length
        Wl = self.wl_length


        D = sum(seg_lens)

        # to we can vectorize this into something real ugly but fast , dont think its needed tho
        fig, axs = plt.subplots(2)

        L1 = Wl
        L2 = Wl
        L3 = Wl
        gammas, ZBs = [], []

        CL_gammas = []

        V = (PI2 * frequency_range) / SPEED_OF_LIGHT

        seg_gamma = np.array([csv_data[Wu][2], csv_data[L1][2], csv_data[Wu][2], csv_data[L2][2],
                              csv_data[Wu][2], csv_data[L3][2], csv_data[Wu][2]]) * 1j

        seg_zc = np.array([csv_data[Wu][1], csv_data[L1][1], csv_data[Wu][1], csv_data[L2][1],
                           csv_data[Wu][1], csv_data[L3][1], csv_data[Wu][1]]) + 0j

        tot = 0
        start = time.time()

        for i, f in enumerate(frequency_range):

            seg_abcds = []
            for j in range(len(seg_gamma)):
                seg_abcds.append(ABCD_Mat(seg_zc[j], seg_gamma[j] * V[i], seg_lens[j]))

            unit_cell_mat = mult_mats(seg_abcds)
            gammas.append(gamma_d(unit_cell_mat))
            ZBs.append(bloch_impedance_Zb(unit_cell_mat))

            CL_gammas.append(gamma_d(ABCD_Mat(seg_zc[0], seg_gamma[0] * V[i], D)))

        overall = time.time() - start
        print((tot / overall) * 100, "%  ", overall)

        axs[0].plot(frequency_range, np.real(np.array(gammas)))
        axs[0].plot(frequency_range, beta_unfold(np.imag(np.array(gammas))) - beta_unfold(np.imag(np.array(CL_gammas))))
        axs[1].plot(frequency_range, np.real(np.array(ZBs)))
        axs[1].plot(frequency_range, np.imag(np.array(ZBs)))
        axs[1].set_ylim([-500, 500])
        plt.show()

    return frequency_range, gamma_d, bloch_impedance, central_line_alpha_d, central_line_beta_d, floquet_transmission
