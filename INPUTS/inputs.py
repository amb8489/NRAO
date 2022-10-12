"""
AARON BERGHASH

file of all inputs for each block

"""

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
    height = 1
    width = 1
    thickness = 1
    epsilon_r = 1
    tan_delta = 1

    model = SuperConductingMicroStripModel(height, width, thickness, epsilon_r, tan_delta)
    # get inputs for micro strip model

    print("g1: ", model.g1)
    print("g2: ", model.g2)

    # todo test other needed outputs and check functions

print("\n\nTime taken: {} s".format(time.time() - startTime))
