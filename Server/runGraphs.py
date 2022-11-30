import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.microStrip.abrx import SCFL_Model
from Supports.Support_Functions import nanoMeter_to_Meter, microMeter_to_Meters


def mkGraphs(unit_Cell_Len, l1, width_unloaded, a, b, er, Height, line_thickness, ground_thickness,
             critical_Temp, pn, tanD, op_temp, StartFreq, EndFreq, resolution, Jc):
    s = time.time()

    freqs = np.linspace(int(StartFreq), int(EndFreq), int(resolution))

    lineModel = SCFL_Model(unit_Cell_Len, l1, width_unloaded, a, b, er, Height, line_thickness, ground_thickness,
                           critical_Temp, pn, tanD, op_temp, Jc)
    betaUnfoled, folded = [], []
    f,a, r, x = [], [], [],[]

    for F in freqs:
        aa, bta, btaUnfolded, rr, xx = lineModel.abrx(F)
        betaUnfoled.append(btaUnfolded)
        a.append(aa)
        folded.append(b)
        r.append(rr)
        x.append(xx)
        f.append(F)

    print("total time taken for timed element: ", lineModel.tot)
    totaltime = time.time() - s
    print("total time: ", totaltime, " % of total time taken up to calc element ", lineModel.tot * 100 / totaltime, "%")

    return {"Freqs": f, "Alpha": a, "Beta": betaUnfoled, "r": r, "x": x}
