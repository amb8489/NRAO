from floquet_line_model.floquet_line import SuperConductingFloquetLine
from model_inputs.cpw_inputs import CPWInputs
from model_inputs.micro_strip_inputs import MicroStripInputs
from super_conductor_model.super_conductor_model import SuperConductivity
from transmission_line_models.cpw.super_conducting_cpw_model import SuperConductingCPWLine
from transmission_line_models.micro_strip.super_conducting_micro_strip_model import SuperConductingMicroStripModel
from utills.constants import MICRO_STRIP_TYPE, CPW_TYPE

"""
this function makes a line model from the gui and returns a floquet line of the model type

"""


# todo refactor and document all

def floquet_line_builder(line_model):
    json_inputs = line_model.get_inputs()

    # make super conductor

    model_type = line_model.type
    if model_type == MICRO_STRIP_TYPE:

        inputs = MicroStripInputs(json_inputs)

        # todo catch any errors and retur them if error

        super_conductivity_model = SuperConductivity(inputs.op_temp, inputs.crit_temp, inputs.normal_resistivity)

        # todo is this taking in both width and D??
        central_line_model = SuperConductingMicroStripModel(inputs.height, inputs.central_line_width,
                                                            inputs.line_thickness, inputs.er, inputs.tangent_delta,
                                                            inputs.crit_current)

        load_line_models = [

            # todo is this taking in accont  width and D val not just width??
            SuperConductingMicroStripModel(inputs.height, width, inputs.line_thickness, inputs.er,
                                           inputs.tangent_delta,
                                           inputs.crit_current) for width in inputs.load_widths]

        floquet_line = SuperConductingFloquetLine(inputs.unit_cell_length, inputs.D0, inputs.load_D_vals,
                                                  load_line_models, central_line_model, super_conductivity_model,
                                                  inputs.central_line_width, inputs.load_widths, inputs.line_thickness,
                                                  inputs.crit_current)
        return floquet_line

    elif model_type == CPW_TYPE:
        inputs = CPWInputs(json_inputs)

        super_conductivity_model = SuperConductivity(inputs.op_temp, inputs.crit_temp, inputs.normal_resistivity)

        # todo is this taking in both width and D??
        # todo where is width being used

        central_line_model = SuperConductingCPWLine(inputs.central_line_width, inputs.ground_spacing,
                                                    inputs.line_thickness, inputs.er, inputs.tangent_delta)
        load_line_models = [SuperConductingCPWLine(load_width, inputs.ground_spacing, inputs.line_thickness, inputs.er,
                                                   inputs.tangent_delta) for load_width in inputs.load_widths]

        floquet_line = SuperConductingFloquetLine(inputs.unit_cell_length, inputs.D0, inputs.load_D_vals,
                                                  load_line_models, central_line_model, super_conductivity_model,
                                                  inputs.central_line_width, inputs.load_widths, inputs.line_thickness,
                                                  inputs.crit_current)
        return floquet_line

    else:
        raise NotImplementedError(f"\"{line_model.type}\" not implemented")
