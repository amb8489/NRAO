from abc import ABC, abstractmethod

# TODO
"""
--- INPUT ---

model specific geometric dimension of transmission line 

Epsilon_R



--- OUT ----

propagation constant

impedance

epsilon_eff

g1
g2
"""


class TransmissionLineModel(ABC):

    # all models must have a G1 AND G2 METHODS
    # geometrical factors
    @abstractmethod
    def g1(self):
        pass

    @abstractmethod
    def g2(self):
        pass

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
