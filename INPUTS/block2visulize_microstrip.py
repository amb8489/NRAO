"""
AARON BERGHASH

file of all inputs for each block

"""
import numpy as np
from matplotlib import pyplot as plt

from SuperConductivityEquations.SCE import conductivity, Zs
from BlockTwoTransmissionLineModels.lineModels.MicroStripModel import SuperConductingMicroStripModel
import time

startTime = time.time()

"""


        BLOCK 2 SUPER CONDUCTING TRANSMISSION LINES
        
        makes a model for chosen line 


"""

# --- INPUTS 1 CHOOSE A LINE MODEL --- "


model_choice = "micro_strip"

if model_choice == "micro_strip":

    # --- INPUTS 2  --- "
    Epsilonr = 3.8  # Permitivitty substrate
    ts = 300E-9  # Thickness strip in m
    tgg = 1000E-9  # Thickness ground in m
    Tc = 8.7  # Critical temperature
    Jc = 200000E4  # Critical current
    Rho = 6.17E-8  # Resistivity in \[CapitalOmega].m
    Sigma = 1 / Rho  # Normal state conductivity

    fopr = 7E9
    Topr = 1

    w = 1
    H = .25
    f = fopr
    TanD = 0
    Temp = Topr
    model = SuperConductingMicroStripModel(H, w, ts, Epsilonr, TanD)

    efm = 1

    model = SuperConductingMicroStripModel(H, w, ts, Epsilonr, TanD)

    x = freqRange = np.linspace(.1, 5, 100)
    Zc_y = []
    P_y = []
    conduct_y = []
    surface_impedance_y = []
    kinetic_inductance_y = []

    for freq in x:
        conduct = conductivity(freq, Temp, Tc, Rho)
        conduct_y.append(conduct)

        zs = Zs(freq, conduct, ts)
        surface_impedance_y.append(zs)

        kinetic_inductance_y.append(model.apha_ky(zs, freq, w, H, ts))

        Z = model.series_impedance_Z(zs, model.g1, model.g2)
        Y = model.shunt_admittance_Y(efm, model.g1)

        Zc_y.append(model.characteristic_impedance(Z, Y))
        P_y.append(model.propagation_constant(Z, Y))

    print("\n\nTime taken: {} s".format(time.time() - startTime))

    fig, ax = plt.subplots(3, 2)
    fig.suptitle('characteristic_impedance and propagation_constant')

    ax[0, 0].plot(x, Zc_y)
    ax[0, 0].set_ylabel('characteristic_impedance')

    ax[1, 0].plot(x, P_y)
    ax[1, 0].set_ylabel('propagation_constant')

    ax[2, 0].plot(x, conduct_y)
    ax[2, 0].set_ylabel('conductivity')

    ax[0, 1].plot(x, surface_impedance_y)
    ax[0, 1].set_ylabel('surface impedance')

    ax[1, 1].plot(x, kinetic_inductance_y)
    ax[1, 1].set_ylabel('Fraction kinetic inductance')

    plt.show()

    # todo test other needed outputs and check functions
