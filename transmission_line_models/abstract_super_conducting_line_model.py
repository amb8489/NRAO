from abc import ABC, abstractmethod


class AbstractSCTL(ABC):

    # sc transmissioin line outputs
    @abstractmethod
    def characteristic_impedance(self, *args, **kwargs):
        pass

    @abstractmethod
    def propagation_constant(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_propagation_constant_characteristic_impedance(self, frequency, surface_impedance):
        pass
