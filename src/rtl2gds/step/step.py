"""
description: behavior of each RTL2GDS step
"""

import logging
import os
import subprocess

from ..global_configs import DEFAULT_SDC_FILE, ENV_TOOLS_PATH, StepName
from . import configs


class Step:
    def __init__(self):
        self.name: str
        self.description: str
        self.shell_cmd: list
        self.tmp_feature_json: str

    def run(
        self,
        design_top: str,
        input_def: str,
        result_dir: str,
        output_def: str,
        clk_port_name: str,
        clk_freq_mhz: float,
    ):
        logging.info("(step.%s) %s", self.name, self.description)
        assert os.path.exists(input_def)

        io_env = {
            "DESIGN_TOP": design_top,
            "INPUT_DEF": input_def,
            "OUTPUT_DEF": output_def,
            "RESULT_DIR": result_dir,
            "SDC_FILE": DEFAULT_SDC_FILE,
            "CLK_PORT_NAME": clk_port_name,
            "CLK_FREQ_MHZ": str(clk_freq_mhz),
        }
        io_env.update(ENV_TOOLS_PATH)

        ret_code = subprocess.call(self.shell_cmd, env=io_env)
        if ret_code != 0:
            raise subprocess.CalledProcessError(ret_code, self.shell_cmd)

        assert os.path.exists(output_def)


class FixFanout(Step):
    def __init__(self):
        super().__init__()
        self.name = StepName.FIXFANOUT
        self.description = "Fixing fanout by iEDA-iNO"
        self.shell_cmd = configs.SHELL_CMD[self.name]
        self.tmp_feature_json = "ino_opt.json"


class Place(Step):
    def __init__(self):
        super().__init__()
        self.name = StepName.PLACE
        self.description = "Standard Cell Placement by iEDA-iPL"
        self.shell_cmd = configs.SHELL_CMD[self.name]
        self.tmp_feature_json = "ipl_place.json"


class CTS(Step):
    def __init__(self):
        super().__init__()
        self.name = StepName.CTS
        self.description = "Clock Tree Synthesis by iEDA-iCTS"
        self.shell_cmd = configs.SHELL_CMD[self.name]
        self.tmp_feature_json = "icts.json"


class DrvOpt(Step):
    def __init__(self):
        super().__init__()
        self.name = StepName.DRV_OPT
        self.description = "Optimization Design Rule Voilation by iEDA-iTO"
        self.shell_cmd = configs.SHELL_CMD[self.name]
        self.tmp_feature_json = "ito_optDrv.json"


class HoldOpt(Step):
    def __init__(self):
        super().__init__()
        self.name = StepName.HOLD_OPT
        self.description = "Optimization Hold Time Voilation by iEDA-iTO"
        self.shell_cmd = configs.SHELL_CMD[self.name]
        self.tmp_feature_json = "ito_opthold.json"


class Legalize(Step):
    def __init__(self):
        super().__init__()
        self.name = StepName.LEGALIZE
        self.description = "Standard Cell Legalization by iEDA-iPL"
        self.shell_cmd = configs.SHELL_CMD[self.name]
        self.tmp_feature_json = "ipl_legalization.json"


class Filler(Step):
    def __init__(self):
        super().__init__()
        self.name = StepName.FILLER
        self.description = "Adding Filler for DFM by iEDA-iPL"
        self.shell_cmd = configs.SHELL_CMD[self.name]
        self.tmp_feature_json = "summary_ipl_filler.json"


class Route(Step):
    def __init__(self):
        super().__init__()
        self.name = StepName.ROUTE
        self.description = "Routing by iEDA-iRT"
        self.shell_cmd = configs.SHELL_CMD[self.name]
        self.tmp_feature_json = "irt.json"
