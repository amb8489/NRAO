import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.MicroStrip.FloquetLine import SuperConductingFloquetLine
from Gain.MicroStrip.solveODEs import Solve_ode
from Gain.AmplitudeEquations.AmplitudeEquations1 import AmplitudeEqs1
from Inputs.MicroStripInputs import MicroStripInputs
from SuperConductivityEquations.SCE import SuperConductivity
from TransmissionLineEquations.MicroStrip.SC_MicroStrip_TL import SuperConductingMicroStripModel
from Utills.Functions import nano_meters_to_meters, micro_meters_to_meters


# steps todo
#   calc beta for given range and resolution
#   calc beta at pumpFreq
#   calc beta for all pumpFreqs and idler freqencys
#   calc for each freq the gain using betas calced above and other init vars


def calcGain(As_init, Ai_init, Ap_init, pump_freq, d, Floquet_line, resolution, I):
    # calc signal freq up to pump_freqTimes2
    betas = []
    f_range = np.linspace(1e9, 2 * pump_freq, resolution)
    for i, signal_freq in enumerate(f_range):
        aa, bta_unfolded, bta, rr, xx, R, L, G, C = Floquet_line.abrx(signal_freq)
        betas.append(bta_unfolded)

    # todo make sure that this freq approximization is okay to do
    beta_pump = betas[np.searchsorted(f_range, pump_freq)]

    z = np.linspace(0, d, resolution)
    Times2PumpFreq = (2 * pump_freq)
    gain = []
    L = resolution // 2
    s = time.time()

    init_vals_arr = [As_init, Ai_init, Ap_init]
    for i, signal_freq in enumerate(f_range):
        # get index for signal and idler freqs inside beta array
        idler_freq = Times2PumpFreq - signal_freq
        # todo opt this could be done in np for each freq then use idx to pass in from calculated arr
        idx_sig, idx_idler = np.searchsorted(f_range, [signal_freq, idler_freq])
        beta_s = betas[idx_sig]  # get beta for signal freq
        beta_i = betas[idx_idler]  # get beta for idel freq

        AmplitudeEqs1Args = (beta_s, beta_i, beta_pump, I)
        g = Solve_ode(init_vals_arr, AmplitudeEqs1, AmplitudeEqs1Args, z, L)
        gain.append(np.log10(g))

    print("time to calc gains:", (time.time() - s))
    print(f"time taken {time.time() - s}")
    plt.plot(f_range, gain)
    plt.show()


if __name__ == "__main__":
    # INPUTS FROM Parametric-amplification-of-electromagnetic-signals-with-superconducting-transmission-lines.pdf on MS

    MSinputs = MicroStripInputs()

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

    Floquet_line = SuperConductingFloquetLine(MSinputs.unit_cell_length, MSinputs.D0, MSinputs.load_lengths,
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

    calcGain(MSinputs.As_init, MSinputs.Ai_init, MSinputs.Ap_init, MSinputs.pump_freq, MSinputs.unit_cell_length, Floquet_line, MSinputs.resoultion)
