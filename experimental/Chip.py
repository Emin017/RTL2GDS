import yaml
import Metrics

class Chip:
    def __init__(self):
        self.config
        self.design_top: str
        self.rtl_file: str
        self.netlist_file: str
        self.def_file: str
        self.gds_file: str
        self.json_file: str
        self.clk_port: str


    def load_config(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.design_top = self.config['DESIGN_TOP']
        self.rtl_file = self.config['RTL_FILE']
        self.gds_file = self.config['GDS_FILE']
        self.clk_freq_mhz = self.config['CLK_FREQ_MHZ']
