import os
import subprocess
from multiprocessing import Pool

import orjson

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
        print("step." + self.name)
        ret_code = subprocess.call(self.shell_cmd, env=io_env)
        assert ret_code == 0, f"Step {self.name} failed with return code {ret_code}"

    def update_progress_bar(self):
        pass


class Synthesis(Step):
    def __init__(self):
        super().__init__()
        self.name = "synthesis"
        self.description = "synthesis by yosys"
        # RTL_FILE, DESIGN_TOP, SDC
        # NETLIST_FILE, MODULE_AREA
        self.shell_cmd = configs.SHELL_CMD[self.name]


class Floorplan(Step):
    def __init__(self):
        super().__init__()
        self.name = "floorplan"
        self.description = "Floorplaning by iEDA-iFP"
        # NETLIST_FILE, DESIGN_TOP, (MODULE_AREA+Utilization) or (DIE_AREA+CORE_AREA)
        # OUTPUT_DEF
        self.shell_cmd = configs.SHELL_CMD[self.name]


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


class DumpLayout(Step):
    def __init__(self, layout_fmt="gds"):
        super().__init__()
        self.description = "Dump Layout by iEDA-DB"
        if layout_fmt == "gds":
            self.name = "layout_gds"
            # INPUT_DEF
            # GDS_FILE
            self.shell_cmd = configs.SHELL_CMD[self.name]
        elif layout_fmt == "json":
            self.name = "layout_json"
            # INPUT_DEF
            # GDS_JSON_FILE
            self.shell_cmd = configs.SHELL_CMD[self.name]

        # elif layout_fmt == 'oasis':
        #     self.shell_cmd = Configs.shell_cmd['layout_oasis']


MAX_FILE_SIZE = 49 * 1024 * 1024  # 49MB in bytes


def process_chunk(args):
    data_chunk, file_no_suffix, index = args
    chunk_data = {"data": data_chunk}
    with open(f"{file_no_suffix}-{index}.json", "wb") as file:
        file.write(orjson.dumps(chunk_data))


def split_gds_json(filename: str):
    with open(filename, "rb") as f:
        data = orjson.loads(f.read())

    assert "data" in data, "Invalid data format: 'data' key missing"
    assert isinstance(data["data"], list), "Invalid data format: not a list"

    header = {key: value for key, value in data.items() if key != "data"}
    file_no_suffix = os.path.splitext(filename)[0]

    with open(f"{file_no_suffix}-header.json", "wb") as file:
        file.write(orjson.dumps(header))

    chunks = []
    current_chunk = []
    current_size = 0

    for item in data["data"]:
        item_size = len(orjson.dumps(item))
        if current_size + item_size > MAX_FILE_SIZE:
            chunks.append((current_chunk, file_no_suffix, len(chunks)))
            current_chunk = []
            current_size = 0
        current_chunk.append(item)
        current_size += item_size

    if current_chunk:
        chunks.append((current_chunk, file_no_suffix, len(chunks)))

    with Pool() as pool:
        pool.map(process_chunk, chunks)


def factory(step_name: str):
    step_map = {
        "synthesis": Synthesis,
        "floorplan": Floorplan,
        "fixfanout": FixFanout,
        "place": Place,
        "cts": CTS,
        "drv_opt": DrvOpt,
        "hold_opt": HoldOpt,
        "legalize": Legalize,
        "route": Route,
        "filler": Filler,
        "layout_gds": DumpLayout("gds"),
        "layout_json": DumpLayout("json"),
    }
    return step_map[step_name]()
