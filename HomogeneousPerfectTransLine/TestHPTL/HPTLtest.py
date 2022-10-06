from HomogeneousPerfectTransLine.HPTL_Equations import *
from SuperConductivityEquations.SCE import conductivityNormalized, Delta_O, conductivity

tempK = .01
Tc = 14
ts = 2
Pn = 52
freq = .01
SIGN = 1/52


DELTAO =Delta_O(Tc)
COND = conductivity(freq,tempK,Tc,Pn)

print(COND)

lamO = Lambda0(SIGN,DELTAO)

zslow = z_slow(freq,lamO,None)

ZS = Zs(freq,COND,ts)

print("Zslow   ",zslow)
print("ZS      ",ZS)
print("LAMBDA0 ",lamO)
zs = Zs(freq,COND,ts)
print("Lambda  ",Lambda(zs,freq,ts))











