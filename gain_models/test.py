import scipy


def solve(L, alpha1, Kp, Ks, Ki, delta_beta, Ap0, As0):
    sol = solve_ivp(fun=lambda z, y: ODE(z, y, alpha1, Kp, Ks, Ki, delta_beta),
                    t_span=(0, L),
                    y0=[Ap0, As0, 0],
                    method='RK45')
    return sol


import numpy as np
from scipy.integrate import solve_ivp


def ODE(z, y, alpha1, Kp, Ks, Ki, delta_beta):
    Ap, As, Ai = y
    dAp_dz = alpha1 * 1j * Kp * (
            (np.abs(Ap) ** 2 + 2 * np.abs(As) ** 2 + 2 * np.abs(Ai) ** 2) * Ap + 2 * As * Ai * np.conj(Ap) * np.exp(
        1j * delta_beta * z))
    dAs_dz = alpha1 * 1j * Ks * (
            (np.abs(As) ** 2 + 2 * np.abs(Ai) ** 2 + 2 * np.abs(Ap) ** 2) * As + Ai * np.conj(Ap) ** 2 * np.exp(
        -1j * delta_beta * z))
    dAi_dz = alpha1 * 1j * Ki * (
            (np.abs(Ai) ** 2 + 2 * np.abs(As) ** 2 + 2 * np.abs(Ap) ** 2) * Ai + As * np.conj(Ap) ** 2 * np.exp(
        -1j * delta_beta * z))
    return [dAp_dz, dAs_dz, dAi_dz]


def dB(Gs):
    return Gs


def beta_at(frequency):
    return 0


def GainFWM(alpha_k, Ap0, As0, L, frequency_pump, frequency_signal):
    I1I = np.sqrt(2 / alpha_k)
    alpha1 = 1 / I1I ** 2
    frequency_idler = 2 * frequency_pump - frequency_signal

    # working on this
    Kp = beta_at(frequency_pump)
    Ks = beta_at(frequency_signal)
    Ki = beta_at(frequency_idler)

    Delta_beta = Ks + Ki - 2 * Kp

    sol = solve_ivp(fun=lambda z, y: ODE(z, y, alpha1, Kp, Ks, Ki, Delta_beta),
                    t_span=(0, L),#ff
                    y0=[Ap0+0j, As0+0j, 0+0j],
                    method='RK45')

    return dB(sol[1][L])






# javeir code


def solve_amplitudeEqs_3signals_sip_noDiss_F(params, z_eval, A0, method):
    def fun(params):
        def fun_internal(z, y):
            A1, A2, A3 = y

            #sCmat_params, w, gamma, R, G, C, L0, f_coeffs = params
            sCmat_params, w, gamma, eta, f_coeffs = params

            alph, I_star = sCmat_params
            w1, w2, w3 = w
            #gamma = np.array(gamma)
            gamma1, gamma2, gamma3 = gamma
            eta1, eta2, eta3 = eta
            #C1, C2, C3 = C
            #R1, R2, R3 = [0, 0, 0]
            #G1, G2, G3 = [0, 0, 0]
            #L01, L02, L03 = L0

            f0, f1, f2, f3, f4, f5 = f_coeffs
            f01, f02, f03 = f0
            f11, f12, f13 = f1
            f21, f22, f23 = f2
            f31, f32, f33 = f3
            f41, f42, f43 = f4
            f51, f52, f53 = f5

            beta1, beta2, beta3 = np.imag(np.array(gamma))
            alpha1, alpha2, alpha3 = [0, 0, 0]

            #Db = 2 * beta3 - (beta1 + beta2)

            #Da1 = 2 * alpha3 + alpha2 - alpha1
            #Da2 = 2 * alpha3 + alpha1 - alpha2
            #Da3 = alpha1 + alpha2

            factor1 = -1j * beta1
            factor2 = -1j * beta2
            factor3 = -1j * beta3

            Dbeta = beta1 + beta2 - 2 * beta3

            fun1 = alph * factor1 / (3 * 8 * I_star ** 2)\
                         * (f01 * (A1 * (f11 * np.abs(A1) ** 2\
                                        + f21 * np.abs(A2) ** 2\
                                        + f31 * np.abs(A3) ** 2)\
                                  + f51 * np.exp(1j * Dbeta * z) * np.conj(A2) * A3 ** 2))

            fun2 = alph * factor2 / (3 * 8 * I_star ** 2)\
                        * (f02 * (A2 * (f12 * np.abs(A1) ** 2\
                                        + f22 * np.abs(A2) ** 2\
                                        + f32 * np.abs(A3) ** 2)\
                                  + f52 * np.exp(1j * Dbeta * z) * np.conj(A1) * A3 ** 2))

            fun3 = alph * factor3 / (3 * 8 * I_star ** 2)\
                        * (f03 * (A3 * (f13 * np.abs(A1) ** 2\
                                        + f23 * np.abs(A2) ** 2\
                                        + f33 * np.abs(A3) ** 2)\
                                  + f53 * np.exp(-1j * Dbeta * z) * np.conj(A3) * A1 * A2))

            fun_vector = np.array([fun1, fun2, fun3])
            return fun_vector
        return fun_internal

    z0 = z_eval[0]
    z_end = z_eval[-1]
    z_span = (z0, z_end)
    zstep = (z_eval[-1] - z0) / (len(z_eval) - 1)

    y0 = np.array(A0)

    sol = scipy.solve_ivp(fun(params), z_span, y0, t_eval=z_eval, method=method,
                          max_step=zstep*0.1)#, atol=1e-8)#, first_step=zstep*0.05)

    return sol




