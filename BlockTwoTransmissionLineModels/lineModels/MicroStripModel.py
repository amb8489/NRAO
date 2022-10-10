import math
import cmath
from Supports.constants import PI, MU_0, PI2, z0, PI4, PLANCK_CONST_REDUCEDev, K0, N0, c
from Supports.Support_Functions import sech, coth, ccoth
from TransmissionLineModels.lineModels.Model import TransmissionLineModel

"""

    MICRO STRIP MODEL FOR TRANSMISSION LINE
    
    
    NRAO
    Aaron Berghash

    Formulas from https://qucs.sourceforge.net/tech/node75.html#SECTION001211200000000000000

    Penetration depth & Surface Impedance _ kautz "picoseconds pulses on super conducting strip lines"

    
"""


# TODO COMMENT ALL IMPORTANT FUNCTIONS from mathimatica code AND TEST

class MicroStripModel(TransmissionLineModel):

    # TODO all geometrical dimensions needed, tan
    def __int__(self, height, width, thickness, epsilon_r, tan_delta):

        # todo use these in the model calculations
        self.height = height
        self.width = thickness
        self.thickness = thickness
        self.epsilon_r = epsilon_r
        self.tan_delta = tan_delta

    # ----------  schneider   t = 0  ----------
    def Fs(self, w, h):
        return math.sqrt(1 + (10 * (h / w)))

    def epsilon_effs(self, epsilon_r, w, h):
        return ((epsilon_r + 1) / 2) + ((epsilon_r - 1) / (2 * self.Fs(w, h)))

    def zmss(self, epsilon_r, w, h):
        z0eff = z0 / (math.sqrt(self.epsilon_effs(epsilon_r, w, h)))

        if w / h <= 1:
            return z0eff * (1 / PI2) * math.log(((8 * h) / w) + (w / (4 * h)))

        return z0eff / ((w / h) + 2.42 - (0.44 * (h / w)) + pow(1 - (h / w), 6))

    # ----------  schneider   t > 0  ----------

    def epsilon_effst(self, epsilon_r, w, h, t):
        u = w / h

        if u <= (1 / PI2):
            delta_w = (t / PI) * (1 + math.log((PI4 * w) / t))
        else:
            delta_w = (t / PI) * (1 + math.log((2 * h) / t))

        return self.epsilon_effs(epsilon_r, w + delta_w, h)

    def zmsst(self, epsilon_r, w, h, t):
        u = w / h

        if u <= (1 / PI2):
            delta_w = (t / PI) * (1 + math.log((PI4 * w) / t))
        else:
            delta_w = (t / PI) * (1 + math.log((2 * h) / t))

        return self.zmss(epsilon_r, w + delta_w, h)

    # ----------  Hammerstad   t = 0  ----------

    def epsilon_effh(self, epsilon_r, w, h):
        u = w / h

        u4 = pow(u, 4)

        firstLog = math.log((u4 + pow(u / 52, 2)) / (u4 + 0.432))
        secondLog = math.log(1 + pow(u / 18.1, 3))

        a = 1 + (1 / 49) * firstLog + (1 / 18.7) * secondLog

        b = 0.564 * pow((epsilon_r - .9) / (epsilon_r + 3), 0.053)

        return ((epsilon_r + 1) / 2) + ((epsilon_r - 1) / 2) * pow(1 + (10 / u), -a * b)

    def ZL1(self, w, h):
        u = w / h

        fu = 6 + (PI2 - 6) * math.exp(-pow(30.666 / u, 0.7528))

        return (z0 / PI2) * math.log((fu / u) + math.sqrt(1 + pow(2 / u, 2)))

    # ----------  Hammerstad   t > 0  ----------

    def delta_wr(self, epsilon_r, w, h, t):
        return (self.delta_w1(w, h, t) * (1 + sech(math.sqrt(epsilon_r - 1)))) / 2

    def delta_w1(self, w, h, t):
        u = w / h
        th = t / h

        upper = 4 * math.e
        lower = th * pow(coth(math.sqrt(6.517 * u)), 2)

        return (t / PI) * math.log(1 + (upper / lower))

    def epsilon_effht(self, epsilon_r, w, h, t):
        w1 = w + self.delta_w1(w, h, t)
        wr = w + self.delta_wr(epsilon_r, w, h, t)

        zl1_up = self.ZL1(w1, h)
        zl1_low = self.ZL1(wr, h)
        return self.epsilon_effh(epsilon_r, wr, h) * pow(zl1_up / zl1_low, 2)

    def Zmsht(self, epsilon_r, w, h, t):
        wr = w + self.delta_wr(epsilon_r, w, h, t)
        upper = self.ZL1(wr, h)
        lower = math.sqrt(self.epsilon_effht(epsilon_r, wr, h, t))

        return upper / lower

    # -------------------

    def Lambda0(self, sigma_N, delta_O):
        # TODO ask about the complex square root should just the real part be rooted or both re and im parts
        # AND sigma_N is 1/ Pn
        return math.sqrt(PLANCK_CONST_REDUCEDev / (PI * MU_0 * sigma_N * delta_O))

    # todo what is t used for?
    def z_slow(self, f, yO, t):
        return 1j * PI2 * f * MU_0 * yO

    # todo what is t used for?
    def Lambda(self, zs, f, t):
        return (zs / (PI2 * f * MU_0)).imag

    # -------------- super conducting equations for miro strip ----------------

    # Geometrical factors

    def g1(self, w, h, t):
        return h / (w * self.Kf(w, h, t))

    def g2(self, w, h, t):
        return self.Kl(w, h, t) / w

    # ------ helper functions ----------

    def ra(self, w, h, p):
        sqrtP = math.sqrt(p)

        return math.exp(
            -1 - ((PI * w) / (2 * h)) - ((p + 1) / (sqrtP)) * math.atanh(sqrtP) - math.log((p - 1) / (4 * p)))

    def rb(self, w, h, rbo, p):
        if (w / h >= 5):
            return rbo
        sqrtP = math.sqrt(p)
        return rbo - (math.sqrt((rbo - 1) * (rbo - p)) + (p + 1) * math.atanh(
            math.sqrt((rbo - p) / (rbo - 1))) - 2 * sqrtP *
                      math.atanh((rbo - p) / (p * (rbo - 1))) + ((PI * w) / (2 * h)) * sqrtP
                      )

    def Eta(self, w, h, p):
        sqrtP = math.sqrt(p)

        return sqrtP * (((PI * w) / (2 * h)) + ((p + 1) / (2 * sqrtP)) * (1 + math.log(4 / (p - 1))) - 2 * math.atanh(
            pow(p, -1 / 2)))

    def b(self, h, t):
        return 1 + (t / h)

    def p(self, b):

        bsqrd = b ** 2

        return 2 * bsqrd - 1 + 2 * b * math.sqrt(bsqrd - 1)

    def rbo(self, eta, p, detaY):
        return eta + ((p + 1) / 2) * math.log(detaY)

    def DeltaY(self, eta, p):

        return max(eta, p)
        # return Eta if Eta > p else p

    def Kf(self, w, h, t):

        bc = b(h, t)

        pc = p(bc)

        rac = ra(w, h, pc)

        EtaC = Eta(w, h, pc)

        DeltaYC = DeltaY(EtaC, pc)

        rboc = rbo(EtaC, pc, DeltaYC)

        rbc = rb(w, h, rboc, pc)

        return (h / w) * (2 / PI) * math.log((2 * rbc) / rac)

    def Kl(self, w, h, t):
        return self.chi(w, h, t) / self.Kf(w, h, t)

    def Is1(self, p, ra, Ra):
        return math.log((2 * p - (p + 1) * ra + 2 * math.sqrt(p * Ra)) / (ra * (p - 1)))

    def Ra(self, p, ra):
        return (1 - ra) * (p - ra)

    def Is2(self, p, rb, Rb):
        return - math.log(((p + 1) * rb - 2 * p - 2 * math.sqrt(p * Rb)) / (rb * (p - 1)))

    def Rb(self, p, rb):
        return (rb - 1) * (rb - p)

    def Ig1(self, p, rb, Rb1):
        return -math.log(((p + 1) * rb + 2 * p + 2 * math.sqrt(p * Rb1)) / (rb * (p - 1)))

    def Rb1(self, p, rb):
        return (rb + 1) * (rb + p)

    def Ig2(self, p, ra, Ra1):
        return math.log(((p + 1) * ra + 2 * p + 2 * math.sqrt(p * Ra1)) / (ra * (p - 1)))

    def Ra1(self, p, ra):
        return (ra + 1) * (ra + p)

    def X(self, zs, f, w, H, ts):

        ChiC = self.Chi(w, H, ts)
        ko = (PI2 * f) / c
        return (2 * ChiC * zs) / (ko * z0 * H)

    def ZSy(self, est, zs, f, epsilon_r, w, H, ts):
        zmst = zt(epsilon_r, w, H, ts)
        return zmst * (cmath.sqrt(1 - 1j * X(zs, f, w, H, ts))).real

    def beta_Soy(self, est, zs, f, epsilon_r, w, H, ts):
        epsilon_fm = est(epsilon_r, w, H, ts)
        return cmath.sqrt(epsilon_fm) * (cmath.sqrt(1 - 1j * X(zs, f, w, H, ts))).real

    def aplha_Sy(self, est, zs, f, epsilon_r, w, H, ts):
        epsilon_fm = est(epsilon_r, w, H, ts)
        return - cmath.sqrt(epsilon_fm) * (cmath.sqrt(1 - 1j * X(zs, f, w, H, ts))).imag

    def apha_ky(self, est, zs, f, epsilon_r, w, H, ts):
        CF = (cmath.sqrt(1 - 1j * X(zs, f, w, H, ts))).real
        return 1 - (1 / CF ** 2)

    def vSy(self, est, zs, f, epsilon_r, w, H, ts):
        epsilon_fm = est(epsilon_r, w, H, ts)
        CF = (cmath.sqrt(1 - 1j * X(zs, f, w, H, ts))).real
        return 1 / (math.sqrt(epsilon_fm) * CF)

    def Beta_Syloss(self, est, zs, f, epsilon_r, tand, w, H, ts):
        epsilon_fm = est(epsilon_r, w, H, ts)

        epsilon_t = epsilon_fm - 1j * epsilon_r * tand

        return (cmath.sqrt(epsilon_t) * cmath.sqrt(1 - 1j * X(zs, f, w, H, ts))).real

    def AlphaSyloss(self, est, zs, f, epsilon_r, tand, w, H, ts):
        epsilon_fm = est(epsilon_r, w, H, ts)

        epsilon_t = epsilon_fm - 1j * epsilon_r * tand

        return -(cmath.sqrt(epsilon_t) * cmath.sqrt(1 - 1j * X(zs, f, w, H, ts))).imag

    def chi(self, w, h, t):
        bc = self.b(h, t)
        pc = self.p(bc)
        rac = self.ra(w, h, pc)
        EtaC = self.Eta(w, h, pc)
        DeltaYC = self.DeltaY(EtaC, pc)
        rboc = self.rbo(EtaC, pc, DeltaYC)
        rbc = self.rb(w, h, rboc, pc)
        Rac = self.Ra(pc, rac)
        Is1c = self.Is1(pc, rac, Rac)
        Rbc = self.Rb(pc, rbc)
        Is2c = self.Is2(pc, rbc, Rbc)
        Rb1c = self.Ra(pc, rbc)
        Ig1c = self.Ig1(pc, rbc, Rb1c)
        Ra1c = self.Ra(pc, rac)
        Ig2c = self.Ig2(pc, rac, Ra1c)

        if (w / h) < 2:
            return (Is1c + Is2c + Ig1c + Ig2c + PI) / (2 * math.log(rbc / rac))
        return (Is1c + Is2c + Ig1c + Ig2c + PI) / (2 * math.log(2 * rbc / rac))

    """
    series impedance of a TEM transmission line
    ko is the free-space wavenumber
    No is the impedance of free space
    Zs, is the surface impedance of the conductors
    g1 and g2 are geometrical factors, which characterize the particular transmission line being used.
    """

    def series_impedance_Z(self, Zs, g1, g2):
        return (1j * (K0 * N0) * g1) + (2 * g2 * Zs)

    """
    shunt admittance of a TEM transmission line
    ko is the free-space wavenumber
    No is the impedance of free space
    epsilon_fm the effective dielectric constant in the modal sense.
    g1 is a geometrical factor, which characterize the particular transmission line being used.
    """

    # TODO where does is epsilon_fm come from and is it model dependent
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
