import cmath
import numpy as np
from scipy.signal import find_peaks, peak_widths

from simulation.floquet_line_model.unit_cell import UnitCell, mk_ABCD_Mat
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.transmission_line_models.abstract_super_conducting_line_model import AbstractSCTL
from simulation.utills.functions import Transmission

# calc transmission todo add these inputs to UI
N_unit_cells = 150
impedance = 50


# todo some refactoring and document all

class SuperConductingFloquetLine():

    def __init__(self, unit_cell_length: float, D0: float, load_lengths: [float], load_line_models: [AbstractSCTL],
                     central_line_model: AbstractSCTL, super_conductivity_model: SuperConductivity,
                 central_line_width: float, load_widths: [float], line_thickness: float):
        # ---------------------------------------------------------

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


    def Bloch_impedance_Zb(self, ABCD_mat_2x2: [[float]]):
        A = ABCD_mat_2x2[0][0]
        B = ABCD_mat_2x2[0][1]
        D = ABCD_mat_2x2[1][1]

        ADs2 = cmath.sqrt(((A + D) ** 2) - 4)
        ADm = A - D

        B2 = 2 * B

        ZB = - (B2 / (ADm + ADs2))
        ZB2 = - (B2 / (ADm - ADs2))
        if ZB.real < 0:
            ZB = ZB2
        return ZB

    def gamma_d(self, ABCD_mat_2x2: [[float]]):
        A = ABCD_mat_2x2[0][0]
        D = ABCD_mat_2x2[1][1]
        return np.arccosh(((A + D) / 2))

    def FindPumpZone(self, peak_number: int, alphas: [float]):
        x = np.array(alphas)
        peaks, _ = find_peaks(x, prominence=.005)

        if len(peaks) < peak_number:
            self.target_pump_zone_start, self.target_pump_zone_end = 0, 0
            return

        y, self.target_pump_zone_start, self.target_pump_zone_end = \
            list(zip(*peak_widths(x, peaks, rel_height=.95)[1:]))[max(peak_number - 1, 0)]

    def simulate(self, frequency):
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
        ZB = self.Bloch_impedance_Zb(unit_cell_abcd_mat)
        floquet_gamma_d = self.gamma_d(unit_cell_abcd_mat)

        floquet_transmission = Transmission(N_unit_cells,
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