from transmission_line_models.artificial_cpw.super_conducting_artificial_cpw_model import \
    SuperConductingArtificialCPWLine
from utills.functions import micro_meters_to_meters, toGHz

frequency = toGHz(2.5)

Ncells = 62

# floquet dimensions

floquet_central_line_Wu = micro_meters_to_meters(19)
floquet_load_Wl = micro_meters_to_meters(35)

L1, N1 = micro_meters_to_meters(660), micro_meters_to_meters(110)

l1, n1 = micro_meters_to_meters(240), micro_meters_to_meters(40)

L2, N2 = micro_meters_to_meters(1326), micro_meters_to_meters(221)

l2, n2 = micro_meters_to_meters(240), micro_meters_to_meters(40)

L3, N3 = micro_meters_to_meters(1206), micro_meters_to_meters(201)

l3, n3 = micro_meters_to_meters(480), micro_meters_to_meters(80)

L4, N4 = micro_meters_to_meters(558), micro_meters_to_meters(93)

d, Nd = micro_meters_to_meters(4710), micro_meters_to_meters(785)

'''

            dimensions for a single line

'''

# central line
finger_central_line_length_LH = micro_meters_to_meters(1)
finger_central_line_width_WH = micro_meters_to_meters(1)

# load
finger_load_length_LL = micro_meters_to_meters(1)
finger_load_width_WL = micro_meters_to_meters(1)

# ground spacing
S = micro_meters_to_meters(1)

number_of_fingers = 110

epsilon_r = ...
thickness = ...
height = ...

line = SuperConductingArtificialCPWLine(finger_central_line_length_LH,
                                        finger_central_line_width_WH,
                                        finger_load_length_LL,
                                        finger_load_width_WL,
                                        S,
                                        number_of_fingers,
                                        epsilon_r,
                                        thickness,
                                        height)
