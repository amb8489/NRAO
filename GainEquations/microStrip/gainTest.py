import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.microStrip.beta_unfold import SCFL_Model
from GainEquations.microStrip.gain import Gain
from Supports.Support_Functions import find_idx_of_closest_value


def calcGain(As_init, Ai_init, Ap_init, pump_freq, d, lineModel, resolution, I):
    s = time.time()

    # calc signal freq up to pump_freqTimes2
    beta_signal = []
    freq_to_idx = {}
    f_range = np.linspace(1000, 2 * pump_freq, resolution)
    for i, signal_freq in enumerate(f_range):
        freq_to_idx[signal_freq] = i
        _, btaUf_signal, _, _, _ = lineModel.beta_unfolded(signal_freq)
        beta_signal.append(btaUf_signal)

    # todo make sure that this freq approximization is okay to do
    # calc beta for the pump freq (finds the closest freq in np.linspace(1000, 2 * pump_freq, resolution) to pump freq )
    beta_pump = beta_signal[find_idx_of_closest_value(f_range, pump_freq)]

    # calc beta for the idle freqs (finds the closest freq in np.linspace(1000, 2 * pump_freq, resolution) to idle freqs )
    # optimization np.searchsorted(f_range, idlerFreqs)) is basically just rev(range(res)) .. a list starting from res to 0  .. [res, res -1 .res-2 ... 0]

    beta_idler = np.array(beta_signal)[np.searchsorted(f_range, ((2 * pump_freq) - f_range))]

    z = np.linspace(0, d, resolution)
    gain = []
    for i, freq in enumerate(f_range):
        # TODO is it not doin gthis right and need to put back in init values ?
        g = Gain(freq, z, I, beta_signal, beta_idler, beta_pump, As_init, Ai_init, Ap_init, 500, resolution,
                 freq_to_idx)
        gain.append(np.log10(g))

    print(f"time taken {time.time() - s}")
    plt.plot(f_range, gain)
    plt.show()


if __name__ == "__main__":
    # INPUTS FROM Parametric-amplification-of-electromagnetic-signals-with-superconducting-transmission-lines.pdf on MS

    # ---------------------------- frequency range and how many sample points between start and end freq
    # todo if EndFreq > pump then go to ebd freq and not pump (this may mess up [resolution - 1 - freq_to_idx[freq]] in gain)
    StartFreq, EndFreq, resolution = 1000, 7e9, 500

    # ---------------------------- unit cell inputs from paper
    unit_Cell_Len = 0.00402
    D2 = 9.5e-5
    D1 = 1e-4
    D0 = 0.00134
    width_loaded = 4e-6
    width_unloaded = 1e-6

    # ---------------------------- SC inputs
    Height = 3e-7
    thickness = 6e-8
    critical_Temp = 14.7
    op_temp = 4
    pn = 0.000132
    er = 11.44
    ground_thickness = Height
    tanD = 1.48351e-5

    lineModel = SCFL_Model(unit_Cell_Len, D0, D1, D2, width_loaded, width_unloaded, er, Height, thickness,
                           ground_thickness,
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
