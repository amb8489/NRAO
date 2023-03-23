from python_gui.utills.utills_gui import signal_amplitude, pump_frequency, idler_amplitude, pump_amplitude
from simulation.utills.functions import hertz_to_GHz


class pre_sim_file_inputs():

    def __init__(self,inputs: dict):
        self.wl_microns = float(inputs["wl_len"])
        self.wu_microns = float(inputs["wu_len"])
        self.Lu_microns = float(inputs["Lu_length"])
        self.dimensions = inputs["Dimensions_inputs"]["loads"]

        self.is_art_cpw_line = bool(inputs["using_art_line"])

        self.n_interpt_points = inputs.get("n_interpt_points")
        self.unit_cell_length = inputs.get("unit_cell_length")
        self.n_repeated_cells = inputs.get("Frequency_Range").get("n_repeated_cells",150)




        self.start_freq = hertz_to_GHz(float(inputs["Frequency_Range"]["Start Frequency"]))
        self.end_freq = hertz_to_GHz(float(inputs["Frequency_Range"]["End Frequency"]))
        self.resolution = int(inputs["Frequency_Range"]["Resolution"])


        # ---------------------------- gain_models inputs
        self.pump_frequency = hertz_to_GHz(float(inputs["gain_models"][pump_frequency.get_name()]))
        self.As_init = complex(float(inputs["gain_models"][signal_amplitude.get_name()]), 0)
        self.Ai_init = complex(float(inputs["gain_models"][idler_amplitude.get_name()]), 0)
        self.Ap_init = complex(float(inputs["gain_models"][pump_amplitude.get_name()]), 0)
        self.init_amplitudes = (self.As_init+0j, self.Ai_init+0j, self.Ap_init+0j)
        self.calc_gain =  bool(inputs["gain_models"]["calc_gain"])










