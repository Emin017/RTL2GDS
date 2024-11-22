""" Step runner factory """

from . import dump_layout_gds, dump_layout_json, floorplan, synthesis
from .step import CTS, DrvOpt, Filler, FixFanout, HoldOpt, Legalize, Place, Route

__all__ = [
    "synthesis",
    "floorplan",
    "dump_layout_gds",
    "dump_layout_json",
    "pr_step_map",
]


pr_step_map = {
    "fixfanout": FixFanout(),
    "place": Place(),
    "cts": CTS(),
    "drv_opt": DrvOpt(),
    "hold_opt": HoldOpt(),
    "legalize": Legalize(),
    "route": Route(),
    "filler": Filler(),
}

from ..global_configs import PR_FLOW_STEP

# Verify pr_step_map matches PR_FLOW_STEP
assert (
    list(pr_step_map.keys()) == PR_FLOW_STEP
), f"pr_step_map keys {list(pr_step_map.keys())} do not match PR_FLOW_STEP {PR_FLOW_STEP}"

# "synthesis": synthesis.run,
# "floorplan": floorplan.run,
# "fixfanout": fixfanout.run,
# "place": place.run,
# "cts": cts.run,
# "drv_opt": drv_opt.run,
# "hold_opt": hold_opt.run,
# "legalize": legalize.run,
# "route": route.run,
# "filler": filler.run,
# "layout_gds": dump_layout_gds.run,
# "layout_json": dump_layout_json.run,
