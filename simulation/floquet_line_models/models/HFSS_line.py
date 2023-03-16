import cmath
import numpy as np
import skrf as rf

from simulation.floquet_line_models.models.abstract_floquet_line import floquet_abs, floquet_base
from simulation.gain_models.multiprocessing_gain_simulate import simulate_gain_multiprocessing
from simulation.utills.functions import Transmission_Db






class hfss_touchstone_file_model(floquet_abs,floquet_base):


    def __init__(self,hfss_touchstone_file_path,n_interp_points,unit_cell_length,n_repeated_unit_cells):


        self.unit_cell_ABCD_mats,self.frequency_range_simulated_over = self.get_abcd_mats_and_frequency_range_from_hfss_touchstone_file(hfss_touchstone_file_path,n_interp_points)
        self.n_repeated_unit_cells = n_repeated_unit_cells
        self.impedance = 50
        self.unit_cell_length = unit_cell_length



    def get_resolution(self):
        return len(self.frequency_range_simulated_over)

    def get_unit_cell_length(self):
        return self.unit_cell_length

    def get_abcd_mats_and_frequency_range_from_hfss_touchstone_file(self,hfss_touchstone_file_path: str, n_interp_points: int = 1000):
        # make network
        network = rf.hfss_touchstone_2_network(hfss_touchstone_file_path)

        # zero points means don't do any interpolation
        if n_interp_points < network.frequency.npoints and n_interp_points > 0:
            raise Exception(
                f"n_interp_points must be > number of already simulated frequency points: {n_interp_points} < {network.sim_frequency.npoints}")

        if n_interp_points > 0:
            interp_freq_range = rf.frequency.Frequency(start=network.frequency.start / 1e9,
                                                       stop=network.frequency.stop / 1e9,
                                                       npoints=int(n_interp_points), unit='ghz')

            network = network.interpolate(interp_freq_range, basis="a")

        # get abcd mats
        unit_cell_ABCD_mats = network.a

        # get the frequency range
        simulated_frequency_range = network.f

        return unit_cell_ABCD_mats, simulated_frequency_range


    def simulate(self):

        floquet_alphas_d, floquet_betas_d, floquet_rs, floquet_xs,floquet_transmission = [], [], [], [],[]
        for unit_cell_abcd_mat in self.unit_cell_ABCD_mats:
            # 6) calculate all the needed outputs
            # calc bloch impedance and propagation const for unit cell

            floquet_propagation_const_gamma = self.gamma_d(unit_cell_abcd_mat)
            ZB = self.bloch_impedance_Zb(unit_cell_abcd_mat)

            floquet_transmission_ = Transmission_Db(self.n_repeated_unit_cells,
                                                    self.impedance,
                                                    ZB,
                                                    floquet_propagation_const_gamma)
            floquet_transmission.append(floquet_transmission_)

            # get alpha beta r x
            floquet_alpha = floquet_propagation_const_gamma.real
            floquet_beta = floquet_propagation_const_gamma.imag
            floquet_r = ZB.real
            floquet_x = ZB.imag

            floquet_alphas_d.append(floquet_alpha)
            floquet_betas_d.append(floquet_beta)
            floquet_rs.append(floquet_r)
            floquet_xs.append(floquet_x)


        return self.frequency_range_simulated_over,floquet_alphas_d, [0] * len(floquet_alphas_d), floquet_betas_d, [0] * len(
            floquet_betas_d), floquet_rs, floquet_xs,floquet_transmission
