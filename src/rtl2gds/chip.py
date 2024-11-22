from pathlib import Path
from typing import Dict, Optional

import yaml

import rtl2gds.global_configs as configs

from .design_constrain import DesignConstrain
from .design_path import DesignPath
from .metrics import DesignMetrics


class Chip:
    """
    Main design object that manages chip design flow from RTL to GDS.

    This class centralizes all design information and provides interfaces
    for running design flow steps like synthesis, floorplanning, etc.
    """

    def __init__(
        self,
        design_top: str = "",
        path_setting: Optional[DesignPath] = None,
        constrain: Optional[DesignConstrain] = None,
    ):
        self.design_top = design_top
        self.path_setting = path_setting
        self.constrain = constrain
        self.metrics = DesignMetrics()
        self.finished_step = configs.INIT_STEP
        self.expect_step = configs.INIT_STEP

    def init_for_step(self, expect_step: str):
        self.finished_step = self.expect_step
        self.expect_step = expect_step

    @classmethod
    def from_yaml(cls, config_path: Path) -> "Chip":
        """Create a Chip instance from YAML configuration"""
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Parse RTL files
        rtl_files = config["RTL_FILE"]
        # rtl_files = (
        #     config["RTL_FILE"]
        #     if isinstance(config["RTL_FILE"], list)
        #     else [
        #         p for pattern in config["RTL_FILE"].split() for p in glob.glob(pattern)
        #     ]
        # )

        # Create path settings and constraints
        path_setting = DesignPath(
            rtl_file=rtl_files,
            netlist_file=config["NETLIST_FILE"],
            def_file=config.get("DEF_FILE", ""),
            gds_file=config["GDS_FILE"],
            result_dir=config["RESULT_DIR"],
            sdc_file=config.get("SDC_FILE", configs.DEFAULT_SDC_FILE),
        )

        constrain = DesignConstrain(
            clk_port_name=config["CLK_PORT_NAME"],
            clk_freq_mhz=config["CLK_FREQ_MHZ"],
            die_area=config.get("DIE_AREA", ""),
            core_area=config.get("CORE_AREA", ""),
            core_util=config.get("CORE_UTIL", 0),
        )

        return cls(
            design_top=config["DESIGN_TOP"],
            path_setting=path_setting,
            constrain=constrain,
        )

    @property
    def env(self) -> Dict[str, str]:
        """Get environment variables for running tools"""
        env = configs.ENV_TOOLS_PATH.copy()
        env.update(self.path_setting.to_env_dict())
        env.update(self.constrain.to_env_dict())
        env["DESIGN_TOP"] = self.design_top
        return env
