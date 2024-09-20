from dataclasses import dataclass


@dataclass
class DesignConstrain:
    # timing constrain (sdc)
    clk_port_name: str
    clk_freq_mhz: int
    # area constrain
    die_area: str
    core_area: str
    # utility: float


# def export_env(self):
#     os.environ["CLK_PORT_NAME"] = self.clk_port_name
#     os.environ["CLK_FREQ_MHZ"] = self.clk_freq_mhz

#     os.environ["DIE_AREA"] = self.die_area
#     os.environ["CORE_AREA"] = self.core_area

# def dump_sdc(self, sdc_file: str):
