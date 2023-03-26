"""
this function makes a line model from the gui and returns a floquet line of the model type
            #   test lenths  [0.000759, 6e-05, 0.0015179999999999998, 6e-05, 0.0015229999999999998, 5e-05, 0.000764]

"""
from simulation.floquet_line_models.models.floquet_line import FloquetLine
from simulation.hfss_sims.hfss_line import hfss_touchstone_floquet_line
from simulation.hfss_sims.hfss_pre_sim_file_line import pre_sim_floquet_line
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.super_conducting_transmission_line_models.cpw.super_conducting_cpw_model import CoplanarWaveguideSC
from simulation.super_conducting_transmission_line_models.micro_strip.super_conducting_micro_strip_model import \
    MicroStripSC
from simulation.utills.constants import CPW_TYPE, MICRO_STRIP_TYPE, ARTIFICIAL_CPW_TYPE


def floquet_line_from_line_model(line_model):
    inputs = line_model.get_inputs()

    super_conductor = inputs.get("super_conductor_properties", {})
    line_dimensions = inputs.get("line_dimensions", {})
    frequency_range = inputs.get("frequency_range", {})
    gain_properties = inputs.get("gain_properties", {})
    lu_dimensions = inputs.get("lu_dimensions", {})

    er = super_conductor.get("Er")
    height = super_conductor.get("Height")
    ts = super_conductor.get("Ts")
    gt = super_conductor.get("Ground Thickness")
    op_temp = super_conductor.get("Super Conductor Operation Temperature")
    tc = super_conductor.get("Super Conductor Critical Temperature")
    ic = super_conductor.get("Super Conductor Critical Current")
    pn = super_conductor.get("Super Conductor Normal Resistivity")
    tan_d = super_conductor.get("Super Conductor Tangent Delta")

    print(f"er:{er} height:{height} ts:{ts} gt:{gt} op_temp:{op_temp} tc:{tc} ic:{ic} pn:{pn} tan_d:{tan_d}")

    lengths_widths = line_dimensions.get("lengths_widths")
    cpw_S = line_dimensions.get("S")

    print(f"lengths_widths:{lengths_widths} cpw_S:{cpw_S}")

    lu_S = lu_dimensions.get("lu_S")
    lu_WH = lu_dimensions.get("lu_WH")
    lu_LH = lu_dimensions.get("lu_LH")
    lu_LL = lu_dimensions.get("lu_LL")

    print(f"lu_S:{lu_S} lu_WH:{lu_WH} lu_LH:{lu_LH} lu_LL:{lu_LL}")




    start_frequency = frequency_range.get("Start Frequency")
    end_frequency = frequency_range.get("End Frequency")
    resolution = frequency_range.get("Resolution")
    n_repeated_cells = frequency_range.get("n_repeated_cells")

    print(f"start_frequency:{start_frequency} end_frequency:{end_frequency} resolution:{resolution} n_repeated_cells:{n_repeated_cells}")


    should_calc_gain = bool(int(gain_properties.get('calc_gain')))
    s_amp_0 = gain_properties.get('Signal Amplitude')
    i_amp_0 = gain_properties.get('Idler Amplitude')
    p_amp_0 = gain_properties.get('Pump Amplitude')
    pump_freq = gain_properties.get('Pump Frequency')
    print(f"should_calc_gain:{should_calc_gain} s_amp_0:{s_amp_0} i_amp_0:{i_amp_0} p_amp_0:{p_amp_0} pump_freq:{pump_freq}")

    exit(1)

    model_type = line_model.type

    print(model_type, inputs)

    # fix and simplify gui

    # simulated by mathematical model
    if model_type in [MICRO_STRIP_TYPE, CPW_TYPE, ARTIFICIAL_CPW_TYPE]:

        super_conductivity_model = SuperConductivity(inputs.op_temp, inputs.crit_temp, inputs.normal_resistivity)

        unit_cell_line_segments = []
        if model_type == MICRO_STRIP_TYPE:

            unit_cell_line_segments = [

                MicroStripSC(width, length, inputs.height, inputs.thickness,
                             inputs.er, inputs.tangent_delta, inputs.crit_current)

                for length, width in inputs.lens_widths]

        elif model_type == CPW_TYPE:

            # todo SC_CoplanarWaveguide and SC_MicroStrip need to checked
            unit_cell_line_segments = [
                CoplanarWaveguideSC(width, length, inputs.ground_spacing, inputs.line_thickness,
                                    inputs.er, inputs.tangent_delta, inputs.crit_current)

                for length, width in inputs.lens_widths]

        elif model_type == ARTIFICIAL_CPW_TYPE:

            # todo refactor art cpw to be calculated by number of Lu segments
            # waiting on Patrico's new model to implement

            # have user define the Lu dimensions -- then the floquet lens by #lu's for each line
            # calcuate line lenght in SuperConductingArtificialCPWLine

            line_models = []

            raise NotImplementedError(
                "ARTIFICIAL_CPW waiting on Patricio's new model to implement")

        return FloquetLine(unit_cell_line_segments, super_conductivity_model, inputs.get("n_repeated_unit_cells"))
    elif model_type == "HFSS_TOUCHSTONE_FILE":

        # todo refacor this into hfss_touchstone_file_model_inputs
        hfss_touchstone_file_path = inputs.get("hfss_touchstone_file_path")
        n_interpt_points = inputs.get("n_interpt_points")
        unit_cell_length = inputs.get("unit_cell_length")
        n_repeated_cells = inputs.get("n_repeated_cells")

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
