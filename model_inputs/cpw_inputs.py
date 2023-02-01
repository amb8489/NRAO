from utills.functions import micro_meters_to_meters, nano_meters_to_meters, toGHz


class CPWInputs():
    def __init__(self, inputs):
        # ---------------------------- Range and Resolution Inputs
        self.resoultion = int(inputs["Frequency Range"]["Resolution"])
        self.start_freq_GHz = toGHz(int(inputs["Frequency Range"]["Start Freq [GHZ]"]))
        self.end_freq_GHz = toGHz(int(inputs["Frequency Range"]["End Freq [GHZ]"]))

        # ---------------------------- Unit Cell Dimensions
        self.unit_cell_length = micro_meters_to_meters(float(inputs["Dimensions"]["Unit Cell Length []"]))
        self.central_line_width = micro_meters_to_meters(float(inputs["Dimensions"]["Central Line Width []"]))
        self.D0 = float(inputs["Dimensions"]["D0"])
        self.load_lengths = []
        self.load_widths = []
        for length, width in inputs["Dimensions"]["loads"]:
            self.load_lengths.append(float(length))
            self.load_widths.append(float(width))

        self.number_of_loads = len(self.load_lengths)

        # ---------------------------- Super Conductor Inputs
        self.er = float(inputs["SC"]["Er"])
        self.height = nano_meters_to_meters(float(inputs["SC"]["H"]))
        self.line_thickness = nano_meters_to_meters(float(inputs["SC"]["Ts"]))
        self.ground_thickness = nano_meters_to_meters(float(inputs["SC"]["Tg"]))
        self.op_temp = float(inputs["SC"]["T"])
        self.crit_temp = float(inputs["SC"]["Tc"])
        self.crit_current = float(inputs["SC"]["Jc"])
        self.normal_resistivity = float(inputs["SC"]["Normal Resistivity"])
        self.tangent_delta = float(inputs["SC"]["Tan D"])

        # ---------------------------- gain_models inputs
        self.As_init = float(inputs["gain_models"]["As0"])  # todo make inputs complex
        self.Ai_init = float(inputs["gain_models"]["Ai0"])  # todo make inputs complex
        self.Ap_init = float(inputs["gain_models"]["Ap0"])  # todo make inputs complex
        self.pump_freq = float(inputs["gain_models"]["Pump Frequency [GHZ]"])
        self.init_amplitudes = (self.As_init, self.Ai_init, self.Ap_init)



