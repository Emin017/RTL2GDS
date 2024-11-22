from dataclasses import dataclass
from typing import List


@dataclass
class DesignPath:
    rtl_file: List[str]
    netlist_file: str
    result_dir: str
    sdc_file: str
    def_file: str = None
    gds_file: str = None

    def to_env_dict(self) -> dict:
        """Convert to dictionary with uppercase keys for environment variables."""
        return {
            "RTL_FILE": " \n ".join(
                self.rtl_file
            ),  # Join with newlines for yosys compatibility
            "NETLIST_FILE": str(self.netlist_file),
            "DEF_FILE": str(self.def_file),
            "INPUT_DEF": str(self.def_file),  # attention, it's INPUT_DEF
            "GDS_FILE": str(self.gds_file),
            "RESULT_DIR": str(self.result_dir),
            "SDC_FILE": str(self.sdc_file),
        }
