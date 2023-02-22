from abc import ABC, abstractmethod


class AbstractSCTL(ABC):

    # sc transmissioin line outputs
    @abstractmethod
    def characteristic_impedance(self, *args, **kwargs):
        pass

    @abstractmethod
    def propagation_constant(self, *args, **kwargs):
        pass

    # todo maybe instead of surface_impedance we pass the conductivity model and store the currrent surface_impedance
    # in the conductivity model
    @abstractmethod
    def get_propagation_constant_characteristic_impedance(self, frequency, surface_impedance):
        pass
