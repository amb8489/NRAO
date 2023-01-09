from random import choice


def randomColor():
    # return "#DDDDDD"
    return "#" + "".join([choice("ABCDEF012345689") for i in range(6)])
