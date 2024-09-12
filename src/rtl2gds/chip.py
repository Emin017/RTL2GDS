import os
import yaml
from dataclasses import dataclass

from .design_constrain import DesignConstrain
from . import configs


# would it be better if use pydantic as a validation layer
@dataclass
class ProjectPath:
    rtl_file: str
    netlist_file: str
    # sdc_file = f"${Configs.PKG_TOOL_DIR}/default.sdc"
    def_file = ""
    gds_file: str
    # json_file: str
    result_dir: str


class Chip:
    def __init__(self):
        self.design_top: str
        self.step: str
        self.path_setting: ProjectPath
        self.constrain: DesignConstrain
        self.io_env: dict[str:str]

    def load_config(self, config_file: str):
        with open(config_file, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f)

        print(user_config)
        self.io_env = dict(user_config | configs.ENV_TOOLS_PATH)
        self.design_top = user_config["DESIGN_TOP"]
        self.step = "init"
        self.path_setting = ProjectPath(
            rtl_file=user_config["RTL_FILE"],
            netlist_file=user_config["NETLIST_FILE"],
            gds_file=user_config["GDS_FILE"],
            result_dir=user_config["RESULT_DIR"],
            # def_file = user_config[''],
            # json_file = user_config[''],
        )
        self.constrain = DesignConstrain(
            clk_port_name=user_config["CLK_PORT_NAME"],
            clk_freq_mhz=user_config["CLK_FREQ_MHZ"],
            die_area=user_config["DIE_AREA"],
            core_area=user_config["CORE_AREA"],
        )

        os.makedirs(self.path_setting.result_dir + "/yosys/", exist_ok=True)
