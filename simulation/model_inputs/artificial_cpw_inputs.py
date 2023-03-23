from python_gui.utills.utills_gui import resolution, start_frequency, end_frequency, Er, pump_frequency, pump_amplitude, \
    idler_amplitude, signal_amplitude, SC_tangent_delta, \
    SC_normal_resistivity, SC_critical_current, SC_critical_temperature, SC_operation_temperature, SC_ground_thickness, \
    SC_thickness, SC_height, n_repeated_cells
from simulation.utills.functions import hertz_to_GHz, nano_meters_to_meters, micro_meters_to_meters, micro_ohms_cm_to_ohms_m


class ArtificialCPWInputs():



    #todo could simplify because S == WH == LH == LL and wu and Wl of the loads are what else is needed
    def __init__(self, inputs: dict):
        # ---------------------------- Range and Resolution Inputs

        self.resoultion = int(inputs["Frequency Range"][resolution.get_name()])
        self.start_freq_GHz = hertz_to_GHz(int(inputs["Frequency Range"][start_frequency.get_name()]))
        self.end_freq_GHz = hertz_to_GHz(int(inputs["Frequency Range"][end_frequency.get_name()]))

        # ---------------------------- gain_models inputs
        self.pump_frequency = hertz_to_GHz(float(inputs["gain_models"][pump_frequency.get_name()]))
        self.As_init = complex(float(inputs["gain_models"][signal_amplitude.get_name()]), 0)
        self.Ai_init = complex(float(inputs["gain_models"][idler_amplitude.get_name()]), 0)
        self.Ap_init = complex(float(inputs["gain_models"][pump_amplitude.get_name()]), 0)
        self.init_amplitudes = (self.As_init, self.Ai_init, self.Ap_init)
        self.calc_gain =  bool(inputs["gain_models"]["calc_gain"])
        # ---------------------------- Super Conductor Inputs
        self.er = float(inputs["SC"][Er.get_name()])
        self.height = nano_meters_to_meters(float(inputs["SC"][SC_height.get_name()]))
        self.line_thickness = nano_meters_to_meters(float(inputs["SC"][SC_thickness.get_name()]))
        self.ground_thickness = micro_meters_to_meters(float(inputs["SC"][SC_ground_thickness.get_name()]))
        self.op_temp = float(inputs["SC"][SC_operation_temperature.get_name()])
        self.crit_temp = float(inputs["SC"][SC_critical_temperature.get_name()])
        self.crit_current = float(inputs["SC"][SC_critical_current.get_name()])
        self.normal_resistivity = micro_ohms_cm_to_ohms_m(float(inputs["SC"][SC_normal_resistivity.get_name()]))
        self.tangent_delta = float(inputs["SC"][SC_tangent_delta.get_name()])

        # Line Dimensions
        self.line_dimensions = [[
            micro_meters_to_meters(float(line_len)),
            micro_meters_to_meters(float(S)),
            micro_meters_to_meters(float(WH)),
            micro_meters_to_meters(float(LH)),
            micro_meters_to_meters(float(WL)),
            micro_meters_to_meters(float(LL))] for line_len, S, WH, LH, WL, LL in inputs["Dimensions"]["loads"]]


        # transmission and transmission
        self.n_repeated_cells = int(inputs["Frequency Range"][n_repeated_cells.get_name()])
