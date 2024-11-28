from dataclasses import dataclass


@dataclass
class DesignConstrain:
    # timing constrain (sdc)
    clk_port_name: str
    clk_freq_mhz: float
    # area constrain
    die_area: str = None
    core_area: str = None
    core_util: float = None

    def to_env_dict(self) -> dict:
        """Convert to dictionary with uppercase keys for environment variables."""
        return {
            "CLK_PORT_NAME": str(self.clk_port_name),
            "CLK_FREQ_MHZ": str(self.clk_freq_mhz),
            "DIE_AREA": str(self.die_area),
            "CORE_AREA": str(self.core_area),
            "CORE_UTIL": str(self.core_util),
        }
