import numpy as np
from scipy.integrate import solve_ivp

from floquet_line_model.floquet_line import SuperConductingFloquetLine
from model_inputs.cpw_inputs import CPWInputs
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.cpw.super_conducting_cpw_model import SuperConductingCPWLine


def ODE_model_1(z, inital_amplitudes, arg1, arg2, arg3):
    as0, ai0, ap0 = inital_amplitudes
    return []


def solve(z_span, inital_amplitudes, args, t_eval):
    # todo dont know about t_eval to e z or frequency
    sol = solve_ivp(fun=ODE_model_1, t_span=z_span, y0=inital_amplitudes, args=args, t_eval=t_eval)
    return sol


json_inputs = {'SC': {'Er': 11.44, 'Height': 0.0, 'Ts': 35.0, 'Ground Thickness': 0.0,
                      'Super Conductor Operation Temperature': 4.0, 'Super Conductor Critical Temperature': 14.7,
                      'Super Conductor Critical Current': 0.0, 'Super Conductor Normal Resistivity': 100.0,
                      'Super Conductor Tangent Delta': 0.0},
               'Dimensions': {'loads': [['60', '3.4'], ['60', '3.4'], ['50', '3.4']], 'Unit Cell Length': 4.734,
                              'Central Line Width': 1.0, 'D0': 1.578, 'S': 1.0},
               'Frequency Range': {'Start Frequency': 0.0, 'End Frequency': 40.0, 'Resolution': 1000.0},
               'gain_models': {'Signal Amplitude': 0.0, 'Idler Amplitude': 0.0, 'Pump Amplitude': 0.0,
                               'Pump Frequency': 0.0}}

inputs = CPWInputs(json_inputs)

super_conductivity_model = SuperConductivity(inputs.op_temp, inputs.crit_temp, inputs.normal_resistivity)

central_line_model = SuperConductingCPWLine(inputs.central_line_width, inputs.ground_spacing,
                                            inputs.line_thickness, inputs.er, inputs.tangent_delta)
load_line_models = [SuperConductingCPWLine(load_width, inputs.ground_spacing, inputs.line_thickness, inputs.er,
                                           inputs.tangent_delta) for load_width in inputs.load_widths]

floquet_line = SuperConductingFloquetLine(inputs.unit_cell_length, inputs.D0, inputs.load_D_vals,
                                          load_line_models, central_line_model, super_conductivity_model,
                                          inputs.central_line_width, inputs.load_widths, inputs.line_thickness,
                                          inputs.crit_current)

########################################################################################
t_eval = np.linspace(0, floquet_line.unit_cell.unit_cell_length, inputs.resoultion)
z_span = (t_eval[0], t_eval[-1])
PUMP_FREQUENCY = 11.63
########################################################################################


frequency_range = np.linespace(inputs.start_freq_GHz, inputs.end_freq_GHz, inputs.resoultion)
for frequency in frequency_range:
    as0, ai0, ap0 = [..., ..., ...]
    inital_amplitudes = [as0, ai0, ap0]
    args = (..., ..., ...)
    sol = solve(z_span, inital_amplitudes, args, t_eval)
