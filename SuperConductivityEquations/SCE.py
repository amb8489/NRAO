'''
NRAO
Aaron Berghash amb8489@g.rit.edu
'''

import math

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
    pass


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


def sigma1NMenos():
    pass


def sigma1NMas():
    pass


def sigma2NMenos():
    pass


def sigma2NMas():
    pass


def sigma1N(delta, hf, kT):

    if hf <= 2 * delta:
        return sigma1NMenos(delta, hf, kT)
    return sigma1NMenos(delta, hf, kT) - sigma1NMas(delta, hf, kT)


def sigma2N(delta, hf, kT):
    if hf <= 2 * delta:
        return sigma2NMenos(delta, hf, kT)
    return sigma2NMas(delta, hf, kT)


def ConductivityN():
    pass
