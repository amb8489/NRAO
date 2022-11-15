import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.microStrip.beta_unfold import SCFL_Model
from GainEquations.microStrip.gain import Gain
from Supports.Support_Functions import find_idx_of_closest_value, microMeter_to_Meters, nanoMeter_to_Meter


def calcGain(As_init, Ai_init, Ap_init, pump_freq, d, lineModel, resolution, I):
    s = time.time()

    # calc signal freq up to pump_freqTimes2
    betas = []
    f_range = np.linspace(1000, 2 * pump_freq, resolution)
    for i, signal_freq in enumerate(f_range):
        _, btaUf_signal, _, _, _ = lineModel.beta_unfolded(signal_freq)
        betas.append(btaUf_signal)

    # todo make sure that this freq approximization is okay to do
    # calc beta for the pump freq (finds the closest freq in np.linspace(1000, 2 * pump_freq, resolution) to pump freq )
    beta_pump = betas[find_idx_of_closest_value(f_range, pump_freq)]

    z = np.linspace(0, d, resolution)
    Times2PumpFreq = (2 * pump_freq)
    gain = []
    L = resolution // 2
    for i, freq in enumerate(f_range):
        # TODO is it not doin gthis right and need to put back in init values ?
        g = Gain(Times2PumpFreq - freq, freq, z, I, betas, beta_pump, As_init, Ai_init, Ap_init, L, resolution, f_range)
        gain.append(np.log10(g))

    print(f"time taken {time.time() - s}")
    plt.plot(f_range, gain)
    plt.show()


if __name__ == "__main__":
    # INPUTS FROM Parametric-amplification-of-electromagnetic-signals-with-superconducting-transmission-lines.pdf on MS

    StartFreq, EndFreq, resolution = 1e9, 7e9, 1000

    # ---------------------------- frequency range and how many sample points between start and end freq
    # todo if EndFreq > pump then go to ebd freq and not pump (this may mess up [resolution - 1 - freq_to_idx[freq]] in gain)
    # ---------------------------- unit cell inputs from paper
    unit_Cell_Len = microMeter_to_Meters(2300)
    l1 = microMeter_to_Meters(50)
    width_unloaded = microMeter_to_Meters(1.49)
    a = 1.2
    b = 2

    # ---------------------------- SC inputs
    er = 10
    Height = nanoMeter_to_Meter(250)
    line_thickness = nanoMeter_to_Meter(60)
    ground_thickness = nanoMeter_to_Meter(300)
    critical_Temp = 14.28
    op_temp = 0
    pn = 1.008e-6
    tanD = 0

    lineModel = SCFL_Model(unit_Cell_Len, l1, width_unloaded, a, b, er, Height, line_thickness, ground_thickness,
                           critical_Temp, pn, tanD, op_temp)

    # ---------------------------- gain inputs
    # todo make inputs complex
    As_init = 100
    Ai_init = 0
    Ap_init = 300000
    pump_freq = 6.772e9
    # todo get value for I
    I = 7

    calcGain(As_init, Ai_init, Ap_init, pump_freq, unit_Cell_Len, lineModel, resolution, I)
