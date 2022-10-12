from matplotlib import pyplot as plt

from BlockTwoTransmissionLineModels.lineModels.MicroStripModel import SuperConductingMicroStripModel

height = 1
width = 1
thickness = 1
epsilon_r = 1
tan_delta = 1

model = SuperConductingMicroStripModel(height, width, thickness, epsilon_r, tan_delta)
# get inputs for micro strip model


Y, X = [], []
V = 0
res = .01

while V < 15:
    val = model.a(V, 1, .01)

    Y.append(val.real)
    X.append(V)

    V += res

fig, ax = plt.subplots()
ax.plot(X, Y, linewidth=1.0)
plt.show()
