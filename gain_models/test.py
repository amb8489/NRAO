






import numpy as np
from scipy.integrate import solve_ivp

def ODE(z, y, alpha1, Kp, Ks, Ki, delta_beta):
    Ap, As, Ai = y
    dAp_dz = alpha1 * 1j * Kp * ((np.abs(Ap)**2 + 2 * np.abs(As)**2 + 2 * np.abs(Ai)**2) * Ap + 2 * As * Ai * np.conj(Ap) * np.exp(1j * delta_beta * z))
    dAs_dz = alpha1 * 1j * Ks * ((np.abs(As)**2 + 2 * np.abs(Ai)**2 + 2 * np.abs(Ap)**2) * As + Ai * np.conj(Ap)**2 * np.exp(-1j * delta_beta * z))
    dAi_dz = alpha1 * 1j * Ki * ((np.abs(Ai)**2 + 2 * np.abs(As)**2 + 2 * np.abs(Ap)**2) * Ai + As * np.conj(Ap)**2 * np.exp(-1j * delta_beta * z))
    return [dAp_dz, dAs_dz, dAi_dz]

def solve(L, alpha1, Kp, Ks, Ki, delta_beta, Ap0, As0):
    sol = solve_ivp(fun=lambda z, y: ODE(z, y, alpha1, Kp, Ks, Ki, delta_beta),
                    t_span=(0, L),
                    y0=[Ap0, As0, 0],
                    method='RK45')
    return sol




