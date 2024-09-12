import subprocess

from . import configs


class Step:
    def __init__(self):
        # self.input = input
        # self.output = output
        self.name: str
        self.description: str
        self.shell_cmd: list[str]

    def run(self, io_env: dict[str:str]):
        """
        TCL KEY IO ENV:
        INPUT_DEF
        GDS_FILE
        """
        ret_code = subprocess.call(self.shell_cmd, env=io_env)
        assert ret_code == 0, f"Step {self.name} failed with return code {ret_code}"

    def update_progress_bar(self):
        pass


class Floorplan(Step):
    def __init__(self):
        super().__init__()
        self.name = "floorplan"
        self.description = "Floorplaning by iEDA-iFP"
        self.shell_cmd = configs.SHELL_CMD["floorplan"]


class FixFanout(Step):
    def __init__(self):
        super().__init__()
        self.name = "fixfanout"
        self.description = "Fixing fanout by iEDA-iNO"
        self.shell_cmd = configs.SHELL_CMD["fixfanout"]


class Place(Step):
    def __init__(self):
        super().__init__()
        self.name = "place"
        self.description = "Standard Cell Placement by iEDA-iPL"
        self.shell_cmd = configs.SHELL_CMD["place"]


class CTS(Step):
    def __init__(self):
        super().__init__()
        self.name = "cts"
        self.description = "Clock Tree Synthesis by iEDA-iCTS"
        self.shell_cmd = configs.SHELL_CMD["cts"]


class DrvOpt(Step):
    def __init__(self):
        super().__init__()
        self.name = "drv_opt"
        self.description = "Optimization Design Rule Voilation by iEDA-iTO"
        self.shell_cmd = configs.SHELL_CMD["drv_opt"]


class HoldOpt(Step):
    def __init__(self):
        super().__init__()
        self.name = "hold_opt"
        self.description = "Optimization Hold Time Voilation by iEDA-iTO"
        self.shell_cmd = configs.SHELL_CMD["hold_opt"]


class Legalize(Step):
    def __init__(self):
        super().__init__()
        self.name = "legalize"
        self.description = "Standard Cell Legalization by iEDA-iPL"
        self.shell_cmd = configs.SHELL_CMD["legalize"]


class Route(Step):
    def __init__(self):
        super().__init__()
        self.name = "route"
        self.description = "Routing by iEDA-iRT"
        self.shell_cmd = configs.SHELL_CMD["route"]


class DumpLayout(Step):
    def __init__(self, layout_fmt="gds"):
        super().__init__()
        self.description = "Dump Layout by iEDA-DB"
        if layout_fmt == "gds":
            self.name = "layout_gds"
            # INPUT_DEF
            # GDS_FILE
            self.shell_cmd = configs.SHELL_CMD["layout_gds"]
        elif layout_fmt == "json":
            self.name = "layout_json"
            # INPUT_DEF
            # GDS_JSON_FILE
            self.shell_cmd = configs.SHELL_CMD["layout_json"]

        # elif layout_fmt == 'oasis':
        #     self.shell_cmd = Configs.shell_cmd['layout_oasis']


@staticmethod
def factory(step_name: str):
    step_map = {
        "floorplan": Floorplan,
        "fixfanout": FixFanout,
        "place": Place,
        "cts": CTS,
        "drv_opt": DrvOpt,
        "hold_opt": HoldOpt,
        "legalize": Legalize,
        "route": Route,
        "layout_gds": DumpLayout("gds"),
        "layout_json": DumpLayout("json"),
    }
    return step_map[step_name]()
