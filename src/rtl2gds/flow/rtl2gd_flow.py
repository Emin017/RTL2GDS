import logging
import os
import time

from rtl2gds import global_configs as configs
from rtl2gds import step
from rtl2gds.chip import Chip


def run(chip: Chip):

    start_time = time.perf_counter()

    step_name = "synthesis"
    chip.init_for_step(step_name)
    logging.info("(step.%s) synthesis by yosys", step_name)
    synth_constrain = step.synthesis.run(
        design_top=chip.design_top,
        design_path=chip.path_setting,
        design_constrain=chip.constrain,
    )
    chip.constrain = synth_constrain

    step_name = "floorplan"
    chip.init_for_step(step_name)
    output_def = f"{chip.path_setting.result_dir}/{chip.design_top}_{step_name}.def"
    chip.path_setting.def_file = output_def
    logging.info("(step.%s) floorplan by iEDA-iFP", step_name)
    step.floorplan.run(
        design_top=chip.design_top,
        design_path=chip.path_setting,
        design_constrain=chip.constrain,
    )

    os.makedirs(f"{chip.path_setting.result_dir}/feature", exist_ok=True)

    # p&r flow
    for step_name, step_obj in step.pr_step_map.items():
        assert step_obj.name == step_name

        chip.init_for_step(step_name)
        output_def = f"{chip.path_setting.result_dir}/{chip.design_top}_{step_name}.def"

        step_obj.run(
            design_top=chip.design_top,
            input_def=chip.path_setting.def_file,
            result_dir=chip.path_setting.result_dir,
            output_def=output_def,
            clk_port_name=chip.constrain.clk_port_name,
            clk_freq_mhz=chip.constrain.clk_freq_mhz,
        )

        chip.path_setting.def_file = output_def

        if step_name in ["place", "cts", "legalize", "route", "filler"]:
            step.dump_layout_gds.run(
                input_def=chip.path_setting.def_file,
                gds_file=chip.path_setting.gds_file,
                result_dir=chip.path_setting.result_dir,
                snapshot_file=f"{chip.path_setting.result_dir}/{chip.design_top}_{step_name}.png",
            )

    end_time = time.perf_counter()
    logging.info("Total elapsed time: %.2f seconds", end_time - start_time)
