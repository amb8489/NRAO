from abc import ABC, abstractmethod

class AbstractSCTL(ABC):

    # sc transmissioin line outputs


    @abstractmethod
    def get_length(self):
        '''
        :return: the length of the line
        '''


    @abstractmethod
    def get_width(self):
        '''
        :return: the width of the line
        '''

    @abstractmethod
    def characteristic_impedance(self, *args, **kwargs):
        """
        implementation of the super conducting characteristic_impedance of the line
        :param frequency:
        :param surface_impedance:
        :return:
        a tuple of the line propagation_constant and characteristic_impedance
        """

        pass

    @abstractmethod
    def propagation_constant(self, *args, **kwargs):
        """
        implementation of the super conducting propagation_constant of the line
        :param frequency:
        :param surface_impedance:
        :return:
        a tuple of the line propagation_constant and characteristic_impedance
        """
        pass

    @abstractmethod
    def get_gamma_Zc(self, frequency: float, surface_impedance: complex) -> (
            complex, complex):
        """
        implementation of the super conducting propagation_constant and characteristic_impedance of the line
        :param frequency:
        :param surface_impedance:
        :return:
        a tuple of the line propagation_constant and characteristic_impedance
        """
        pass
