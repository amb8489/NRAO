import skrf as rf

from simulation.floquet_line_models.models.abstract_floquet_line import floquet_abs, floquet_base
from simulation.utills.functions import Transmission_Db


class hfss_touchstone_floquet_line(floquet_abs, floquet_base):

    def __init__(self, hfss_touchstone_file_path, n_interp_points, unit_cell_length, n_repeated_unit_cells):

        self.unit_cell_ABCD_mats, self.frequency_range_simulated_over = self.get_abcd_mats_and_frequency_range_from_hfss_touchstone_file(
            hfss_touchstone_file_path, n_interp_points)
        self.n_repeated_unit_cells = n_repeated_unit_cells
        self.impedance = 50
        self.unit_cell_length = unit_cell_length

    def get_resolution(self):
        return len(self.frequency_range_simulated_over)

    def get_unit_cell_length(self):
        return self.unit_cell_length

    def get_abcd_mats_and_frequency_range_from_hfss_touchstone_file(self, hfss_touchstone_file_path: str,
                                                                    n_interp_points: int = 1000):
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

    def simulate_over_frequency_range(self):

        # could make this a pandas df
        gamma_d = []
        bloch_impedance = []
        central_line_beta_d = [0] * len(self.unit_cell_ABCD_mats)
        central_line_alpha_d = [0] * len(self.unit_cell_ABCD_mats)

        floquet_transmission = []
        for unit_cell_abcd_mat in self.unit_cell_ABCD_mats:
            # 6) calculate all the needed outputs
            # calc bloch impedance and propagation const for unit cell

            floquet_gamma_d = self.gamma_d(unit_cell_abcd_mat)
            ZB = self.bloch_impedance_Zb(unit_cell_abcd_mat)

            floquet_transmission_ = Transmission_Db(self.n_repeated_unit_cells,
                                                    self.impedance,
                                                    ZB,
                                                    floquet_gamma_d)
            floquet_transmission.append(floquet_transmission_)
            gamma_d.append(floquet_gamma_d)
            bloch_impedance.append(ZB)




        return self.frequency_range_simulated_over, gamma_d, bloch_impedance, central_line_alpha_d, central_line_beta_d, floquet_transmission
