"""
description: behavior of each RTL2GDS step
"""

import logging
import os
import subprocess

import rtl2gds.global_configs as configs

from ..global_configs import DEFAULT_SDC_FILE, ENV_TOOLS_PATH
from . import configs


class Step:
    def __init__(self):
        self.name: str
        self.description: str
        self.shell_cmd: list

    def run(
        self,
        design_top: str,
        input_def: str,
        result_dir: str,
        output_def: str,
        clk_port_name: str,
        clk_freq_mhz: float,
    ):
        """
        TCL KEY IO ENV:
        INPUT_DEF
        GDS_FILE
        """
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
        self.name = "fixfanout"
        self.description = "Fixing fanout by iEDA-iNO"
        self.shell_cmd = configs.SHELL_CMD[self.name]


class Place(Step):
    def __init__(self):
        super().__init__()
        self.name = "place"
        self.description = "Standard Cell Placement by iEDA-iPL"
        self.shell_cmd = configs.SHELL_CMD[self.name]


class CTS(Step):
    def __init__(self):
        super().__init__()
        self.name = "cts"
        self.description = "Clock Tree Synthesis by iEDA-iCTS"
        self.shell_cmd = configs.SHELL_CMD[self.name]


class DrvOpt(Step):
    def __init__(self):
        super().__init__()
        self.name = "drv_opt"
        self.description = "Optimization Design Rule Voilation by iEDA-iTO"
        self.shell_cmd = configs.SHELL_CMD[self.name]


class HoldOpt(Step):
    def __init__(self):
        super().__init__()
        self.name = "hold_opt"
        self.description = "Optimization Hold Time Voilation by iEDA-iTO"
        self.shell_cmd = configs.SHELL_CMD[self.name]


class Legalize(Step):
    def __init__(self):
        super().__init__()
        self.name = "legalize"
        self.description = "Standard Cell Legalization by iEDA-iPL"
        self.shell_cmd = configs.SHELL_CMD[self.name]


class Filler(Step):
    def __init__(self):
        super().__init__()
        self.name = "filler"
        self.description = "Adding Filler for DFM by iEDA-iPL"
        self.shell_cmd = configs.SHELL_CMD[self.name]


class Route(Step):
    def __init__(self):
        super().__init__()
        self.name = "route"
        self.description = "Routing by iEDA-iRT"
        self.shell_cmd = configs.SHELL_CMD[self.name]
