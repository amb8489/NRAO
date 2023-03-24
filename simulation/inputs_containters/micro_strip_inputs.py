from python_gui.utills.utills_gui import resolution, start_frequency, end_frequency, unit_cell_length, \
    central_line_width, D0, Er, pump_frequency, pump_amplitude, idler_amplitude, signal_amplitude, SC_tangent_delta, \
    SC_normal_resistivity, SC_critical_current, SC_critical_temperature, SC_operation_temperature, SC_ground_thickness, \
    SC_thickness, SC_height, n_repeated_cells
from simulation.utills.functions import hertz_to_GHz, mm_to_meters, micro_meters_to_meters, micro_ohms_cm_to_ohms_m, \
    nano_meters_to_meters


# todo also refactor to use .get(key,None) to prevent error on bad key

class MicroStripInputs():
    def __init__(self, inputs: dict):
        # ---------------------------- Range and Resolution Inputs

        self.resoultion = int(inputs["Frequency Range"][resolution.get_name()])
        self.start_freq_GHz = hertz_to_GHz(int(inputs["Frequency Range"][start_frequency.get_name()]))
        self.end_freq_GHz = hertz_to_GHz(int(inputs["Frequency Range"][end_frequency.get_name()]))

        # todo convert to right units
        # todo refactor so that unit_cell_length holds its value and is connected to the change of the widget that represents its value
        # ---------------------------- Unit Cell Dimensions

        self.unit_cell_length = mm_to_meters(float(inputs["Dimensions"][unit_cell_length.get_name()]))
        self.central_line_width = micro_meters_to_meters(float(inputs["Dimensions"][central_line_width.get_name()]))
        self.D0 = mm_to_meters(float(inputs["Dimensions"][D0.get_name()]))

        self.load_D_vals, self.load_widths = [], []
        for D_len, width in inputs["Dimensions"]["loads"]:
            self.load_D_vals.append(micro_meters_to_meters(float(D_len)))
            self.load_widths.append(micro_meters_to_meters(float(width)))
        self.number_of_loads = len(self.load_D_vals)

        # ---------------------------- Super Conductor Inputs
        self.er = float(inputs["SC"][Er.get_name()])
        self.height = nano_meters_to_meters(float(inputs["SC"][SC_height.get_name()]))
        self.line_thickness = nano_meters_to_meters(float(inputs["SC"][SC_thickness.get_name()]))
        self.ground_thickness = nano_meters_to_meters(float(inputs["SC"][SC_ground_thickness.get_name()]))
        self.op_temp = float(inputs["SC"][SC_operation_temperature.get_name()])
        self.crit_temp = float(inputs["SC"][SC_critical_temperature.get_name()])
        self.crit_current = float(inputs["SC"][SC_critical_current.get_name()])
        self.normal_resistivity = micro_ohms_cm_to_ohms_m(float(inputs["SC"][SC_normal_resistivity.get_name()]))
        self.tangent_delta = float(inputs["SC"][SC_tangent_delta.get_name()])








        # ---------------------------- gain_models inputs
        self.pump_frequency = hertz_to_GHz(float(inputs["gain_models"][pump_frequency.get_name()]))
        self.As_init = complex(float(inputs["gain_models"][signal_amplitude.get_name()]), 0)
        self.Ai_init = complex(float(inputs["gain_models"][idler_amplitude.get_name()]), 0)
        self.Ap_init = complex(float(inputs["gain_models"][pump_amplitude.get_name()]), 0)
        self.init_amplitudes = (self.As_init, self.Ai_init, self.Ap_init)
        self.calc_gain =  bool(inputs["gain_models"]["calc_gain"])

        # transmission and transmission
        self.n_repeated_cells = int(inputs["Frequency Range"][n_repeated_cells.get_name()])
