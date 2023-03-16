import cmath


# standanrd format is (z, init_amplitudes,args)
def SIP_MODEL_2(z, init_amplitudes, betas, alphas, gs, delta_beta, I_Star):
    # signal-idler-pump equations for N = 3

    beta_s, beta_i, beta_p = betas
    alpha_s, alpha_i, alpha_p = alphas
    g_s, g_i, g_p = gs

    amp_S, amp_I, amp_P = init_amplitudes

    abs_ampS_sqrd = abs(amp_S) ** 2
    abs_ampI_sqrd = abs(amp_I) ** 2
    abs_ampP_sqrd = abs(amp_P) ** 2

    I_Star_sqrd = I_Star ** 2

    j_db1_z = (1j * delta_beta * z)

    eight_is_sqred = (8 * I_Star_sqrd)

    expj_db1_z = cmath.exp(j_db1_z)

    As = (1j * g_s * amp_S - 2 * alpha_s * amp_S + ((-1j * beta_s) / eight_is_sqred)
          * (amp_S * (abs_ampS_sqrd + 2 * abs_ampI_sqrd + 2 * abs_ampP_sqrd)
             + amp_I.conjugate() * amp_P ** 2 * expj_db1_z))

    Ai = (1j * g_i * amp_I - 2 * alpha_i * amp_I + ((-1j * beta_i) / eight_is_sqred)
          * (amp_I * (2 * abs_ampS_sqrd + abs_ampI_sqrd + 2 * abs_ampP_sqrd)
             + amp_S.conjugate() * amp_P ** 2 * expj_db1_z))

    Ap = (1j * g_p * amp_P - 2 * alpha_p * amp_P + ((-1j * beta_p) / eight_is_sqred)
          * (amp_P * (2 * abs_ampS_sqrd + 2 * abs_ampI_sqrd + abs_ampP_sqrd)
             + 2 * amp_P.conjugate() * amp_S * amp_I * cmath.exp(-j_db1_z)))

    return [As, Ai, Ap]
