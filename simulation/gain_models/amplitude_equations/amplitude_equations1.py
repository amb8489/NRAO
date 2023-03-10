import cmath


# standanrd format is (z, init_amplitudes,args)
def SIP_MODEL_1(z, init_amplitudes,   beta_s, beta_i, beta_p, delta_beta, I_Star):
    # signal-idler-pump equations for N = 3

    amp_S, amp_I, amp_P = init_amplitudes

    abs_ampS_sqrd = abs(amp_S) ** 2
    abs_ampI_sqrd = abs(amp_I) ** 2
    abs_ampP_sqrd = abs(amp_P) ** 2

    I_Star_sqrd = I_Star ** 2

    j_db1_z = (1j * delta_beta * z)

    eight_is_sqred = (8 * I_Star_sqrd)

    expj_db1_z = cmath.exp(j_db1_z)

    As = (((-1j * beta_s) / eight_is_sqred)
          * (amp_S * (abs_ampS_sqrd + 2 * abs_ampI_sqrd + 2 * abs_ampP_sqrd)
             + amp_I.conjugate() * amp_P ** 2 * expj_db1_z))

    Ai = (((-1j * beta_i) / eight_is_sqred)
          * (amp_I * (2 * abs_ampS_sqrd + abs_ampI_sqrd + 2 * abs_ampP_sqrd)
             + amp_S.conjugate() * amp_P ** 2 * expj_db1_z))

    Ap = (((-1j * beta_p) / eight_is_sqred)
          * (amp_P * (2 * abs_ampS_sqrd + 2 * abs_ampI_sqrd + abs_ampP_sqrd)
             + 2 * amp_P.conjugate() * amp_S * amp_I * cmath.exp(-j_db1_z)))

    return [As, Ai, Ap]
