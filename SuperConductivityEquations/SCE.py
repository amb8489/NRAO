'''
NRAO
Aaron Berghash amb8489@g.rit.edu
'''

import math
from scipy.integrate import quad

'''
------------------------------definitions------------------------------
'''


def e1(e, delta):
    return math.sqrt(e ** 2 - delta ** 2)


def e2(e, delta, hf):
    return math.sqrt((e + hf) ** 2 - delta ** 2)


def e3(e, delta, hf):
    return e ** 2 + delta ** 2 + hf * e


def e4(e, delta):
    return math.sqrt(delta ** 2 - e ** 2)


def g(e, delta, hf):
    return e3(e, delta, hf) / (e1(e, delta) * e2(e, delta, hf))


def g2(e, delta, hf):
    return e3(e, delta, hf) / (e4(e, delta) * e2(e, delta, hf))


def fd(e, kT):
    return 1 / (math.exp(e / kT) + 1)


def ff(e, hf, kT):
    return fd(e, kT) - fd(e + hf, kT)


def f2(e, hf, kT):
    return 1 - 2 * fd(e + hf, kT)


def int1(e, delta, hf, kT):
    return ff(e, hf, kT) * g(e, delta, hf)


def int11(e, delta, hf, kT):
    return f2(e, hf, kT) * g(e, delta, hf)


def int2(e, delta, hf, kT):
    return f2(e, hf, kT) * g2(e, delta, hf)


def sigma1NL(delta, hf, kT):
    lower = 0
    upper = 20 * math.sqrt(delta)

    f = lambda x: int1(delta + x ** 2, delta, hf, kT) * 2 * x

    return (2 / hf) * quad(f, lower, upper)[0]


def sigma1NU(delta, hf, kT):
    lower = 0
    upper = math.sqrt((hf / 2) - delta)

    f1 = lambda x: int11(delta - hf + x ** 2, delta, hf, kT) * 2 * x
    f2 = lambda x: int11(-delta - x ** 2, delta, hf, kT) * 2 * x

    return (1 / hf) * (quad(f1, lower, upper)[0] + quad(f2, lower, upper)[0])


def sigma1N(delta, hf, kT):
    if hf <= 2 * delta:
        return sigma1NL(delta, hf, kT)
    return sigma1NL(delta, hf, kT) - sigma1NU(delta, hf, kT)


def sigma2NL(delta, hf, kT):
    lower = 0
    upper = math.sqrt((hf / 2))

    f1 = lambda x: int2(delta - hf + x ** 2, delta, hf, kT) * 2 * x
    f2 = lambda x: int2(delta - x ** 2, delta, hf, kT) * 2 * x


    return (1 / hf) * (quad(f1, lower, upper)[0] + quad(f2, lower, upper)[0])


def sigma2NU(delta, hf, kT):
    lower = 0
    upper = math.sqrt(delta)

    f1 = lambda x: int2(-delta + x ** 2, delta, hf, kT) * 2 * x
    # this shows up twice , can we calc just once ?
    f2 = lambda x: int2(delta - x ** 2, delta, hf, kT) * 2 * x

    return (1 / hf) * (quad(f1, lower, upper)[0] + quad(f2, lower, upper)[0])


def sigma2N(delta, hf, kT):
    if hf <= 2 * delta:
        return sigma2NL(delta, hf, kT)
    return sigma2NU(delta, hf, kT)




def conductivityN(delta, hf, kT):
    return sigma1N(delta, hf, kT) - 1j * sigma2N(delta, hf, kT)
