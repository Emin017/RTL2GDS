from .. import step
from ..chip import Chip
from ..global_configs import StepName
from . import rtl2gds_flow
from .step_runner import StepRunner


def run(chip: Chip, expect_step: str = StepName.RTL2GDS_ALL):

    dump_json = False
    result_files = []
    if expect_step == StepName.RTL2GDS_ALL:
        rtl2gds_flow.run(chip)
        dump_json = True
    else:
        runner = StepRunner(chip)

        if expect_step == StepName.SYNTHESIS:
            result_files = runner.run_synthesis()
        elif expect_step == StepName.FLOORPLAN:
            result_files = runner.run_floorplan()
            # runner.run_dump_layout_gds(step_name=expect_step, take_snapshot=True)
            dump_json = True
        else:
            result_files = runner.run_pr_step(expect_step)
            if expect_step == StepName.LEGALIZE:
                result_files.append(
                    f"{chip.path_setting.result_dir}/feature/rt/legalization_egr_union_overflow.csv"
                )
            if expect_step in [
                StepName.PLACE,
                StepName.CTS,
                StepName.LEGALIZE,
                StepName.ROUTE,
                StepName.FILLER,
            ]:
                # runner.run_dump_layout_gds(step_name=expect_step, take_snapshot=True)
                dump_json = True

    # Dump and return json files
    if dump_json:
        json_files = step.dump_layout_json.run(
            input_def=chip.path_setting.def_file,
            result_dir=chip.path_setting.result_dir,
            layout_json_file=f"{chip.path_setting.result_dir}/{chip.design_top}_{chip.finished_step}.json",
        )
        result_files.extend(json_files)

    return result_files
