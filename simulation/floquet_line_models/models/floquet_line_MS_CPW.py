import numpy as np

from simulation.floquet_line_models.models.abstract_floquet_line import floquet_base, floquet_abs
from simulation.floquet_line_models.unit_cell import UnitCell, mk_ABCD_Mat
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.functions import Transmission_Db

# calc transmission todo add these inputs to UI
N_unit_cells = 150
impedance = 50


# todo some refactoring and document all



class SuperConductingFloquetLine(floquet_abs, floquet_base):

    def __init__(self, unit_cell_length: float, D0: float, load_lengths: [float], load_line_models: [AbstractSCTL],
                 central_line_model: AbstractSCTL, super_conductivity_model: SuperConductivity,
                 central_line_width: float, load_widths: [float], line_thickness: float, start_freq_GHz: float,
                 end_freq_GHz: float, resolution: int):
        # ---------------------------------------------------------

        self.resolution = resolution
        self.start_freq_GHz = start_freq_GHz
        self.end_freq_GHz = end_freq_GHz

        # ---------------------------- model of the Super conductor

        self.super_conductivity_model = super_conductivity_model

        # ---------------------------- unit cell inputs
        self.central_Line_width = central_line_width

        self.load_widths = load_widths

        # model of the dimensions for the floquet line
        self.unit_cell = UnitCell(unit_cell_length, D0, load_lengths, central_line_model,
                                  line_thickness, load_line_models)




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
