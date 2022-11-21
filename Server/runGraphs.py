import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.microStrip.beta_unfold import SCFL_Model
from Supports.Support_Functions import nanoMeter_to_Meter, microMeter_to_Meters






def mkGraphs(unit_Cell_Len, l1, width_unloaded, a, b, er, Height, line_thickness, ground_thickness,
                           critical_Temp, pn, tanD, op_temp,StartFreq, EndFreq, resolution):
    s = time.time()

    lineModel = SCFL_Model(unit_Cell_Len, l1, width_unloaded, a, b, er, Height, line_thickness, ground_thickness,
                           critical_Temp, pn, tanD, op_temp)
    betaUnfoled, folded, freqs = [], [], []
    a, r, x = [], [], []



    for F in np.linspace(int(StartFreq), int(EndFreq), int(resolution)):
        aa, bta, b, rr, xx = lineModel.beta_unfolded(F)
        betaUnfoled.append(bta)
        a.append(aa)
        folded.append(b)
        r.append(abs(rr))
        x.append(xx)
        freqs.append(F)

    print("total time taken for timed element: ", lineModel.tot)
    totaltime = time.time() - s
    print("total time: ", totaltime, " % of total time taken up to calc element ", lineModel.tot * 100 / totaltime, "%")

    fig, (a1, a2, a3, a4) = plt.subplots(4)
    a1.plot(freqs, betaUnfoled)
    a1.plot(freqs, folded)
    a2.plot(freqs, a)
    a3.plot(freqs, r)
    a4.plot(freqs, x)
    plt.savefig('foo.png', bbox_inches='tight')
    plt.savefig('/Users/aaron/Desktop/proj/src/images/plt.png', bbox_inches='tight')





