from random import choice


def randomColor():
    return "#" + "".join([choice("012345689ABCDEF") for i in range(6)])


def randomColorBright():
    return "#" + "".join([choice("689ABCD") for i in range(6)])
