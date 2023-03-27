"""
this function makes a line model from the gui and returns a floquet line of the model type
            #   test lenths  759.0, 60.0, 1517.9999999999998, 60.0, 1522.9999999999998, 50.0, 764.0

"""
import numpy as np

from simulation.floquet_line_models.models.floquet_line import FloquetLine
from simulation.hfss_sims.hfss_line import hfss_touchstone_floquet_line
from simulation.hfss_sims.hfss_pre_sim_file_line import PreSimFloquetLine
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.super_conducting_transmission_line_models.cpw.super_conducting_cpw_model import CoplanarWaveguideSC
from simulation.super_conducting_transmission_line_models.micro_strip.super_conducting_micro_strip_model import \
    MicroStripSC
from simulation.utills.constants import CPW_TYPE, MICRO_STRIP_TYPE, ARTIFICIAL_CPW_TYPE
from simulation.utills.functions import hertz_to_GHz, microns_to_meters, micro_ohms_cm_to_ohms_m, nano_to_meters


def floquet_line_from_line_model(line_model):
    inputs = line_model.get_inputs()

    super_conductor = inputs.get("super_conductor_properties", {})
    line_dimensions = inputs.get("line_dimensions", {})
    frequency_range = inputs.get("frequency_range", {})
    lu_dimensions = inputs.get("lu_dimensions", {})

    er = float(super_conductor.get("Er", 0))
    height = nano_to_meters(float(super_conductor.get("Height", 0)))
    thickness = nano_to_meters(float(super_conductor.get("Ts", 0)))
    gt = microns_to_meters(float(super_conductor.get("Ground Thickness", 0)))
    op_temp = float(super_conductor.get("Super Conductor Operation Temperature", 0))
    crit_temp = float(super_conductor.get("Super Conductor Critical Temperature", 0))
    ic = float(super_conductor.get("Super Conductor Critical Current", 0))
    pn = micro_ohms_cm_to_ohms_m(float(super_conductor.get("Super Conductor Normal Resistivity", 0)))
    tan_d = float(super_conductor.get("Super Conductor Tangent Delta", 0))

    print(
        f"er:{er} height:{height} ts:{thickness} gt:{gt} op_temp:{op_temp} tc:{crit_temp} ic:{ic} pn:{pn} tan_d:{tan_d}")

    try:
        lengths_widths = [[microns_to_meters(float(length)), microns_to_meters(float(width))]
                          for length, width in line_dimensions.get("lengths_widths", [0, 0])]
    except:
        lengths_widths = []

    cpw_S = microns_to_meters(float(line_dimensions.get("S", 0)))

    n_repeated_cells = int(frequency_range.get("n_repeated_cells", 150))

    print(f"lengths_widths:{lengths_widths} cpw_S:{cpw_S} n_repeated_cells:{n_repeated_cells}")

    lu_S = microns_to_meters(float(lu_dimensions.get("lu_S", 0)))
    lu_WH = microns_to_meters(float(lu_dimensions.get("lu_WH", 0)))
    lu_LH = microns_to_meters(float(lu_dimensions.get("lu_LH", 0)))
    lu_LL = microns_to_meters(float(lu_dimensions.get("lu_LL", 0)))

    print(f"lu_S:{lu_S} lu_WH:{lu_WH} lu_LH:{lu_LH} lu_LL:{lu_LL}")

    model_type = line_model.type

    # fix and simplify gui

    # simulated by mathematical model
    if model_type in [MICRO_STRIP_TYPE, CPW_TYPE, ARTIFICIAL_CPW_TYPE]:

        super_conductivity_model = SuperConductivity(op_temp, crit_temp, pn, thickness)

        unit_cell_line_segments = []
        if model_type == MICRO_STRIP_TYPE:

            unit_cell_line_segments = [
                MicroStripSC(width, length, thickness, height, er, tan_d, ic) for length, width in lengths_widths]

        elif model_type == CPW_TYPE:

            unit_cell_line_segments = [
                CoplanarWaveguideSC(width, length, cpw_S, thickness, er, tan_d, ic) for length, width in lengths_widths]

        elif model_type == ARTIFICIAL_CPW_TYPE:
            line_models = []

            raise NotImplementedError(
                "ARTIFICIAL_CPW waiting on Patricio's new model to implement")

        return FloquetLine(unit_cell_line_segments, super_conductivity_model, n_repeated_cells)


    # MODELS PRE-SIMULATED USING HFSS
    elif model_type in ["HFSS_TOUCHSTONE_FILE", "PRE_SIM_FILE"]:

        if model_type == "HFSS_TOUCHSTONE_FILE":

            hfss_touchstone_file_path = inputs.get("hfss_touchstone_file_path")
            n_interpt_points = int(inputs.get("n_interpt_points"))
            unit_cell_length = float(inputs.get("unit_cell_length"))
            n_repeated_cells = int(inputs.get("n_repeated_cells"))

            return hfss_touchstone_floquet_line(hfss_touchstone_file_path, n_interpt_points, unit_cell_length,
                                                n_repeated_cells)

        elif model_type == "PRE_SIM_FILE":

            wl = float(inputs.get("wl_len"))
            wu = float(inputs.get("wu_len"))
            n_repeated_cells = int(inputs.get("Frequency_Range")["n_repeated_cells"])
            is_art_cpw_line = bool(int(inputs.get("using_art_line")))
            lu_length = microns_to_meters(float(inputs.get("Lu_length")))
            print(inputs)
            line_lengths = np.array([float(n[0]) for n in inputs.get("Dimensions_inputs")["lengths_widths"]])
            csv_data= line_model.csv_data

            return PreSimFloquetLine(csv_data, wl, wu, lu_length, line_lengths, is_art_cpw_line,n_repeated_cells)

    else:
        raise NotImplementedError(
            f"\"{line_model.type}\" not implemented")
