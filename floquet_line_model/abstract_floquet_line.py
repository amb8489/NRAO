from abc import ABC, abstractmethod


class AbstractFloquetLine(ABC):
    # 2x2 ABCD matrix of TLs
    @abstractmethod
    def make_ABCD_Matrix(self, *args, **kwargs):
        pass

    # gamma for TL
    @abstractmethod
    def Pd(self, *args, **kwargs):
        pass

    # return array of both positive direction of proagation and negitive ex: return [- (B2 / (ADm + ADs2)), - (B2 / (ADm - ADs2))]
    @abstractmethod
    def Bloch_impedance_Zb(self, *args, **kwargs):
        pass

    # returning the RL and GC of circuit return ex:  return R, L, G, C
    @abstractmethod
    def RLGC(self, *args, **kwargs):
        pass

    @abstractmethod
    def Transmission(self, *args, **kwargs):
        pass

    # todo abstractmethod for abrx
