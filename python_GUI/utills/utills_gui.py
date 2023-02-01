import random
from random import choice

from python_gui.utills.unit import nameUnit


def rft():
    return random.random()


def fit():
    return random.randint(1, 50)


def randomColor():
    return "#" + "".join([choice("012345689ABCDEF") for i in range(6)])


def randomColorBright():
    return "#" + "".join([choice("689ABCD") for i in range(6)])


# TODO MAKE NOT RELITIVE TO MY COMPUTER
SETTINGS_FILE_PATH = "/Users/aaron/PycharmProjects/NRAO/python_gui/setting/settings.txt"

MICRO_METER = "μm"
MILLI_METER = "mm"
NANO_METER = "nm"
KELVIN = "K"
OHMS = "Ω"
MICRO_OHMS_CM = "μΩ.cm"
GHZ = "GHz"

Er = nameUnit("Er")
SC_height = nameUnit("Height", NANO_METER)
SC_ground_thickness = nameUnit("Ground Thickness", MICRO_METER)
SC_thickness = nameUnit("Ts", NANO_METER)
SC_operation_temperature = nameUnit("Super Conductor Operation Temperature", KELVIN)
SC_critical_temperature = nameUnit("Super Conductor Critical Temperature", KELVIN)
SC_critical_current = nameUnit("Super Conductor Critical Current", OHMS)
SC_normal_resistivity = nameUnit("Super Conductor Normal Resistivity", MICRO_OHMS_CM)
SC_tangent_delta = nameUnit("Super Conductor Tangent Delta")
unit_cell_length = nameUnit("Unit Cell Length", MILLI_METER)
central_line_width = nameUnit("Central Line Width", MICRO_METER)
D0 = nameUnit("D0", MILLI_METER)
ground_spacing = nameUnit("S", MICRO_METER)


start_frequency =  nameUnit("Start Frequency", GHZ)
end_frequency =  nameUnit("End Frequency", GHZ)
resolution =  nameUnit("Resolution")

pump_frequency =  nameUnit("Pump Frequency", GHZ)
signal_amplitude =  nameUnit("Signal Amplitude")
idler_amplitude =  nameUnit("Idler Amplitude")
pump_amplitude =  nameUnit("Pump Amplitude")




