from dataclasses import dataclass


@dataclass
class DesignConstrain:
    """
    Design Constrains

    `clk_port_name`: str
        Clock port name
    `clk_freq_mhz`: float
        Clock frequency in MHz
    `die_bbox`: str
        Die area in format
        "lower_left_x, lower_left_y, upper_right_x, upper_right_y"
    `core_bbox`: str
        Core area in format
        "lower_left_x, lower_left_y, upper_right_x, upper_right_y"
    `core_util`: float
        Core utilization in percentage
    """
    # timing constrain (sdc)
    clk_port_name: str
    clk_freq_mhz: float
    # area constrain
    die_bbox: str | None = None
    core_bbox: str | None = None
    core_util: float | None = None

    def to_env_dict(self) -> dict[str, str]:
        """Convert to dictionary with uppercase keys for environment variables."""
        return {
            "CLK_PORT_NAME": str(self.clk_port_name),
            "CLK_FREQ_MHZ": str(self.clk_freq_mhz),
            "DIE_AREA": str(self.die_bbox),   # without `xywh`!
            "CORE_AREA": str(self.core_bbox),   # without `xywh`!
            "CORE_UTIL": str(self.core_util),
        }
