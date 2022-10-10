from HomogeneousPerfectTransLine.lineModels.HPTL_Equations import *
from SuperConductivityEquations.SCE import Delta_O
import matplotlib.pyplot as plt

tempK = .01
Tc = 14
ts = 50
Pn = 52
freq = 1
SIGN = 1 / 52
DELTAO = Delta_O(Tc)

# COND = conductivity(freq,tempK,Tc,Pn)
#
# print(COND)
#
# lamO = Lambda0(SIGN,DELTAO)
#
# zslow = z_slow(freq,lamO,None)
#
# ZS = Zs(freq,COND,ts)
#
# print("Zslow   ",zslow)
# print("ZS      ",ZS)
# print("LAMBDA0 ",lamO)
# zs = Zs(freq,COND,ts)
# print("Lambda  ",Lambda(zs,freq,ts))


StartFreq, EndFreq = .1, 10
tempK = 1
tc = 14
Pn = 52

step = .1

re, im, freqs = [], [], []
freq = StartFreq
while freq < EndFreq:

    val = Lambda0(SIGN,DELTAO)

    # val = Zs(freq,conductivity(freq,tempK,Tc,Pn),ts)
    # val = z_slow(freq,Lambda0(SIGN,DELTAO),ts)
    # zs = Zs(freq,conductivity(freq,tempK,Tc,Pn),ts)
    # vall = Lambda(zs,freq,ts)
    # val = zmss(freq, .8, freq)

    # print(val)
    re.append(val)
    # im.append(zs.imag)

    freqs.append(freq)
    freq += step

# plot
fig, ax = plt.subplots()
ax.plot(freqs, re, linewidth=1.0, label='{} Kelvin'.format(tempK))
ax.plot(freqs, im, linewidth=2.0,label='{} Kelvin'.format(tempK))

ax.set_ylabel('conductivity')
ax.set_xlabel('frequency')
# plt.ylim([0, 1])
plt.legend()
plt.show()
