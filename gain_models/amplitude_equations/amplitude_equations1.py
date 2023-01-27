import cmath


# todo make standanrd format (amplitudes, z ,args)

def AmplitudeEqs1(amplitudes, z, beta_signals, beta_idler, beta_pump):
    # signal-idler-pump equations for N = 3

    A_sig = amplitudes[0]
    A_idler = amplitudes[1]
    A_pump = amplitudes[2]

    # conj amplitudes
    A_star_s = amplitudes[0].conjugate()
    A_star_i = amplitudes[1].conjugate()
    A_star_p = amplitudes[2].conjugate()

    deltaB = (beta_signals + beta_idler) - (2 * beta_pump)

    # Optical coupled equations

    AmplitudeSignal = ((-1j * (beta_signals / 8)) * (A_sig * ((abs(A_sig) ** 2) + (2 * (abs(A_idler) ** 2)) +
                                                              (2 * (abs(A_pump) ** 2))) + A_star_i * (
                                                             A_pump ** 2) * cmath.exp(1j * deltaB * z)))

    AmplitudeIdler = ((-1j * (beta_idler / 8)) * (A_idler * ((2 * (abs(A_sig) ** 2)) + (abs(A_idler) ** 2) +
                                                             (2 * (abs(A_pump) ** 2))) + A_star_s * (
                                                          A_pump ** 2) * cmath.exp(1j * deltaB * z)))

    AmplitudePump = ((-1j * (beta_pump / 8)) * (A_pump * (2 * (abs(A_sig) ** 2) + (2 * (abs(A_idler) ** 2)) +
                                                          (
                                                                  abs(A_pump) ** 2)) + 2 * A_star_p * A_sig * A_idler * cmath.exp(
        -1j * deltaB * z)))

    return [AmplitudeSignal, AmplitudeIdler, AmplitudePump]