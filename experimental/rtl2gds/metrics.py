import yaml

class DesignMetrics:
    '''
    DesignMetrics class
    store and manipulate design PPA metrics
    '''
    def __init__(self):
        # description metrics
        self.tech = '130nm',
        self.instance = int,
        self.wirelength = int,
        self.stdcell = int,
        # self.macro = {
        #     'mem': int,
        # }

        # performance metrics
        self.longest_logic_level = int,
        self.performance = {
            'main_freq_mhz': float,
            'critical_path': float,
        }

        # power metrics
        self.power = {
            'total': float,
            'leakage': float,
            'switch': float,
            'internal': float,
        }

        # area metrics
        self.die = list[float]
        self.core = list[float]
        self.area = {
            # 'die': float,
            'core': float,
            'stdcell': float,
            'utilization': float,
        }

        # signoff violation metrics
        self.drc = int, # 0 drc
        self.lvs = int, # 0 lvs
        self.sta = int, # setup slack >= 0

    def dump(self):
        return yaml.dump(self.__dict__)


class EDAMetrics:
    '''
    EDAMetrics class
    store and manipulate EDA tool metrics
    '''
    def __init__(self):
        self.tool = str,
        self.version = str,
