import random



import numpy as np

def __get_closest_betas(master, targets):
    # because frequency_range - PUMP_FREQUENCY could result in needing beta values at frequencies that were not
    # simulated we find the closes frequency that was simulated to the one that was not and use that beta
    sorted_keys = np.argsort(master)
    return sorted_keys[np.searchsorted(master, targets, sorter=sorted_keys,side="left")]




PUMP_FREQUENCY = 11.8
res = 10

master = np.random.randint(40, size=res)
search = np.random.randint(40, size=res)

print(__get_closest_betas(master, search))









