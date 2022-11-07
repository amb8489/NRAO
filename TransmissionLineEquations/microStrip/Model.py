from abc import ABC, abstractmethod

# TODO
"""
--- INPUT ---

model specific geometric dimension of transmission line 

Epsilon_R , tand( on some models)



--- OUT ----

propagation constant

impedance

epsilon_eff

g1
g2



"""


# TODO all models should output these outputs check if this is all after merge of second and third model


class TransmissionLineModel(ABC):
    pass

    # all models must have a G1 AND G2 METHODS
    # geometrical factors

    # @abstractmethod
    # def g1(self):
    #     pass
    #
    # @abstractmethod
    # def g2(self):
    #     pass

    # TODO what is this for micro strip model ??
    # @abstractmethod
    # def epsilon_eff(self):
    #     pass

    # TODO what is this for micro strip model ??
    # @abstractmethod
    # def impedance(self):
    #     pass

    # TODO what is this for micro strip model ??
    # @abstractmethod
    # def propagation_const(self):
    #     pass

    # @abstractmethod
    # def characteristic_impedance(self):
    #     pass
