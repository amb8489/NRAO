import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.microStrip.beta_unfold import calc_aplha_beta_r_x



StartFreq, EndFreq = 1000,25e9
betaUnfoled, folded, freqs = [], [], []
s = time.time()

lineModel = calc_aplha_beta_r_x()

for F in np.linspace(StartFreq, EndFreq,10000):

    buf,bta = lineModel.beta_unfolded(F)
    betaUnfoled.append(buf)
    folded.append(bta)
    freqs.append(F)


print("total time: ", time.time() - s)

fig, axs = plt.subplots()
axs.plot(freqs, folded)
axs.plot(freqs, betaUnfoled)
plt.show()
