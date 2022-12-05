import time
import numpy as np
from Fluqet_Line_Equations.microStrip.abrx import SCFL_Model


def mkGraphs(StartFreq,EndFreq,resolution,unit_Cell_Len, D0, In_Order_loads_Widths, number_of_loads, width_unloaded, width_loaded, er,
                          Height, line_thickness, ground_thickness, Tc, pn, tanD, T, Jc):
    s = time.time()

    freqs = np.linspace(int(StartFreq), int(EndFreq), int(resolution))

    FloquetLine = SCFL_Model(unit_Cell_Len, D0, In_Order_loads_Widths, number_of_loads, width_unloaded, width_loaded, er,
                          Height, line_thickness, ground_thickness, Tc, pn, tanD, T, Jc)
    betaUnfoled, folded = [], []
    f,a, r, x = [], [], [],[]

    for F in freqs:
        aa, bta, btaUnfolded, rr, xx = FloquetLine.abrx(F)
        betaUnfoled.append(btaUnfolded)
        a.append(aa)
        folded.append(bta)
        r.append(rr)
        x.append(xx)
        f.append(F)

    totaltime = time.time() - s
    print("total time: ", totaltime)

    return {"Freqs": f, "Alpha": a, "Beta": betaUnfoled, "r": r, "x": x}
