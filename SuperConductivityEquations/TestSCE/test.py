import time
from SuperConductivityEquations import SCE


# speed test
s = time.time()

for i in range(100):
    SCE.conductivityN(1, 1, 1)
print(time.time() - s)

import matplotlib.pyplot as plt


# make data

lim = 1000
x = [SCE.conductivityN(.8, 3, i) for i in range(1,lim)]
y = [i for i in range(1,lim)]

# plot
fig, ax = plt.subplots()

ax.plot(x, y, linewidth=1.0)


plt.show()
