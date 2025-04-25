""" Step runner factory """

from . import drc, floorplan, layout_gds, layout_json, synthesis
from .step import (CTS, DrvOpt, Filler, HoldOpt, Legalization, NetlistOpt,
                   Placement, Routing)

__all__ = [
    "synthesis",
    "floorplan",
    "layout_gds",
    "layout_json",
    "pr_step_map",
    "drc",
    "sta",
]


pr_step_map = {
    "netlist_opt": NetlistOpt(),
    "placement": Placement(),
    "cts": CTS(),
    "drv_opt": DrvOpt(),
    "hold_opt": HoldOpt(),
    "legalization": Legalization(),
    "routing": Routing(),
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
