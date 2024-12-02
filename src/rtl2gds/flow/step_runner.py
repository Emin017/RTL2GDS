import os
from pathlib import Path
from typing import Dict, Optional

import yaml

from .. import step
from ..chip import Chip
from ..global_configs import RTL2GDS_FLOW_STEP, StepName


def get_expected_step(finished_step: str) -> Optional[str]:
    """Get the expected step for the rtl2gds flow"""
    if finished_step == RTL2GDS_FLOW_STEP[-1]:
        return None
    return RTL2GDS_FLOW_STEP[RTL2GDS_FLOW_STEP.index(finished_step) + 1]


class StepRunner:
    """return step metrics file"""

    def __init__(self, chip: Chip):
        self.chip = chip

    def _check_expected_step(self, step_name: str):
        expected_step = get_expected_step(self.chip.finished_step)
        if expected_step != step_name:
            raise ValueError(f"Expected step: {expected_step}, but got: {step_name}")

    def run_step(self, step_name: str):
        self._check_expected_step(step_name)

        if step_name == step.synthesis.STEP_NAME:
            self.run_synthesis()
        elif step_name == step.floorplan.STEP_NAME:
            self.run_floorplan()
        else:
            self.run_pr_step(step_name)

    def run_synthesis(self):
        """Run synthesis step"""
        step_name = StepName.SYNTHESIS
        self._check_expected_step(step_name)

        results = step.synthesis.run(
            design_top=self.chip.design_top,
            rtl_file=self.chip.path_setting.rtl_file,
            netlist_file=self.chip.path_setting.netlist_file,
            sdc_file=self.chip.path_setting.sdc_file,
            result_dir=self.chip.path_setting.result_dir,
            clk_port_name=self.chip.constrain.clk_port_name,
            clk_freq_mhz=self.chip.constrain.clk_freq_mhz,
            die_area=self.chip.constrain.die_area,
            core_area=self.chip.constrain.core_area,
            core_util=self.chip.constrain.core_util,
        )

        self.chip.constrain.die_area = results["DIE_AREA"]
        self.chip.constrain.core_area = results["CORE_AREA"]
        self.chip.constrain.core_util = results["CORE_UTIL"]
        self.chip.finished_step = step_name
        return list([f"{self.chip.path_setting.result_dir}/yosys/synth_stat.txt"])

    def run_floorplan(self):
        """Run floorplan step"""
        step_name = StepName.FLOORPLAN
        self._check_expected_step(step_name)
        # Create feature directory (iEDA issue workaround)
        os.makedirs(f"{self.chip.path_setting.result_dir}/feature", exist_ok=True)

        output_def = f"{self.chip.path_setting.result_dir}/{self.chip.design_top}_{step_name}.def"
        self.chip.path_setting.def_file = output_def

        results = step.floorplan.run(
            design_top=self.chip.design_top,
            result_dir=self.chip.path_setting.result_dir,
            sdc_file=self.chip.path_setting.sdc_file,
            input_netlist=self.chip.path_setting.netlist_file,
            output_def=self.chip.path_setting.def_file,
            die_area=self.chip.constrain.die_area,
            core_area=self.chip.constrain.core_area,
        )

        self.chip.constrain.die_area = results["DIE_AREA"]
        self.chip.constrain.core_area = results["CORE_AREA"]
        self.chip.constrain.core_util = results["CORE_UTIL"]
        self.chip.finished_step = step_name
        return list(
            [f"{self.chip.path_setting.result_dir}/feature/summary_floorplan.json"]
        )

    def run_pr_step(self, step_name: str):
        """Run a specific place & route step"""
        self._check_expected_step(step_name)

        step_obj = step.pr_step_map.get(step_name)
        if not step_obj:
            raise ValueError(f"Unknown PR step: {step_name}")

        step_file_prefix = (
            f"{self.chip.path_setting.result_dir}/{self.chip.design_top}_{step_name}"
        )
        output_def = f"{step_file_prefix}.def"
        # Create feature directory (iEDA issue workaround)
        os.makedirs(f"{self.chip.path_setting.result_dir}/feature", exist_ok=True)

        step_obj.run(
            design_top=self.chip.design_top,
            input_def=self.chip.path_setting.def_file,
            result_dir=self.chip.path_setting.result_dir,
            output_def=output_def,
            clk_port_name=self.chip.constrain.clk_port_name,
            clk_freq_mhz=self.chip.constrain.clk_freq_mhz,
        )

        self.chip.path_setting.def_file = output_def
        self.chip.finished_step = step_name
        return list(
            [f"{self.chip.path_setting.result_dir}/feature/{step_obj.tmp_feature_json}"]
        )

    def run_dump_layout_gds(self, step_name: str, take_snapshot: bool = False):
        """Run dump layout GDS step"""
        step.dump_layout_gds.run(
            input_def=self.chip.path_setting.def_file,
            gds_file=f"{self.chip.path_setting.result_dir}/{self.chip.design_top}_{step_name}.gds",
            result_dir=self.chip.path_setting.result_dir,
            snapshot_file=(
                f"{self.chip.path_setting.result_dir}/{self.chip.design_top}_{step_name}.png"
                if take_snapshot
                else None
            ),
        )
