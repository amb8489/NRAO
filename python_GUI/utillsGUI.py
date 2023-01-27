import random
from random import choice


def rft():
    return random.random()


def fit():
    return random.randint(1, 50)


def randomColor():
    return "#" + "".join([choice("012345689ABCDEF") for i in range(6)])


def randomColorBright():
    return "#" + "".join([choice("689ABCD") for i in range(6)])


def random_setting(ncols):
    return {'SC': {'Er': rft(), 'H': rft(), 'Ts': rft(), 'Tg': rft(), 'T': rft(), 'Tc': rft(), 'Jc': rft(),
                   'Normal Resistivity': rft(), 'Tan D': rft()},

            'Dimensions': {'loads': [[fit() for i in range(ncols)] for i in range(fit())], 'Unit Cell Length []': rft(),
                           'Central Line Width []': rft()},

            'Frequency Range': {'Start Freq [GHZ]': fit(), 'End Freq [GHZ]': fit(), 'Resolution': fit()},

            'Gain': {'As0': rft(), 'Ai0': rft(), 'Ap0': rft(), 'Pump Frequency [GHZ]': rft()}}
