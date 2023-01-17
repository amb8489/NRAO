import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.MicroStrip.FloquetLine import SuperConductingFloquetLine
from Gain.MicroStrip.FindGain import Calc_Gain
from Gain.MicroStrip.solveODEs import Solve_ode
from Gain.AmplitudeEquations.AmplitudeEquations1 import AmplitudeEqs1
from Inputs.MicroStripInputs import MicroStripInputs
from SuperConductivityEquations.SCE import SuperConductivity
from TransmissionLineEquations.MicroStrip.SC_MicroStrip_TL import SuperConductingMicroStripModel






if __name__ == "__main__":
    # INPUTS FROM Parametric-amplification-of-electromagnetic-signals-with-superconducting-transmission-lines.pdf on MS

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
    The term I∗ is proportional to I∗′/√α∗, where I∗′ is a parameter comparable to the critical current ic, and α∗ is 
    the ratio of kinetic inductance to total inductance.
    
    """


    start_time = time.time()
    L = 500 #todo where does L comefrom in mathimatica
    f_range, gain = Calc_Gain(floquet_line, MSinputs.resoultion, MSinputs.pump_freq,MSinputs.init_amplitudes, L)
    print("time to calc gains:", (time.time() - start_time))
    plt.plot(f_range, gain)
    plt.show()