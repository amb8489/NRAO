import random

import numpy as np
from matplotlib import pyplot as plt

n = 10
y1 = [random.randint(0, n) for i in range(n)]
x1 = range(n)


y2 = [random.randint(0, n) for i in range(n)]
x2 = range(n)

fig6, ax66 = plt.subplots()
plt.suptitle(f"[Pump Freq: {000} GHz] [# cells: {123}] [pump current: {456}]")
ax66.plot(x1, y1, '-', color='tab:orange')
ax66.plot(x2, y2, '--', color='tab:blue')

ax66.set_ylim([None, None])
ax66.set_title(f"SIGNAL GAIN [Db]")
ax66.set_xlabel('Frequency [GHz]')

data = []
f = []
for idx,line in enumerate(fig6.gca().lines):
    data.extend(line.get_data())
    print(fig6.gca().get_xlabel())
    print(fig6.gca())



print(f)

print(np.column_stack(data))



plt.show()