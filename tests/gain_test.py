import time

from floquet_line_model.MicroStrip.FloquetLine import SuperConductingFloquetLine
from gain_models.microstrip.find_gain import Calc_Gain
from matplotlib import pyplot as plt

from model_inputs.micro_strip_inputs import MicroStripInputs
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.micro_strip.super_conducting_micro_strip_model import SuperConductingMicroStripModel

if __name__ == "__main__":
    # INPUTS FROM Parametric-amplification-of-electromagnetic-signals-with-superconducting-transmission_plt-lines.pdf on MS

    MSinputs = MicroStripInputs()

    # ---------------------------- dependency models ----------------------------
    super_conductivity_model = SuperConductivity(MSinputs.op_temp, MSinputs.crit_temp, MSinputs.normal_resistivity)
    Central_line_model = SuperConductingMicroStripModel(MSinputs.height, MSinputs.central_line_width,
                                                        MSinputs.line_thickness, MSinputs.er, MSinputs.tangent_delta,
                                                        MSinputs.crit_current)
    Load_line_models = [
        SuperConductingMicroStripModel(MSinputs.height, width, MSinputs.line_thickness, MSinputs.er,
                                       MSinputs.tangent_delta,
                                       MSinputs.crit_current) for width in MSinputs.load_widths]

    floquet_line = SuperConductingFloquetLine(MSinputs.unit_cell_length, MSinputs.D0, MSinputs.load_lengths,
                                              Load_line_models,
                                              Central_line_model,
                                              super_conductivity_model, MSinputs.central_line_width,
                                              MSinputs.load_widths,
                                              MSinputs.line_thickness, MSinputs.crit_current)

    # ---------------------------- gain inputs

    """
    The term I∗ is proportional to I∗′/√α∗, where I∗′ is alpha_plt parameter comparable to the critical current ic, and α∗ is 
    the ratio of kinetic inductance to total inductance.
    
    """

    start_time = time.time()
    L = 500  # todo where does L comefrom in mathimatica
    f_range, gain = Calc_Gain(floquet_line, MSinputs.resoultion, MSinputs.pump_freq, MSinputs.init_amplitudes, L)
    print("time to calc gains:", (time.time() - start_time))
    plt.plot(f_range, gain)
    plt.show()
