import subprocess
import Configs

class Step:
    def __init__(self, input = str, output = str):
        self.name: str
        self.description: str
        self.input = input
        self.output = output
        self.shell_cmd = str

    def run(self):
        subprocess.call(self.shell_cmd)

    def update_progress_bar(self):
        pass

class Floorplan(Step):
    def __init__(self):
        super().__init__()
        self.name = 'floorplan'
        self.description = 'Floorplaning by iEDA-iFP'
        self.shell_cmd = Configs.shell_cmd['floorplan']

class FixFanout(Step):
    def __init__(self):
        super().__init__()
        self.name = 'fixfanout'
        self.description = 'Fixing fanout by iEDA-iNO'
        self.shell_cmd = Configs.shell_cmd['fixfanout']

class Place(Step):
    def __init__(self):
        super().__init__()
        self.name = 'place'
        self.description = 'Standard Cell Placement by iEDA-iPL'
        self.shell_cmd = Configs.shell_cmd['place']

class CTS(Step):
    def __init__(self):
        super().__init__()
        self.name = 'cts'
        self.description = 'Clock Tree Synthesis by iEDA-iCTS'
        self.shell_cmd = Configs.shell_cmd['cts']

class DrvOpt(Step):
    def __init__(self):
        super().__init__()
        self.name = 'drv_opt'
        self.description = 'Optimization Design Rule Voilation by iEDA-iTO'
        self.shell_cmd = Configs.shell_cmd['drv_opt']

class HoldOpt(Step):
    def __init__(self):
        super().__init__()
        self.name = 'hold_opt'
        self.description = 'Optimization Hold Time Voilation by iEDA-iTO'
        self.shell_cmd = Configs.shell_cmd['hold_opt']

class Legalize(Step):
    def __init__(self):
        super().__init__()
        self.name = 'legalize'
        self.description = 'Standard Cell Legalization by iEDA-iPL'
        self.shell_cmd = Configs.shell_cmd['legalize']

class Route(Step):
    def __init__(self):
        super().__init__()
        self.name = 'route'
        self.description = 'Routing by iEDA-iRT'
        self.shell_cmd = Configs.shell_cmd['route']

class DumpLayout(Step):
    def __init__(self, format = 'gds'):
        super().__init__()
        self.description = 'Dump Layout by iEDA-DB'
        if format == 'gds':
            self.name = 'layout_gds'
            self.shell_cmd = Configs.shell_cmd['layout_gds']
        elif format == 'json':
            self.name = 'layout_json'
            self.shell_cmd = Configs.shell_cmd['layout_json']
        # elif format == 'oasis':
        #     self.shell_cmd = Configs.shell_cmd['layout_oasis']

def factory(step_name: str):
    step_map = {
        'floorplan': Floorplan,
        'fixfanout': FixFanout,
        'place': Place,
        'cts': CTS,
        'drv_opt': DrvOpt,
        'hold_opt': HoldOpt,
        'legalize': Legalize,
        'route': Route,
        'layout_gds': DumpLayout('gds'),
        'layout_json': DumpLayout('json'),
    }
    return step_map[step_name]
