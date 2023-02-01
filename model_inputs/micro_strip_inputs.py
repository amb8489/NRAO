from python_gui.utills.utills_gui import resolution, start_frequency
from utills.functions import micro_meters_to_meters, nano_meters_to_meters, toGHz


class MicroStripInputs():
    def __init__(self, inputs):
        # ---------------------------- Range and Resolution Inputs

        #todo change thse to
        self.resoultion = int(inputs["Frequency Range"][resolution.get_name()])
        self.start_freq_GHz = toGHz(int(inputs["Frequency Range"][start_frequency.get_name()]))
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






        # temp = self.__dict__.copy()
        #
        # # ---------------------------- range and resolution inputs
        # self.resoultion = 1700
        # self.start_freq_GHz = toGHz(1)
        # self.end_freq_GHz = toGHz(25)
        #
        # # ---------------------------- unit cell inputs
        #
        # self.unit_cell_length = micro_meters_to_meters(2300)
        # self.central_line_width = micro_meters_to_meters(1.49)
        #
        # self.load1_width = self.central_line_width * 1.2
        # self.load2_width = self.central_line_width * 1.2
        # self.load3_width = self.central_line_width * 1.2
        #
        # self.load_widths = [self.load1_width, self.load2_width, self.load3_width]
        #
        # self.D0 = .000766666666666666666
        # self.D1 = 5e-5
        # self.D2 = 5e-5
        # self.D3 = .0001
        # self.load_lengths = [self.D1, self.D2, self.D3]
        # self.number_of_loads = len(self.load_lengths)
        #
        # # ---------------------------- SC inputs
        # self.er = 10
        #
        # # todo question: why is this height diff from FL dims height
        # self.height = nano_meters_to_meters(250)
        # self.line_thickness = nano_meters_to_meters(60)
        # self.ground_thickness = nano_meters_to_meters(300)
        # self.crit_temp = 14.28
        # self.op_temp = 4
        # self.normal_resistivity = 1.008e-6
        # self.tangent_delta = 0
        # self.crit_current = 200000000
        #
        # # ---------------------------- gain_models inputs
        # # todo make inputs complex
        #
        # self.As_init = 100000
        # self.Ai_init = 1309
        # self.Ap_init = 3
        # self.pump_freq = 6.772e9
        #
        # self.init_amplitudes = (self.As_init, self.Ai_init, self.Ap_init)
        #
        # print("vales 2", self.__dict__)
        #
        # for k, v in self.__dict__.items():
        #     if self.__dict__[k] != temp[k]:
        #         print(f"{k} {self.__dict__[k]} != {temp[k]}")
