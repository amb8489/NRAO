import time
from multiprocessing import Pool

import numpy as np

from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.utills.functions import hertz_to_GHz

super_conductivity_model = SuperConductivity(4, 14.7,.00000135)












def run():
    conductivity = []
    f = np.linspace(hertz_to_GHz(1), hertz_to_GHz(40), 1000)
    s = time.time()
    for freq in f:
        conductivity.append(super_conductivity_model.conductivity(freq))
    print("classic", time.time() - s)


    s = time.time()
    with Pool(2) as p:
            power_gain = p.map(super_conductivity_model.conductivity, f)
    print("multi", time.time() - s)

if __name__ == '__main__':
    run()







