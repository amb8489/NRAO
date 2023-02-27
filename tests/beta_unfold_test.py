import time

import numpy as np
from matplotlib import pyplot as plt

from floquet_line_model.floquet_line_temp import SuperConductingFloquetLine_art
from model_inputs.artificial_cpw_inputs import ArtificialCPWInputs
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.artificial_cpw.super_conducting_artificial_cpw_model import \
    SuperConductingArtificialCPWLine
from utills.functions import toGHz, beta_unfold

inputs = {'SC': {'Er': 11.4, 'Height': 5000.0, 'Ts': 600.0, 'Ground Thickness': 0.0,
                 'Super Conductor Operation Temperature': 1.0, 'Super Conductor Critical Temperature': 14.4,
                 'Super Conductor Critical Current': 0.0, 'Super Conductor Normal Resistivity': 132.0,
                 'Super Conductor Tangent Delta': 0.0}, 'Dimensions': {
    'loads': [['660', '1', '1', '1', '19', '3'], ['240', '1', '1', '1', '35', '3'], ['1326', '1', '1', '1', '19', '3'],
              ['240', '1', '1', '1', '35', '3'], ['1206', '1', '1', '1', '19', '3'], ['480', '1', '1', '1', '35', '3'],
              ['558', '1', '1', '1', '19', '3.']]},
          'Frequency Range': {'Start Frequency': 1.0, 'End Frequency': 25.0, 'Resolution': 1000.0},
          'gain_models': {'Signal Amplitude': 0.0, 'Idler Amplitude': 0.0, 'Pump Amplitude': 0.0,
                          'Pump Frequency': 0.0}}

inputs = ArtificialCPWInputs(inputs)

super_conductivity_model = SuperConductivity(inputs.op_temp, inputs.crit_temp, inputs.normal_resistivity)
er = inputs.er
ts = inputs.line_thickness
h = inputs.height

line_models = []
i = 1
for line_len, S, WH, LH, WL, LL in inputs.line_dimensions:
    nfs = line_len // (LH + (2 * S) + LL)
    line_models.append(
        SuperConductingArtificialCPWLine(LH, WH, LL, WL, S, nfs, er, ts, h, super_conductivity_model, line_len))
    i += 1
floquet_line = SuperConductingFloquetLine_art(line_models, super_conductivity_model, ts)

# ---------------------------- storage -------------------
floquet_alpha, floquet_beta, floquet_r, floquet_x = [], [], [], []
floquet_transmission_plt = []

central_line_beta = []
central_line_alpha = []

start_freq_GHz = toGHz(1)
end_freq_GHz = toGHz(40)
frequency_range = np.linspace(start_freq_GHz, end_freq_GHz, 5000)

for frequency in frequency_range:
    alpha, beta, alphaCl, betaCL, r_, x_ = floquet_line.simulate(frequency)
    floquet_beta.append(beta)
    central_line_beta.append(betaCL)

size = 10**7
random = np.random.randint(10000000, size=size)

s = time.time()
fast  = beta_unfold(random)
print("fast: ",time.time()-s)


plt.plot([v for v in np.abs(floquet_beta)], 'b')
plt.plot(beta_unfold([v for v in floquet_beta]), 'r')

plt.show()
