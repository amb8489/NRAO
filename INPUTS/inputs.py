"""
AARON BERGHASH

file of all inputs for each block

"""

from SuperConductivityEquations.SCE import conductivity, Zs
from BlockTwoTransmissionLineModels.lineModels.MicroStripModel import SuperConductingMicroStripModel
import time

startTime = time.time()
"""


        BLOCK 1 SUPER CONDUCTIVITY EQUATIONS
        
        
"""

# --- INPUTS ---
TempK = 1
Tc = 1
Pn = 1
fStart = 1
fEnd = 1
Thickness_ts = 1

# --- OUTPUTS ---
MaterialConductivity = conductivity(fStart, TempK, Tc, Pn)
surface_impedance_Zs = Zs(fStart, MaterialConductivity, Thickness_ts)

"""


        BLOCK 2 SUPER CONDUCTING TRANSMISSION LINES
        
        makes a model for chosen line 


"""

# --- INPUTS 1 CHOOSE A LINE MODEL --- "


model_choice = "micro_strip"

if model_choice == "micro_strip":
    height = 1
    width = 1
    thickness = 1
    epsilon_r = 1
    tan_delta = 1

    model = SuperConductingMicroStripModel(height, width, thickness, epsilon_r, tan_delta)
    # get inputs for micro strip model


    print("g1: ",model.g1(width, height, thickness))
    print("g2: ",model.g2(4, 1, thickness))









print("\n\nTime taken: {} s".format(time.time() - startTime))
