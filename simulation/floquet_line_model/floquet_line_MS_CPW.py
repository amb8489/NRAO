import numpy as np

from simulation.floquet_line_model.abstract_floquet_line import floquet_abs, floquet_base
from simulation.floquet_line_model.unit_cell import UnitCell, mk_ABCD_Mat
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

        self.IC = central_line_model.IC
        # ---------------------------- model of the Super conductor

        self.super_conductivity_model = super_conductivity_model

        # ---------------------------- unit cell inputs
        self.central_Line_width = central_line_width

        # todo are these even being used in any calculations
        self.load_widths = load_widths

        # model of the dimensions for the floquet line
        self.unit_cell = UnitCell(unit_cell_length, D0, load_lengths, central_line_model,
                                  line_thickness, load_line_models)

        self.target_pump_zone_start = 0
        self.target_pump_zone_end = 0

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

        # get alpha beta r x
        floquet_beta = floquet_gamma_d.imag
        floquet_alpha = floquet_gamma_d.real

        floquet_r = ZB.real
        floquet_x = ZB.imag

        # calculate central line alpha and beta
        central_line_gamma, central_line_characteristic_impedance = self.unit_cell.get_segment_gamma_and_characteristic_impedance(
            0, frequency, surface_impedance)

        central_line_mat = mk_ABCD_Mat(central_line_characteristic_impedance, central_line_gamma,
                                       self.unit_cell.unit_cell_length)
        central_line_propagation_const = self.gamma_d(central_line_mat)
        central_line_beta = central_line_propagation_const.imag
        central_line_alpha = central_line_propagation_const.real

        # retuning outputs
        return [floquet_alpha, floquet_beta, central_line_alpha, central_line_beta, floquet_r, floquet_x,
                floquet_transmission]

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

        frequency_range = np.linspace(self.start_freq_GHz, self.end_freq_GHz, self.resolution)
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
