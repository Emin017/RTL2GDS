import os
import pathlib
from typing import Dict

import yaml

from . import global_configs
from .design_constrain import DesignConstrain
from .design_path import DesignPath


class Chip:
    """
    Main design object that manages chip design flow from RTL to GDS.

    This class centralizes all design information and provides interfaces
    for running design flow steps like synthesis, floorplanning, etc.
    """

    def __init__(
        self,
        config_yaml: str,
    ):
        self.design_top = None
        self.path_setting: DesignPath = None
        self.constrain: DesignConstrain = None
        # self.metrics: DesignMetrics = None
        self.finished_step = None
        self.config_yaml = config_yaml
        # self._io_env = {}
        self.init_from_yaml(config_yaml)

    def init_from_yaml(self, config_path: str):
        """Init a Chip instance from YAML configuration"""
        if not os.path.exists(config_path):
            pathlib.Path(config_path).touch()
        self.config_yaml = config_path
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        self.init_from_config(config)

    def init_from_config(self, config: Dict):
        """Init a Chip instance from a config dictionary"""
        if not os.path.exists(self.config_yaml):
            pathlib.Path(self.config_yaml).touch()
        self.finished_step = (
            config["FINISHED_STEP"]
            if "FINISHED_STEP" in config
            else global_configs.StepName.INIT
        )
        self.design_top = config["DESIGN_TOP"]
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
            sdc_file=config.get("SDC_FILE", global_configs.DEFAULT_SDC_FILE),
        )

        constrain = DesignConstrain(
            clk_port_name=config["CLK_PORT_NAME"],
            clk_freq_mhz=config["CLK_FREQ_MHZ"],
            die_area=config.get("DIE_AREA", ""),
            core_area=config.get("CORE_AREA", ""),
            core_util=config.get("CORE_UTIL", 0),
        )

        self.path_setting = path_setting
        self.constrain = constrain

    def env(self) -> Dict[str, str]:
        """Get environment variables for running tools"""
        io_env = global_configs.ENV_TOOLS_PATH.copy()
        io_env.update(self.path_setting.to_env_dict())
        io_env.update(self.constrain.to_env_dict())
        io_env["DESIGN_TOP"] = self.design_top
        io_env["FINISHED_STEP"] = self.finished_step
        return io_env

    def dump_config(self):
        """Dump the config to the yaml file"""
        with open(self.config_yaml, "w", encoding="utf-8") as f:
            yaml.dump(self.env(), f)
