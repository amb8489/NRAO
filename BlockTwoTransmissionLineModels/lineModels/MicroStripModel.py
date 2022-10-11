import math
import cmath

from BlockTwoTransmissionLineModels.lineModels.Model import TransmissionLineModel
from Supports.constants import PI, MU_0, PI2, z0, PI4, PLANCK_CONST_REDUCEDev, K0, N0, c
from Supports.Support_Functions import sech, coth, ccoth

"""

    MICRO STRIP MODEL FOR TRANSMISSION LINE
    
    
    NRAO
    Aaron Berghash

    Formulas from https://qucs.sourceforge.net/tech/node75.html#SECTION001211200000000000000

    Penetration depth & Surface Impedance _ kautz "picoseconds pulses on super conducting strip lines"

    
"""


# TODO WHAT IS FUNCTION zt
# TODO CHECK ALL FUNCTIONS
# TODO MAKE SURE WE HAVE ALL THE NEEDED OUTPUTS FOR BOTH BLOCKS THAT WERE MERGED
# TODO  JUST NEED TO CHECK THAT T IS THICKNESS
# TODO where does is epsilon_fm come from in shunt_admittance_Y and is it model dependent
# TODO check K0 in consts


#                                  OPTIMIZATIONS
# TODO use np to opimize if possible
# TODO optimize when going though a freq range dont remake the entire model obj again
# just change and recalc whats changed when the freq changed-- for exaple g1 and g2 dont change depending on the freq
# so they onyl need to be calculated once, but somthing that takes in an argument thats affected by freq then needs to be
# recalculated
# TODO optimizations calcualte once things that are beign called alot | cache common calcs


class SuperConductingMicroStripModel(TransmissionLineModel):

    # TODO where is tan_delta used?
    def __init__(self, height, width, thickness, epsilon_r, tan_delta):

        self.height = height
        self.width = width
        self.thickness = thickness
        self.epsilon_r = epsilon_r
        self.tan_delta = tan_delta

        self.g1 = self.gg1(width, height, thickness)
        self.g2 = self.gg2(width, height, thickness)

    # ----------  schneider   t = 0  ----------
    def __Fs(self, w, h):
        return math.sqrt(1 + (10 * (h / w)))

    def __epsilon_effs(self, epsilon_r, w, h):
        return ((epsilon_r + 1) / 2) + ((epsilon_r - 1) / (2 * self.__Fs(w, h)))

    def __zmss(self, epsilon_r, w, h):
        z0eff = z0 / (math.sqrt(self.__epsilon_effs(epsilon_r, w, h)))

        if w / h <= 1:
            return z0eff * (1 / PI2) * math.log(((8 * h) / w) + (w / (4 * h)))

        return z0eff / ((w / h) + 2.42 - (0.44 * (h / w)) + pow(1 - (h / w), 6))

    # ----------  schneider   t > 0  ----------

    def __epsilon_effst(self, epsilon_r, w, h, t):
        u = w / h

        if u <= (1 / PI2):
            delta_w = (t / PI) * (1 + math.log((PI4 * w) / t))
        else:
            delta_w = (t / PI) * (1 + math.log((2 * h) / t))

        return self.__epsilon_effs(epsilon_r, w + delta_w, h)

    def __zmsst(self, epsilon_r, w, h, t):
        u = w / h

        if u <= (1 / PI2):
            delta_w = (t / PI) * (1 + math.log((PI4 * w) / t))
        else:
            delta_w = (t / PI) * (1 + math.log((2 * h) / t))

        return self.__zmss(epsilon_r, w + delta_w, h)

    # ----------  Hammerstad   t = 0  ----------

    def __epsilon_effh(self, epsilon_r, w, h):
        u = w / h

        u4 = pow(u, 4)

        firstLog = math.log((u4 + pow(u / 52, 2)) / (u4 + 0.432))
        secondLog = math.log(1 + pow(u / 18.1, 3))

        a = 1 + (1 / 49) * firstLog + (1 / 18.7) * secondLog

        b = 0.564 * pow((epsilon_r - .9) / (epsilon_r + 3), 0.053)

        return ((epsilon_r + 1) / 2) + ((epsilon_r - 1) / 2) * pow(1 + (10 / u), -a * b)

    def __ZL1(self, w, h):
        u = w / h

        fu = 6 + (PI2 - 6) * math.exp(-pow(30.666 / u, 0.7528))

        return (z0 / PI2) * math.log((fu / u) + math.sqrt(1 + pow(2 / u, 2)))

    # ----------  Hammerstad   t > 0  ----------

    def __delta_wr(self, epsilon_r, w, h, t):
        return (self.__delta_w1(w, h, t) * (1 + sech(math.sqrt(epsilon_r - 1)))) / 2

    def __delta_w1(self, w, h, t):
        u = w / h
        th = t / h

        upper = 4 * math.e
        lower = th * pow(coth(math.sqrt(6.517 * u)), 2)

        return (t / PI) * math.log(1 + (upper / lower))

    def __epsilon_effht(self, epsilon_r, w, h, t):
        w1 = w + self.__delta_w1(w, h, t)
        wr = w + self.__delta_wr(epsilon_r, w, h, t)

        zl1_up = self.__ZL1(w1, h)
        zl1_low = self.__ZL1(wr, h)
        return self.__epsilon_effh(epsilon_r, wr, h) * pow(zl1_up / zl1_low, 2)

    def __Zmsht(self, epsilon_r, w, h, t):
        wr = w + self.__delta_wr(epsilon_r, w, h, t)
        upper = self.__ZL1(wr, h)
        lower = math.sqrt(self.__epsilon_effht(epsilon_r, wr, h, t))

        return upper / lower

    # -------------------

    def Lambda0(self, sigma_N, delta_O):
        # TODO TEST FOR CORRECTNESS WITH MATHEMATICA CODE
        # TODO ask about the complex square root should just the real part be rooted or both re and im parts
        # AND sigma_N is 1/ Pn
        return math.sqrt(PLANCK_CONST_REDUCEDev / (PI * MU_0 * sigma_N * delta_O))

    # TODO TEST FOR CORRECTNESS WITH MATHEMATICA CODE
    # todo what is t used for?
    def z_slow(self, f, yO, t):
        return 1j * PI2 * f * MU_0 * yO

    # TODO TEST FOR CORRECTNESS WITH MATHEMATICA CODE
    # todo what is t used for?
    def Lambda(self, zs, f, t):
        return (zs / (PI2 * f * MU_0)).imag

    """
    
    
    
    
    
                    super conducting trans line equations for miro strip
                    
             Implementation of the paper of Yassin
             Electromagnetic models for superconducting millimetre-wave and
             sub-milLimetre-wave microstrip transmission lines
    """

    # ------ helper functions ----------

    def __ra(self, w, h, p):
        sqrtP = math.sqrt(p)

        return cmath.exp(
            -1 - ((PI * w) / (2 * h)) - ((p + 1) / sqrtP) * cmath.atanh(1 / sqrtP) - cmath.log((p - 1) / (4 * p)))

    def __rb(self, w, h, rbo, p):
        if w / h >= 5:
            return rbo

        sqrtP = math.sqrt(p)
        return rbo - math.sqrt((rbo - 1) * (rbo - p)) + (p + 1) * math.atanh(
            math.sqrt((rbo - p) / (rbo - 1))) - 2 * sqrtP * math.atanh((rbo - p) / (p * (rbo - 1))) + (
                       (PI * w) / (2 * h)) * sqrtP

    def __Eta(self, w, h, p):
        sqrtP = math.sqrt(p)

        return sqrtP * (((PI * w) / (2 * h)) + ((p + 1) / (2 * sqrtP)) * (1 + math.log(4 / (p - 1))) - 2 * math.atanh(
            1 / sqrtP))

    def __b(self, h, t):
        return 1 + (t / h)

    def __p(self, b):

        bsqrd = b ** 2

        return 2 * bsqrd - 1 + (2 * b * math.sqrt(bsqrd - 1))

    def __rbo(self, eta, p, detaY):
        return eta + ((p + 1) / 2) * math.log(detaY)

    def __DeltaY(self, eta, p):
        return eta if eta > p else p

    def __Kl(self, w, h, t):
        return self.__Chi(w, h, t) / self.__Kf(w, h, t)

    def __Kf(self, w, h, t):

        bc = self.__b(h, t)

        pc = self.__p(bc)

        rac = self.__ra(w, h, pc)

        EtaC = self.__Eta(w, h, pc)

        DeltaYC = self.__DeltaY(EtaC, pc)

        rboc = self.__rbo(EtaC, pc, DeltaYC)

        rbc = self.__rb(w, h, rboc, pc)

        return (h / w) * (2 / PI) * cmath.log((2 * rbc) / rac)

    # Functions to calculate Chi

    def __Is1(self, p, ra, Ra):
        return cmath.log((2 * p - (p + 1) * ra + 2 * cmath.sqrt(p * Ra)) / (ra * (p - 1)))

    def __Ra(self, p, ra):
        return (1 - ra) * (p - ra)

    def __Is2(self, p, rb, Rb):
        return - math.log(((p + 1) * rb - 2 * p - 2 * math.sqrt(p * Rb)) / (rb * (p - 1)))

    def __Rb(self, p, rb):
        return (rb - 1) * (rb - p)

    def __Ig1(self, p, rb, Rb1):
        return -cmath.log(((p + 1) * rb + 2 * p + 2 * cmath.sqrt(p * Rb1)) / (rb * (p - 1)))

    def __Rb1(self, p, rb):
        return (rb + 1) * (rb + p)

    def __Ig2(self, p, ra, Ra1):
        return cmath.log(((p + 1) * ra + 2 * p + 2 * cmath.sqrt(p * Ra1)) / (ra * (p - 1)))

    def __Ra1(self, p, ra):
        return (ra + 1) * (ra + p)

    def __Chi(self, w, h, t):
        bc = self.__b(h, t)
        pc = self.__p(bc)
        rac = self.__ra(w, h, pc)
        EtaC = self.__Eta(w, h, pc)
        DeltaYC = self.__DeltaY(EtaC, pc)
        rboc = self.__rbo(EtaC, pc, DeltaYC)
        rbc = self.__rb(w, h, rboc, pc)
        Rac = self.__Ra(pc, rac)
        Is1c = self.__Is1(pc, rac, Rac)
        Rbc = self.__Rb(pc, rbc)
        Is2c = self.__Is2(pc, rbc, Rbc)
        Rb1c = self.__Ra(pc, rbc)
        Ig1c = self.__Ig1(pc, rbc, Rb1c)
        Ra1c = self.__Ra(pc, rac)
        Ig2c = self.__Ig2(pc, rac, Ra1c)

        if (w / h) < 2:
            return (Is1c + Is2c + Ig1c + Ig2c + PI) / (2 * cmath.log(rbc / rac))
        return (Is1c + Is2c + Ig1c + Ig2c + PI) / (2 * cmath.log(2 * rbc / rac))

    # An important expression for calculating impedance and complex propagation constant
    # defined in this way mainly to calculate tan_Delta from Alpha
    def __X(self, zs, f, w, H, ts):

        ChiC = self.__Chi(w, H, ts)
        ko = (PI2 * f) / c
        return (2 * ChiC * zs) / (ko * z0 * H)

    # Superconducting impedance of the microstrip
    # Note that in this version I have used the suface impedance as parameter
    # Surface impedance can be determined with functions Zs and Zslow
    # zt is the expresion to determine the PCE microstip impedance
    def __ZSy(self, __zt, zs, f, epsilon_r, w, H, ts):
        zmst = self.__zt(epsilon_r, w, H, ts)
        return zmst * (cmath.sqrt(1 - 1j * self.__X(zs, f, w, H, ts))).real

    # Superconducting wavenumber Beta_S / ko
    # It requires the model for the PCE stripline
    # Schneider --> Epsilon_effst, Hammerstad --> Epsilon_effht
    def __beta_Soy(self, est, zs, f, epsilon_r, w, H, ts):
        epsilon_fm = est(epsilon_r, w, H, ts)
        return cmath.sqrt(epsilon_fm) * (cmath.sqrt(1 - 1j * self.__X(zs, f, w, H, ts))).real

    # Superconducting attenuation Alpha_S ko
    # It requires the model for the PCE stripline
    # Schneider --> Epsilon_effst, Hammerstad --> Epsilon_effht
    def __aplha_Sy(self, est, zs, f, epsilon_r, w, H, ts):
        epsilon_fm = est(epsilon_r, w, H, ts)
        return - cmath.sqrt(epsilon_fm) * (cmath.sqrt(1 - 1j * self.__X(zs, f, w, H, ts))).imag

    # Fraction of kinetic inductance
    def __apha_ky(self, zs, f, w, H, ts):
        CF = (cmath.sqrt(1 - 1j * self.__X(zs, f, w, H, ts))).real
        return 1 - (1 / CF ** 2)

    # Phase velocity respect to vo = c
    def __vSy(self, est, zs, f, epsilon_r, w, H, ts):
        epsilon_fm = est(epsilon_r, w, H, ts)
        CF = (cmath.sqrt(1 - 1j * self.__X(zs, f, w, H, ts))).real
        return 1 / (math.sqrt(epsilon_fm) * CF)

    # Including losses
    # Superconducting wave number Beta_S / ko
    # It requires the model for the PCE stripline
    # Schneider --> Epsilon_effst, Hammerstad --> Epsilon_effht
    def __Beta_Syloss(self, est, zs, f, epsilon_r, tand, w, H, ts):
        epsilon_fm = est(epsilon_r, w, H, ts)

        epsilon_t = epsilon_fm - 1j * epsilon_r * tand

        return (cmath.sqrt(epsilon_t) * cmath.sqrt(1 - 1j * self.__X(zs, f, w, H, ts))).real

    # Attenuation AlphaS / ko due to superconducting strip (negligible) and dielectric
    # It requires the model for the PCE stripline
    # Schneider --> Epsilon_effst, Hammerstad --> Epsilon_effht
    def __AlphaSyloss(self, est, zs, f, epsilon_r, tand, w, H, ts):
        epsilon_fm = est(epsilon_r, w, H, ts)

        epsilon_t = epsilon_fm - 1j * epsilon_r * tand

        return -(cmath.sqrt(epsilon_t) * cmath.sqrt(1 - 1j * self.__X(zs, f, w, H, ts))).imag

    # ------------------  OUTPUTS ------------------

    """
    series impedance of a TEM transmission line
    ko is the free-space wavenumber
    No is the impedance of free space
    Zs, is the surface impedance of the conductors
    g1 and g2 are geometrical factors, which characterize the particular transmission line being used.
    """

    # Geometrical factors

    def gg1(self, w, h, t):
        return h / (w * self.__Kf(w, h, t))

    def gg2(self, w, h, t):
        return self.__Kl(w, h, t) / w

    def series_impedance_Z(self, Zs, g1, g2):
        return (1j * (K0 * N0) * g1) + (2 * g2 * Zs)

    """
    shunt admittance of a TEM transmission line
    ko is the free-space wavenumber
    No is the impedance of free space
    epsilon_fm the effective dielectric constant in the modal sense.
    g1 is a geometrical factor, which characterize the particular transmission line being used.
    """

    def shunt_admittance_Y(self, epsilon_fm, g1):
        return 1j * (K0 / N0) * (epsilon_fm / g1)

    # Zc
    def characteristic_impedance(self, Z, Y):
        return cmath.sqrt(Z / Y)

    def propagation_constant(self, Z, Y):
        return cmath.sqrt(Y * Z)

        # TOdo what are these used for where do we calc these?
        # attenuation const
        # alpha = ...
        #
        # # wave number
        #
        # beta = ...
