import logging
import os
import time

from ..chip import Chip
from ..global_configs import PR_FLOW_STEPS, StepName
from .step_wrapper import StepWrapper


def run(chip: Chip):
    start_time = time.perf_counter()
    runner = StepWrapper(chip)

    # Run synthesis
    runner.run_synthesis()

    # Run floorplan
    runner.run_floorplan()
    runner.run_save_layout_gds(step_name=StepName.FLOORPLAN)

    # Run P&R flow
    for step_name in PR_FLOW_STEPS:
        runner.run_pr_step(step_name)
        if step_name in [StepName.PLACEMENT, StepName.FILLER]:
            runner.run_save_layout_gds(step_name=step_name, take_snapshot=True)

    assert chip.finished_step == StepName.FILLER
    assert os.path.exists(chip.path_setting.gds_file)

    end_time = time.perf_counter()
    logging.info("Total elapsed time: %.2f seconds", end_time - start_time)
