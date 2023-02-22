'''
Testing file for calculating A B R X
'''
import time

import numpy as np
from matplotlib import pyplot as plt

from floquet_line_model.floquet_line import SuperConductingFloquetLine
from model_inputs.cpw_inputs import CPWInputs
from python_gui.utills.utills_gui import resolution, start_frequency, end_frequency
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.cpw.super_conducting_cpw_model import SuperConductingCPWLine
from utills.functions import toGHz, unfold


# ---------------------------- unit cell inputs from paper


def simulate():
    inputs = {'SC': {'Er': 11.44, 'Height': 0.0, 'Ts': 20.0, 'Ground Thickness': 0.0,
                     'Super Conductor Operation Temperature': 0.0, 'Super Conductor Critical Temperature': 15.83,
                     'Super Conductor Critical Current': 0.0, 'Super Conductor Normal Resistivity': 95.0,
                     'Super Conductor Tangent Delta': 1e-10},
              'Dimensions': {'loads': [['60', '14'], ['60', '14'], ['50', '14']], 'Unit Cell Length': 5.386,
                             'Central Line Width': 2.0, 'D0': 1.795, 'S': 2.0},
              'Frequency Range': {'Start Frequency': 1.0, 'End Frequency': 40.0, 'Resolution': 1000.0},
              'gain_models': {'Signal Amplitude': 0.0, 'Idler Amplitude': 0.0, 'Pump Amplitude': 0.0,
                              'Pump Frequency': 0.0}}

    inputs = CPWInputs(inputs)

    super_conductivity_model = SuperConductivity(inputs.op_temp, inputs.crit_temp, inputs.normal_resistivity)
    central_line_model = SuperConductingCPWLine(inputs.central_line_width, inputs.ground_spacing, inputs.line_thickness,
                                                inputs.er, inputs.tangent_delta)
    load_line_models = [SuperConductingCPWLine(load_width, inputs.ground_spacing, inputs.line_thickness, inputs.er,
                                               inputs.tangent_delta) for load_width in inputs.load_widths]
    floquet_line = SuperConductingFloquetLine(inputs.unit_cell_length, inputs.D0, inputs.load_D_vals,
                                              load_line_models, central_line_model, super_conductivity_model,
                                              inputs.central_line_width, inputs.load_widths, inputs.line_thickness,
                                              inputs.crit_current)
    # ---------------------------- calculations -------------------
    alpha_plt, r, x, beta_plt, beta_unfold_plt, RR, LL, GG, CC, gamma, transmission_plt = [], [], [], [], [], [], [], [], [], [], []
    cl_beta = []
    cl_alpha = []

    resoultion = 10000
    start_freq_GHz = toGHz(1)
    end_freq_GHz = toGHz(40)

    # todo
    FRange = np.linspace(start_freq_GHz, end_freq_GHz, resoultion)

    start = time.time()
    trials = 10
    for i in range(trials):
        for F in FRange:
            alpha, beta, alphaCl, betaCL, r_, x_ = floquet_line.simulate(F)


    print((time.time() - start)/trials)

    plt.show()

simulate()
