from transmission_line_models.artificial_cpw.super_conducting_artificial_cpw_model import \
    SuperConductingArtificialCPWLine
from utills.functions import micro_meters_to_meters, toGHz

frequency = toGHz(2.5)

Ncells = 62

# floquet dimensions

floquet_central_line_Wu = micro_meters_to_meters(19)
floquet_load_Wl = micro_meters_to_meters(35)

N1 = ...
N2 = ...
N3 = ...
N4 = ...
N5 = ...
N6 = ...
N7 = ...

L1 = ...  # Lu1 * N1
L2 = ...
L3 = ...
L4 = ...
L5 = ...
L6 = ...
L7 = ...

'''

            dimensions for a single line

'''

# central line
central_line_length_LH = micro_meters_to_meters(1)
central_line_width_WH = micro_meters_to_meters(1)

# load
load_length_LL = micro_meters_to_meters(1)
load_width_WL = micro_meters_to_meters(1)

# ground spacing
S = micro_meters_to_meters(1)

number_of_fingers = 110

epsilon_r = .0000156
thickness = micro_meters_to_meters(1)
height = micro_meters_to_meters(1)

line = SuperConductingArtificialCPWLine(central_line_length_LH,
                                        central_line_width_WH,
                                        load_length_LL,
                                        load_width_WL,
                                        S,
                                        number_of_fingers,
                                        epsilon_r,
                                        thickness,
                                        height)

print(line.get_propagation_constant_characteristic_impedance(2.5 * 10 ** 9, 0))
