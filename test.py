import numpy as np
import matplotlib.pyplot as plt

from utills.functions import toGHz

x_org = np.linspace(0, 2 * np.pi, 10)
y_org = np.sin(x_org)


xvals = np.linspace(0, 2*np.pi, 50)
yinterp = np.interp(xvals, x_org, y_org)


# plt.plot(x, y, 'o')
plt.plot(xvals, yinterp, '-x')
plt.show()
plt.close()
#########################################

resolution = 1000
PUMP_FREQUENCY = toGHz(11.63)


Y_org = np.linspace(0, 2 * PUMP_FREQUENCY, resolution)
X_org = np.linspace(0, resolution, resolution)

plt.plot(X_org, Y_org)
plt.show()






