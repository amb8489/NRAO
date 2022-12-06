from abc import ABC, abstractmethod


class SC_TransmissionLine(ABC):
    # Geometrical factors
    @abstractmethod
    def G1(self, *args, **kwargs):
        pass

    @abstractmethod
    def G2(self, *args, **kwargs):
        pass

    @abstractmethod
    def series_impedance_Z(self, *args, **kwargs):
        pass

    """
    shunt admittance of a TEM transmission line
    """

    @abstractmethod
    def shunt_admittance_Y(self, *args, **kwargs):
        pass

    # sc transmissioin line outputs
    @abstractmethod
    def characteristic_impedance(self, *args, **kwargs):
        pass

    @abstractmethod
    def propagation_constant(self, *args, **kwargs):
        pass
