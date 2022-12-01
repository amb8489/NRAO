'''

class to represent a floquet line

given:
 -D: the len of unit cell
 -D0: spacing between centers of loads
 -number_of_loads : the number of loads in unit cell
 -In_Order_loads_Widths: the lengths of each load from left to right in Floquet line
    ex: -----[   3   ] ----- [  2  ]-----[ 1 ] -----
    In_Order_loads_Widths = [3,2,1]
'''
from Supports.Support_Functions import microMeters_to_Meters


class Line():

    def __init__(self, D: float, D0: float, number_of_loads: int, In_Order_loads_Widths: [float]):

        # param checking for correctness
        if number_of_loads < 1:
            raise Exception(f"number of loads has to be >= 1: passed in {number_of_loads}")

        if number_of_loads != len(In_Order_loads_Widths):
            raise Exception("number_of_loads != amount of load widths passed in")

        # saving usefull info
        self.D = D
        self.D0 = D0
        self.number_of_loads = number_of_loads
        self.In_Order_loads_Widths = In_Order_loads_Widths

        # array to hold lengths of line segments of the FL
        self.Floquet_Line_Parts_Lengths = []

        # todo in paper the first and last is D0/2 - (loadlen/2) if so coud change ([D0] + self.In_Order_loads_Widths + [D0])
        # add D0 widths loads to front and back to simplify code in calculating segments
        self.In_Order_loads_Widths = [D0] + self.In_Order_loads_Widths + [D0]

        # compute the lengths of the ccentral lines between the loads
        for i in range(number_of_loads + 1):

            # add the load length just not thr first 0
            if i != 0: self.Floquet_Line_Parts_Lengths.append(self.In_Order_loads_Widths[i])

            # compute and add length of the central line between load[i] and load[i+1]   [load i] ---CL--- [load i+1]
            self.Floquet_Line_Parts_Lengths.append(
                D0 - (self.In_Order_loads_Widths[i] / 2) - (self.In_Order_loads_Widths[i + 1] / 2))

        # check to make sure sum of lengths adds up to unit cell length
        if abs(D - sum(self.Floquet_Line_Parts_Lengths)) > 0.001:
            raise Exception(
                f"sum of loads and central line lenths do not add to expected total length of line D {D - sum(self.Floquet_Line_Parts_Lengths)}")
        self.In_Order_loads_Widths = In_Order_loads_Widths

    # returns the length of the wanted segment in FL
    def get_L_number(self, partNumber: int):
        return self.Floquet_Line_Parts_Lengths[partNumber]
