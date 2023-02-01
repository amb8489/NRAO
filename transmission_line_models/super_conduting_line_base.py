class superConductingLineEquations():

    # todo
    def __init__(self, g1, g2, efm):
        self.efm = ...
        self.g2_ground = ...
        self.g2_central_line = ...
        self.g1 = ...
        self.g2_list = [self.g2_ground, self.g2_central_line]

    # -----------------------

    '''
    PARAMETRIC AMPLIFICATION OF ELECTROMAGNETIC SIGNALS WITH SUPERCONDUCTING TRANSMISSION LINES
    TESIS PARA OPTAR AL GRADO DE
    MAGÍSTER EN CIENCIAS DE LA INGENIERÍA, MENCIÓN ELÉCTRICA
    JAVIER ALEJANDRO CARRASCO ÁVILA
    
    
    UNIVERSIDAD DE CHILE
    FACULTAD DE CIENCIAS FÍSICAS Y MATEMÁTICAS DEPARTAMENTO DE INGENIERÍA ELÉCTRICA
    
    '''

    # equations from
    def G2(self, g1, width, ground_spacing, thickness, a, b, thickness_sc):
        dsc = thickness_sc / PI

        w1 = a + (dsc / 2) - ((dsc / 2) * math.log(dsc / a) + (3 / 2) * dsc * math.log(2)) - (dsc / 2) * math.log(
            (a + b) / (b - a))

        w2 = b - (dsc / 2) + ((dsc / 2) * math.log(dsc / b) - ((3 / 2) * dsc * math.log(2))) + (dsc / 2) * math.log(
            (a + b) / (b - a))

        k = w1 / w2

        k_prime = math.sqrt(1 - k ** 2)

        elliptic_k = ellip_k(k)

        elliptic_k_prime = ellip_k(k_prime)

        log_diff_div = math.log((b - a) / (b + a))

        G2_central_line = (g1 / (8 * elliptic_k * elliptic_k_prime * (1 - k ** 2))) * (
                (PI / a) + (1 / a) * math.log((8 * a) / dsc) + (1 / b) * log_diff_div)

        G2_ground_surfaces = (g1 / (4 * elliptic_k * elliptic_k_prime * (1 - k ** 2))) * (
                (PI / b) + (1 / b) * math.log((8 * b) / dsc) + (1 / a) * log_diff_div)

        return [G2_central_line, G2_ground_surfaces]

    def G1(self, k, k_prime):
        return ellip_k(k_prime) / (4 * ellip_k(k))

    # todo move this into the abstract class or make the this class inhearet from a new class
    # Zc
    def characteristic_impedance(self, Z, Y):
        return cmath.sqrt(Z / Y)

    # todo move this into the abstract class or make the this class inhearet from a new class
    # gamma
    def propagation_constant(self, Z, Y):
        return cmath.sqrt(Z * Y)

    def epsilon_fm(self, er, tand):
        return ((er + 1) / 2) * (1 - 1j * tand)

    # todo move this into the abstract class or make the this class inhearet from a new class
    def shunt_admittance_Y(self, epsilon_fm, g1, f):
        return 1j * (K0(f) / Z0) * (epsilon_fm / g1)

    # todo move this into the abstract class
    def series_impedance_Z(self, g1, list_of_g2, list_of_Zs, f):
        assert len(list_of_Zs) == len(list_of_g2), f"should be an equal number of g2 and Zs"
        return (1j * (K0(f) * Z0) * g1) + (2 * sum([g2_n * Zs_n for g2_n, Zs_n in zip(list_of_g2, list_of_Zs)]))

    # todo move this into the abstract class
    def get_propagation_constant_characteristic_impedance(self, freq, zs):
        # todo what is zs for ground and line g2 and make a list
        Z = self.series_impedance_Z(self.g1, self.g2_list, [zs], freq)
        Y = self.shunt_admittance_Y(self.efm, self.g1, freq)

        propagation_constant = cmath.sqrt(Z * Y)
        characteristic_impedance_Zc = cmath.sqrt(Z / Y)
        return propagation_constant, characteristic_impedance_Zc
