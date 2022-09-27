import time
from SuperConductivityEquations import SCE

s = time.time()
print(SCE.conductivityN(1, 1, 2))
print(time.time() - s)
