"""
this function makes a line model from the gui and returns a floquet line of the model type

"""
from simulation.floquet_line_models.models.HFSS_line import hfss_touchstone_file_model
from simulation.floquet_line_models.models.floquet_line_ARTIFICAL import SuperConductingFloquetLine_art
from simulation.floquet_line_models.models.floquet_line_MS_CPW import SuperConductingFloquetLine
from simulation.floquet_line_models.models.hfss_pre_sim_file_line import pre_sim_floquet_line
from simulation.model_inputs.artificial_cpw_inputs import ArtificialCPWInputs
from simulation.model_inputs.cpw_inputs import CPWInputs
from simulation.model_inputs.hfss_touchstone_file_model_inputs import hfss_touchstone_file_model_inputs
from simulation.model_inputs.micro_strip_inputs import MicroStripInputs
from simulation.model_inputs.pre_sim_file_inputs import pre_sim_file_inputs
from simulation.super_conductor_model.super_conductor_model import SuperConductivity
from simulation.transmission_line_models.artificial_cpw.super_conducting_artificial_cpw_model import \
    SuperConductingArtificialCPWLine
from simulation.transmission_line_models.cpw.super_conducting_cpw_model import SuperConductingCPWLine
from simulation.transmission_line_models.micro_strip.super_conducting_micro_strip_model import \
    SuperConductingMicroStripModel
from simulation.utills.constants import CPW_TYPE, MICRO_STRIP_TYPE, ARTIFICIAL_CPW
from simulation.utills.functions import hertz_to_GHz


# todo refactor and document all

def floquet_line_builder(line_model):
    GUI_json_inputs = line_model.get_inputs()

    print(GUI_json_inputs)

    # make super conductor

    model_type = line_model.type
    if model_type == MICRO_STRIP_TYPE:

        GUI_inputs = MicroStripInputs(GUI_json_inputs)

        # todo catch any errors and retur them if error

        super_conductivity_model = SuperConductivity(GUI_inputs.op_temp, GUI_inputs.crit_temp,
                                                     GUI_inputs.normal_resistivity)

        # todo is this taking in both width and unit_cell_length??
        central_line_model = SuperConductingMicroStripModel(GUI_inputs.height, GUI_inputs.central_line_width,
                                                            GUI_inputs.line_thickness, GUI_inputs.er,
                                                            GUI_inputs.tangent_delta,
                                                            GUI_inputs.crit_current)

        load_line_models = [

            # todo is this taking in accont  width and unit_cell_length val not just width??
            SuperConductingMicroStripModel(GUI_inputs.height, width, GUI_inputs.line_thickness, GUI_inputs.er,
                                           GUI_inputs.tangent_delta,
                                           GUI_inputs.crit_current) for width in GUI_inputs.load_widths]

        floquet_line = SuperConductingFloquetLine(GUI_inputs.unit_cell_length, GUI_inputs.D0, GUI_inputs.load_D_vals,
                                                  load_line_models, central_line_model, super_conductivity_model,
                                                  GUI_inputs.central_line_width, GUI_inputs.load_widths,
                                                  GUI_inputs.line_thickness, GUI_inputs.start_freq_GHz,
                                                  GUI_inputs.end_freq_GHz, GUI_inputs.resoultion)
        return floquet_line, GUI_inputs

    elif model_type == CPW_TYPE:
        GUI_inputs = CPWInputs(GUI_json_inputs)

        super_conductivity_model = SuperConductivity(GUI_inputs.op_temp, GUI_inputs.crit_temp,
                                                     GUI_inputs.normal_resistivity)

        # todo is this taking in both width and unit_cell_length??
        # todo where is width being used
        # todo combine this into one
        central_line_model = SuperConductingCPWLine(GUI_inputs.central_line_width, GUI_inputs.ground_spacing,
                                                    GUI_inputs.line_thickness, GUI_inputs.er, GUI_inputs.tangent_delta,
                                                    GUI_inputs.crit_current)
        load_line_models = [
            SuperConductingCPWLine(load_width, GUI_inputs.ground_spacing, GUI_inputs.line_thickness, GUI_inputs.er,
                                   GUI_inputs.tangent_delta, GUI_inputs.crit_current) for load_width in
            GUI_inputs.load_widths]

        floquet_line = SuperConductingFloquetLine(GUI_inputs.unit_cell_length, GUI_inputs.D0, GUI_inputs.load_D_vals,
                                                  load_line_models, central_line_model, super_conductivity_model,
                                                  GUI_inputs.central_line_width, GUI_inputs.load_widths,
                                                  GUI_inputs.line_thickness, GUI_inputs.start_freq_GHz,
                                                  GUI_inputs.end_freq_GHz, GUI_inputs.resoultion)
        return floquet_line, GUI_inputs
    elif model_type == ARTIFICIAL_CPW:

        GUI_inputs = ArtificialCPWInputs(GUI_json_inputs)

        super_conductivity_model = SuperConductivity(GUI_inputs.op_temp, GUI_inputs.crit_temp,
                                                     GUI_inputs.normal_resistivity)

        line_models = []
        for line_len, S, WH, LH, WL, LL in GUI_inputs.line_dimensions:
            nfs = line_len // (LH + (2 * S) + LL)
            line_models.append(
                SuperConductingArtificialCPWLine(LH, WH, LL, WL, S, nfs, GUI_inputs.er, GUI_inputs.line_thickness,
                                                 GUI_inputs.height, super_conductivity_model, line_len))
        floquet_line = SuperConductingFloquetLine_art(line_models, super_conductivity_model, GUI_inputs.line_thickness,
                                                      GUI_inputs.start_freq_GHz, GUI_inputs.end_freq_GHz,
                                                      GUI_inputs.resoultion)
        return floquet_line, GUI_inputs


    elif model_type == "HFSS_TOUCHSTONE_FILE":

        GUI_inputs = hfss_touchstone_file_model_inputs(GUI_json_inputs)

        hfss_touchstone_file_path = GUI_json_inputs.get("hfss_touchstone_file_path")
        n_interpt_points = GUI_json_inputs.get("n_interpt_points")
        unit_cell_length = GUI_json_inputs.get("unit_cell_length")
        n_repeated_cells = GUI_json_inputs.get("n_repeated_cells")

        return hfss_touchstone_file_model(hfss_touchstone_file_path, n_interpt_points, unit_cell_length,
                                          n_repeated_cells), GUI_inputs


    elif model_type == "SIM_FILE":



        GUI_inputs = pre_sim_file_inputs(GUI_json_inputs)

        csv_data_list = line_model.csv_data

        floquet_line = pre_sim_floquet_line(csv_data_list, GUI_inputs.wl_microns, GUI_inputs.wu_microns,
                                            GUI_inputs.Lu_microns, GUI_inputs.dimensions, GUI_inputs.is_art_cpw_line,
                                            GUI_inputs.start_freq, GUI_inputs.end_freq, GUI_inputs.resolution,
                                            GUI_inputs.n_repeated_cells)

        return floquet_line, GUI_inputs


    else:
        raise NotImplementedError(
            f"\"{line_model.type}\" not implemented need to go into Floquet_line_builder.py and Implement")
