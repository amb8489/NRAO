import time

from matplotlib import pyplot as plt

from floquet_line_model.floquet_line import SuperConductingFloquetLine
from gain_models.find_gain import Calc_Gain
from model_inputs.cpw_inputs import CPWInputs
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.cpw.super_conducting_cpw_model import SuperConductingCPWLine

if __name__ == "__main__":

    json_inputs = {'SC': {'Er': 11.44, 'Height': 0.0, 'Ts': 35.0, 'Ground Thickness': 0.0,
                      'Super Conductor Operation Temperature': 4.0, 'Super Conductor Critical Temperature': 14.7,
                      'Super Conductor Critical Current': 0.0, 'Super Conductor Normal Resistivity': 100.0,
                      'Super Conductor Tangent Delta': 0.0},
               'Dimensions': {'loads': [['60', '3.4'], ['60', '3.4'], ['50', '3.4']], 'Unit Cell Length': 4.734,
                              'Central Line Width': 1.0, 'D0': 1.578, 'S': 1.0},
               'Frequency Range': {'Start Frequency': 0.0, 'End Frequency': 40.0, 'Resolution': 1000.0},
               'gain_models': {'Signal Amplitude': .000000001, 'Idler Amplitude': .000001, 'Pump Amplitude': .2,
                               'Pump Frequency': 11.63}}

    inputs = CPWInputs(json_inputs)
    super_conductivity_model = SuperConductivity(inputs.op_temp, inputs.crit_temp, inputs.normal_resistivity)
    Central_line_model = SuperConductingCPWLine(inputs.central_line_width, inputs.ground_spacing,
                                                inputs.line_thickness, inputs.er, inputs.tangent_delta,200)
    Load_line_models = [SuperConductingCPWLine(load_width, inputs.ground_spacing, inputs.line_thickness, inputs.er,
                                               inputs.tangent_delta,200) for load_width in inputs.load_widths]
    floquet_line = SuperConductingFloquetLine(inputs.unit_cell_length, inputs.D0, inputs.load_D_vals, Load_line_models,
                                              Central_line_model, super_conductivity_model, inputs.central_line_width,
                                              inputs.load_widths, inputs.line_thickness)

    # step 3) gain

    """
    The term I∗ is proportional to I∗′/√α∗, where I∗′ is floquet_alpha parameter comparable to the critical current ic, and α∗ is 
    the ratio of kinetic inductance to total inductance.
    
    """

    start_time = time.time()
    L = 500
    f_range, gain = Calc_Gain(floquet_line, inputs.resoultion, inputs.pump_freq, inputs.init_amplitudes, L)
    print("time to calc gains:", (time.time() - start_time))
    plt.plot(f_range, gain)
    plt.show()
