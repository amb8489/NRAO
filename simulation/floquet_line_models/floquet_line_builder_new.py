"""
this function makes a line model from the gui and returns a floquet line of the model type
            #   test lenths  759.0, 60.0, 1517.9999999999998, 60.0, 1522.9999999999998, 50.0, 764.0

"""
from simulation.floquet_line_models.models.floquet_line import FloquetLine
from simulation.hfss_sims.hfss_line import hfss_touchstone_floquet_line
from simulation.hfss_sims.hfss_pre_sim_file_line import pre_sim_floquet_line
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

    er = float(super_conductor.get("Er"))
    height = nano_to_meters(float(super_conductor.get("Height")))
    thickness = nano_to_meters(float(super_conductor.get("Ts")))
    gt = microns_to_meters(float(super_conductor.get("Ground Thickness")))
    op_temp = float(super_conductor.get("Super Conductor Operation Temperature"))
    crit_temp = float(super_conductor.get("Super Conductor Critical Temperature"))
    ic = float(super_conductor.get("Super Conductor Critical Current"))
    pn = micro_ohms_cm_to_ohms_m(float(super_conductor.get("Super Conductor Normal Resistivity")))
    tan_d = float(super_conductor.get("Super Conductor Tangent Delta"))

    print(
        f"er:{er} height:{height} ts:{thickness} gt:{gt} op_temp:{op_temp} tc:{crit_temp} ic:{ic} pn:{pn} tan_d:{tan_d}")

    lengths_widths = [[microns_to_meters(float(length)), microns_to_meters(float(width))]
                      for length, width in line_dimensions.get("lengths_widths")]

    cpw_S = microns_to_meters(float(line_dimensions.get("S", 0)))

    n_repeated_cells = int(frequency_range.get("n_repeated_cells"))

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

            print([ [length, width ] for length, width in lengths_widths])
            unit_cell_line_segments = [
                MicroStripSC(width, length, thickness,height, er, tan_d, ic) for length, width in lengths_widths]

        elif model_type == CPW_TYPE:

            unit_cell_line_segments = [
                CoplanarWaveguideSC(width, length, cpw_S, thickness, er, tan_d, ic) for length, width in lengths_widths]

        elif model_type == ARTIFICIAL_CPW_TYPE:
            line_models = []
            raise NotImplementedError(
                "ARTIFICIAL_CPW waiting on Patricio's new model to implement")

        return FloquetLine(unit_cell_line_segments, super_conductivity_model, n_repeated_cells)
    elif model_type == "HFSS_TOUCHSTONE_FILE":

        # todo refacor this into hfss_touchstone_file_model_inputs
        hfss_touchstone_file_path = inputs.get("hfss_touchstone_file_path")
        n_interpt_points = inputs.get("n_interpt_points")
        unit_cell_length = inputs.get("unit_cell_length")
        n_repeated_cells = n_repeated_cells

        return hfss_touchstone_floquet_line(hfss_touchstone_file_path, n_interpt_points, unit_cell_length,
                                            n_repeated_cells), inputs

    elif model_type == "PRE_SIM_FILE":

        csv_data_list = line_model.csv_data

        floquet_line = pre_sim_floquet_line(csv_data_list, inputs.wl_microns, inputs.wu_microns,
                                            inputs.Lu_microns, inputs.dimensions, inputs.is_art_cpw_line,
                                            inputs.start_freq, inputs.end_freq, inputs.resolution,
                                            inputs.n_repeated_cells)

        return floquet_line, inputs
    else:
        raise NotImplementedError(
            f"\"{line_model.type}\" not implemented")
