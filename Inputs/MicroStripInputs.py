from Utills.Functions import micro_meters_to_meters, nano_meters_to_meters, toGHz


class MicroStripInputs():
    def __init__(self):
        # ---------------------------- range and resolution inputs
        self.resoultion = 1000
        self.start_freq_GHz = toGHz(1)
        self.end_freq_GHz = toGHz(25)

        # ---------------------------- unit cell inputs

        self.unit_cell_length = micro_meters_to_meters(2300)
        self.l1 = micro_meters_to_meters(50)
        self.central_line_width = micro_meters_to_meters(1.49)

        self.load1_width = self.central_line_width * 1.2
        self.load2_width = self.central_line_width * 1.2
        self.load3_width = self.central_line_width * 1.2

        self.load_widths = [self.load1_width, self.load2_width, self.load3_width]

        self.D0 = .000766666666666666666
        self.D1 = 5e-5
        self.D2 = 5e-5
        self.D3 = .0001
        self.load_lengths = [self.D1, self.D2, self.D3]
        self.number_of_loads = len(self.load_lengths)

        # ---------------------------- SC inputs
        self.er = 10

        # todo question: why os this height diff from FL dims height
        self.height = nano_meters_to_meters(250)
        self.line_thickness = nano_meters_to_meters(60)
        self.ground_thickness = nano_meters_to_meters(300)
        self.crit_temp = 14.28
        self.op_temp = 4
        self.normal_resistivity = 1.008e-6
        self.tangent_delta = 0
        self.crit_current = 200000000

        # ---------------------------- Gain inputs
        # todo make inputs complex

        self.As_init = 100000
        self.Ai_init = 1309
        self.Ap_init = 3
        self.pump_freq = 6.772e9

        self.init_amplitudes = (self.As_init, self.Ai_init, self.Ap_init)
