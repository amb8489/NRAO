"""
this function makes a line model from the gui and returns a floquet line of the model type

"""
from simulation.floquet_line_models.models.hfss_line import hfss_touchstone_floquet_line
from simulation.floquet_line_models.models.floquet_line_art_cpw import SuperConductingFloquetLine_art
from simulation.floquet_line_models.models.floquet_line_ms_cpw import SuperConductingFloquetLine
from simulation.floquet_line_models.models.hfss_pre_sim_file_line import pre_sim_floquet_line
from simulation.inputs_containters.artificial_cpw_inputs import ArtificialCPWInputs
from simulation.inputs_containters.cpw_inputs import CPWInputs
from simulation.inputs_containters.hfss_touchstone_file_model_inputs import hfss_touchstone_file_model_inputs
from simulation.inputs_containters.micro_strip_inputs import MicroStripInputs
from simulation.inputs_containters.pre_sim_file_inputs import pre_sim_file_inputs
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.super_conducting_transmission_line_models.artificial_cpw.super_conducting_artificial_cpw_model import \
    SuperConductingArtificialCPWLine
from simulation.super_conducting_transmission_line_models.cpw.super_conducting_cpw_model import SuperConductingCPWLine
from simulation.super_conducting_transmission_line_models.micro_strip.super_conducting_micro_strip_model import \
    SuperConductingMicroStripModel
from simulation.utills.constants import CPW_TYPE, MICRO_STRIP_TYPE, ARTIFICIAL_CPW
from simulation.utills.functions import hertz_to_GHz


# todo refactor and document all

def floquet_line_from_line_model(line_model):
    GUI_json_inputs = line_model.get_inputs()

    print(GUI_json_inputs)

    # make super conductor

    model_type = line_model.type
    if model_type == MICRO_STRIP_TYPE:

        micro_strip_inputs = MicroStripInputs(GUI_json_inputs)

        # todo catch any errors and retur them if error

        super_conductivity_model = SuperConductivity(micro_strip_inputs.op_temp, micro_strip_inputs.crit_temp,
                                                     micro_strip_inputs.normal_resistivity)

        # todo is this taking in both width and unit_cell_length??
        central_line_model = SuperConductingMicroStripModel(micro_strip_inputs.height, micro_strip_inputs.central_line_width,
                                                            micro_strip_inputs.line_thickness, micro_strip_inputs.er,
                                                            micro_strip_inputs.tangent_delta,
                                                            micro_strip_inputs.crit_current)

        load_line_models = [

            # todo is this taking in accont  width and unit_cell_length val not just width??
            SuperConductingMicroStripModel(micro_strip_inputs.height, width, micro_strip_inputs.line_thickness, micro_strip_inputs.er,
                                           micro_strip_inputs.tangent_delta,
                                           micro_strip_inputs.crit_current) for width in micro_strip_inputs.load_widths]

        floquet_line = SuperConductingFloquetLine(micro_strip_inputs.unit_cell_length, micro_strip_inputs.D0, micro_strip_inputs.load_D_vals,
                                                  load_line_models, central_line_model, super_conductivity_model,
                                                  micro_strip_inputs.central_line_width, micro_strip_inputs.load_widths,
                                                  micro_strip_inputs.line_thickness, micro_strip_inputs.start_freq_GHz,
                                                  micro_strip_inputs.end_freq_GHz, micro_strip_inputs.resoultion)
        return floquet_line, micro_strip_inputs

    elif model_type == CPW_TYPE:
        CPW_inputs = CPWInputs(GUI_json_inputs)

        super_conductivity_model = SuperConductivity(CPW_inputs.op_temp, CPW_inputs.crit_temp,
                                                     CPW_inputs.normal_resistivity)

        # todo is this taking in both width and unit_cell_length??
        # todo where is width being used
        # todo combine this into one
        central_line_model = SuperConductingCPWLine(CPW_inputs.central_line_width, CPW_inputs.ground_spacing,
                                                    CPW_inputs.line_thickness, CPW_inputs.er, CPW_inputs.tangent_delta,
                                                    CPW_inputs.crit_current)
        load_line_models = [
            SuperConductingCPWLine(load_width, CPW_inputs.ground_spacing, CPW_inputs.line_thickness, CPW_inputs.er,
                                   CPW_inputs.tangent_delta, CPW_inputs.crit_current) for load_width in
            CPW_inputs.load_widths]

        floquet_line = SuperConductingFloquetLine(CPW_inputs.unit_cell_length, CPW_inputs.D0, CPW_inputs.load_D_vals,
                                                  load_line_models, central_line_model, super_conductivity_model,
                                                  CPW_inputs.central_line_width, CPW_inputs.load_widths,
                                                  CPW_inputs.line_thickness, CPW_inputs.start_freq_GHz,
                                                  CPW_inputs.end_freq_GHz, CPW_inputs.resoultion)
        return floquet_line, CPW_inputs
    elif model_type == ARTIFICIAL_CPW:

        art_cpw_inputs = ArtificialCPWInputs(GUI_json_inputs)

        super_conductivity_model = SuperConductivity(art_cpw_inputs.op_temp, art_cpw_inputs.crit_temp,
                                                     art_cpw_inputs.normal_resistivity)

        line_models = []
        for line_len, S, WH, LH, WL, LL in art_cpw_inputs.line_dimensions:
            nfs = line_len // (LH + (2 * S) + LL)
            line_models.append(
                SuperConductingArtificialCPWLine(LH, WH, LL, WL, S, nfs, art_cpw_inputs.er, art_cpw_inputs.line_thickness,
                                                 art_cpw_inputs.height, super_conductivity_model, line_len))
        floquet_line = SuperConductingFloquetLine_art(line_models, super_conductivity_model, art_cpw_inputs.line_thickness,
                                                      art_cpw_inputs.start_freq_GHz, art_cpw_inputs.end_freq_GHz,
                                                      art_cpw_inputs.resoultion)
        return floquet_line, art_cpw_inputs


    elif model_type == "HFSS_TOUCHSTONE_FILE":


        hfss_s_inputs = hfss_touchstone_file_model_inputs(GUI_json_inputs)

        #todo refacor this into hfss_touchstone_file_model_inputs
        hfss_touchstone_file_path = GUI_json_inputs.get("hfss_touchstone_file_path")
        n_interpt_points = GUI_json_inputs.get("n_interpt_points")
        unit_cell_length = GUI_json_inputs.get("unit_cell_length")
        n_repeated_cells = GUI_json_inputs.get("n_repeated_cells")

        return hfss_touchstone_floquet_line(hfss_touchstone_file_path, n_interpt_points, unit_cell_length,
                                            n_repeated_cells), hfss_s_inputs

    #todo rename to pre sim file
    elif model_type == "SIM_FILE":



        pre_sim_inputs = pre_sim_file_inputs(GUI_json_inputs)

        csv_data_list = line_model.csv_data

        floquet_line = pre_sim_floquet_line(csv_data_list, pre_sim_inputs.wl_microns, pre_sim_inputs.wu_microns,
                                            pre_sim_inputs.Lu_microns, pre_sim_inputs.dimensions, pre_sim_inputs.is_art_cpw_line,
                                            pre_sim_inputs.start_freq, pre_sim_inputs.end_freq, pre_sim_inputs.resolution,
                                            pre_sim_inputs.n_repeated_cells)

        return floquet_line, pre_sim_inputs


    else:
        raise NotImplementedError(
            f"\"{line_model.type}\" not implemented need to go into Floquet_line_builder.py and Implement")
