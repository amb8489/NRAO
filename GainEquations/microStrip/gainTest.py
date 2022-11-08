import time
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint
from Fluqet_Line_Equations.microStrip.beta_unfold import calc_aplha_beta_r_x
from GainEquations.microStrip.amplitudeEquations import ApmlitudeEquations
from Supports.Support_Functions import find_idx_of_closest_value


def calcGain(As_init, Ai_init, Ap_init, d):





    resolution = 1000

    pump_freq = 6.772e9
    pump_freqTimes2 = 2 * pump_freq

    # calc signal freq up to
    lineModel = calc_aplha_beta_r_x()
    beta_signal = []

    s = time.time()

    f_range = np.linspace(1000, pump_freqTimes2, resolution)
    for i, signal_freq in enumerate(f_range):
        btaUf_signal, bta = lineModel.beta_unfolded(signal_freq)
        beta_signal.append(btaUf_signal)

    print(f"time taken {time.time() - s}")
    beta_pump = beta_signal[find_idx_of_closest_value(f_range, pump_freq)]

    # optimization np.searchsorted(f_range, idlerFreqs)) is basically just rev(range(res)) .. a list starting from res to 0  .. [res, res -1 .res-2 ... 0]
    beta_idler = np.array(beta_signal)[np.searchsorted(f_range, (pump_freqTimes2 - f_range))]

    z = np.linspace(0, d, resolution)
    y0 = [As_init, Ai_init, Ap_init]
    bp = beta_pump
    gain = []
    for i, signal_freq in enumerate(f_range):
        # init conditions
        # range over fluquet line

        bs = beta_signal[i]
        bi = beta_idler[i]

        I = 1
        x = odeint(ApmlitudeEquations, y0, z, args=(bs, bi, bp, I))
        y0 = x[1]
        gain.append(np.log10(x[:, 0][500]))

    plt.plot(f_range, gain)
    plt.show()


if __name__ == "__main__":
    StartFreq, EndFreq = 1000, 7e9
    d = .0023

    # todo init conditions
    calcGain(1000000, 0, 30000, d)
