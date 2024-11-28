import logging
import os
import shutil
import time

from ..chip import Chip
from ..global_configs import StepName
from .. import step
from .step_runner import StepRunner

def run(chip: Chip):
    start_time = time.perf_counter()
    runner = StepRunner(chip)

    # Run synthesis
    runner.run_synthesis()

    # Run floorplan
    runner.run_floorplan()
    runner.run_dump_layout_gds(step_name=StepName.FLOORPLAN)

    # Run P&R flow
    for step_name in step.pr_step_map:
        runner.run_pr_step(step_name)
        if step_name in [StepName.PLACE, StepName.CTS, StepName.LEGALIZE, StepName.ROUTE, StepName.FILLER]:
            runner.run_dump_layout_gds(step_name, take_snapshot=True)

    # Copy final GDS
    final_gds_file = f"{chip.path_setting.result_dir}/{chip.design_top}_filler.gds"
    assert os.path.exists(final_gds_file)
    shutil.copy(final_gds_file, chip.path_setting.gds_file)

    end_time = time.perf_counter()
    logging.info("Total elapsed time: %.2f seconds", end_time - start_time)
