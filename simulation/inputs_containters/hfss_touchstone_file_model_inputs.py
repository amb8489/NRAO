from python_gui.utills.utills_gui import signal_amplitude, pump_frequency, idler_amplitude, pump_amplitude
from simulation.utills.functions import hertz_to_GHz


class hfss_touchstone_file_model_inputs():

    def __init__(self,inputs: dict):


        self.hfss_touchstone_file_path = inputs.get("hfss_touchstone_file_path")
        self.n_interpt_points = inputs.get("n_interpt_points")
        self.unit_cell_length = inputs.get("unit_cell_length")
        self.n_repeated_cells = inputs.get("n_repeated_cells")

        # ---------------------------- gain_models inputs
        self.pump_frequency = hertz_to_GHz(float(inputs["gain_models"][pump_frequency.get_name()]))
        self.As_init = complex(float(inputs["gain_models"][signal_amplitude.get_name()]), 0)
        self.Ai_init = complex(float(inputs["gain_models"][idler_amplitude.get_name()]), 0)
        self.Ap_init = complex(float(inputs["gain_models"][pump_amplitude.get_name()]), 0)
        self.init_amplitudes = (self.As_init, self.Ai_init, self.Ap_init)
        self.calc_gain =  bool(inputs["gain_models"]["calc_gain"])










