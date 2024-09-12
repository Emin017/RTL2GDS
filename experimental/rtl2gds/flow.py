import yaml

from . import metrics
from . import step
from . import chip


class RTL2GDS:

    def __init__(self, chip: chip):
        self.chip = chip
        self.metrics: FlowMetrics
        self._steps = [
            "floorplan",
            "fixfanout",
            "place",
            "cts",
            "drv_opt",
            "hold_opt",
            "legalize",
            "route",
            "layout_gds",
        ]

    def run(self):
        # netlist_file = self.chip.path_setting.netlist_file
        floorplan = step.Floorplan()
        # input=netlist_file, output=self.chip.path_setting.def_file
        floorplan.run(self.chip.io_env)
        # self.update_metrics()

        # iterate over steps except theose with special input and output
        for step_name in self._steps[1:-1]:
            s = step.factory(step_name)
            s.run(self.chip.io_env)
            # step.input = self.chip.path_setting.def_file
            # step.output = self.chip.path_setting.def_file
            # self.update_metrics()

        layout_gds = step.DumpLayout()
        # input=self.chip.path_setting.def_file, output=self.chip.gds_file
        layout_gds.run(self.chip.io_env)
        # self.update_metrics()

    def update_metrics(self):
        pass

    def dump_metrics(self):
        pass

    def dump_gds(self):
        pass


class FlowMetrics:

    def __init__(self):
        self.design: metrics.DesignMetrics
        self.step: metrics.EDAMetrics

    def dump(self):
        return yaml.dump(self.__dict__)
