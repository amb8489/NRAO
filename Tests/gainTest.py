import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.MicroStrip.FloquetLine import SuperConductingFloquetLine
from Gain.MicroStrip.solveODEs import Solve_ode
from Gain.AmplitudeEquations.AmplitudeEquations1 import AmplitudeEqs1
from SuperConductivityEquations.SCE import SuperConductivity
from TransmissionLineEquations.MicroStrip.SC_MicroStrip_TL import SuperConductingMicroStripModel
from Utills.Functions import nanoMeters_to_Meters, microMeters_to_Meters


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

    StartFreq, EndFreq, resolution = 1e9, 7e9, 1000
    # ---------------------------- unit cell inputs from paper
    unit_Cell_Len = microMeters_to_Meters(2300)
    l1 = microMeters_to_Meters(50)
    width_unloaded = microMeters_to_Meters(1.49)
    width_loaded = width_unloaded * 1.2

    D0 = .0007666666666666666666
    D1 = 5e-5
    D2 = 5e-5
    D3 = .0001
    loads_Widths = [D1, D2, D3]
    number_of_loads = len(loads_Widths)

    # ---------------------------- SC inputs
    er = 10
    Height = nanoMeters_to_Meters(250)
    line_thickness = nanoMeters_to_Meters(60)
    ground_thickness = nanoMeters_to_Meters(300)
    Tc = 14.28
    T = 4
    pn = 1.008e-6
    tanD = 0
    Jc = 1

    # secoind paper inputs
    # ---------------------------- unit cell inputs from paper
    # width_unloaded = microMeters_to_Meters(1)
    # width_loaded = microMeters_to_Meters(4)
    # D0 = mm_To_Meters(1.34)
    # D1 = microMeters_to_Meters(100)
    # D2 = microMeters_to_Meters(100)
    # D3 = microMeters_to_Meters(95)
    # unit_Cell_Len = mm_To_Meters(4.02)
    #
    # In_Order_loads_Widths = [D1, D2, D3]
    # number_of_loads = len(In_Order_loads_Widths)
    #
    # # ---------------------------- SC inputs
    # Height = nanoMeters_to_Meters(300)
    # line_thickness = nanoMeters_to_Meters(60)
    # ground_thickness = nanoMeters_to_Meters(300)
    # Tc = 14.7
    # T = 4  # what equatioins to use when temp is > 0
    # pn = 0.00000132
    # er = 11.44
    # tanD = 1.48351e-5
    # Jc = 1

    # ---------------------------- models of the MicroStripModel -
    #                      one for an unloaded line , one for a loaded line
    loaded_line_model = SuperConductingMicroStripModel(Height, width_loaded, line_thickness, er, tanD, Jc)
    unloaded_line_model = SuperConductingMicroStripModel(Height, width_unloaded, line_thickness, er, tanD, Jc)

    # ---------------------------- model of the Super conductor
    super_conductivity_model = SuperConductivity(T, Tc, pn)

    # ---------------------------- model of the floquet line
    Floquet_line = SuperConductingFloquetLine(unit_Cell_Len, D0, loads_Widths, loaded_line_model, unloaded_line_model,
                                              super_conductivity_model, width_unloaded, width_loaded, line_thickness,
                                              Jc)

    # ---------------------------- gain inputs

    # todo make inputs complex
    As_init = 100
    Ai_init = 0
    Ap_init = 300000
    pump_freq = 6.772e9
    # todo get value for I

    """
    The term I∗ is proportional to I∗′/√α∗, where I∗′ is a parameter comparable to the critical current Ic, and α∗ is 
    the ratio of kinetic inductance to total inductance.
    
    """

    calcGain(As_init, Ai_init, Ap_init, pump_freq, unit_Cell_Len, Floquet_line, resolution)
