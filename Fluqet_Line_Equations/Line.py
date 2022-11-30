class Line():

    def __init__(self, D, D0, number_of_loads, In_Order_loads_Widths):


        if number_of_loads < 1:
            raise Exception(f"number of loads has to be >= 1: passed in {number_of_loads}")

        if number_of_loads != len(In_Order_loads_Widths):
            raise Exception("number_of_loads != amount of load widths passed in")

        self.D = D
        self.D0 = D0
        self.number_of_loads = number_of_loads
        self.In_Order_loads_Widths = In_Order_loads_Widths

        # add imaginay loads of widths zero to front and back to simplify code
        self.In_Order_loads_Widths = [0] + self.In_Order_loads_Widths + [0]

        self.Floquet_Line_Parts_Lengths = []

        # combute the lrngths of the ccentral lines between the loads
        #todo in paper the first and last is D0/2 - (loadlen/2) if so coud change ([D0/2] + self.In_Order_loads_Widths + [D0/2])
        for i in range(number_of_loads + 1):
            if i != 0: self.Floquet_Line_Parts_Lengths.append(self.In_Order_loads_Widths[i])
            self.Floquet_Line_Parts_Lengths.append(
                D0 - (self.In_Order_loads_Widths[i] / 2) - (self.In_Order_loads_Widths[i + 1] / 2))

        if abs(D - sum(self.Floquet_Line_Parts_Lengths)) > 0.001:
            raise Exception("sum of loads and central line lenths do not add to expected total length of line D")

        self.In_Order_loads_Widths = self.In_Order_loads_Widths[1:-1]

    def get_L_number(self, partNumber):

        try:
            return self.Floquet_Line_Parts_Lengths[partNumber]
        except IndexError:
            raise Exception(f"out of bounds, Floquet Line only has {self.number_of_loads*2+1} segments")
        except:
            raise Exception("partNumber must be a number")


