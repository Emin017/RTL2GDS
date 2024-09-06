import subprocess
import Configs
import Metrics
import Step
import Chip
import yaml

class Flow:

    def __init__(self, chip: Chip):
        self.chip = chip
        self.metrics: FlowMetrics
        self.steps = ['floorplan', 'fixfanout', 'place', 'cts', 'drv_opt', 'hold_opt', 'legalize', 'route', 'layout_gds']

    def run(self):
        netlist_file = self.chip.netlist_file
        floorplan = Step.Floorplan(
            input = netlist_file,
            output = self.chip.def_file
        )
        floorplan.run()
        self.update_metrics()

        # iterate over steps except theose with special input and output
        for step_name in self.steps[1:-1]:
            step = Step.factory(step_name)
            step.input = self.chip.def_file
            step.output = self.chip.def_file
            step.run()
            self.update_metrics()

        layout_gds = Step.DumpLayout(
            input = self.chip.def_file,
            output = self.chip.gds_file
        )
        layout_gds.run()
        self.update_metrics()

        
    def update_metrics(self):
        pass

class FlowMetrics:

    def __init__(self):
        self.design: Metrics.DesignMetrics
        self.step: Metrics.EDAMetrics

    def dump(self):
        return yaml.dump(self.__dict__)
