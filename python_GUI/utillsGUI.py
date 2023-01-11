from random import choice


def randomColor():
    return "#05" + "".join([choice("012345689ABCDEF") for i in range(4)])


def randomColorBright():
    return "#" + "".join([choice("689ABCD") for i in range(6)])
