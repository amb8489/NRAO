import math
import cmath
from Supports.constants import PI, MU_0, PI2, z0, PI4, PLANCK_CONST_REDUCEDev
from Supports.Support_Functions import sech, coth, ccoth
from HomogeneousPerfectTransLine.lineModels.Model import TransmissionLineModel


class MicroStripModel(TransmissionLineModel):

    # TODO all things needed for a microstrip
    # TODO all geometrical dimensions needed
    def __int__(self, height, width, thickness, epsilon_r):

        # todo use these in the model
        height, width, thickness, epsilon_r = height, width, thickness, epsilon_r

    # TODO w,h,epsilon_r,t

    """
    NRAO
    Aaron Berghash

    Formulas from https://qucs.sourceforge.net/tech/node75.html#SECTION001211200000000000000

    Penetration depth & Surface Impedance _ kautz "picoseconds pulses on super conducting strip lines"

    g1 g2 are model dependent
    """

    # TODO does all of this only for a micro strip model

    import math
    import cmath
    from Supports.constants import PI, MU_0, PI2, z0, PI4, PLANCK_CONST_REDUCEDev
    from Supports.Support_Functions import sech, coth, ccoth

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

    # TODO geometrical factors
    def g2(self):
        pass

    def g1(self):
        pass
