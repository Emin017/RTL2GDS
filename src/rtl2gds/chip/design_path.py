from dataclasses import dataclass

from rtl2gds.global_configs import DEFAULT_SDC_FILE


@dataclass
class DesignPath:
    rtl_file: str | list[str]
    result_dir: str
    netlist_file: str
    def_file: str
    gds_file: str
    sdc_file: str = DEFAULT_SDC_FILE

    def to_env_dict(self) -> dict[str, str]:
        """Convert to dictionary with uppercase keys for environment variables."""
        if isinstance(self.rtl_file, list):
            # Join with newlines for yosys compatibility
            self.rtl_file = " \n ".join(self.rtl_file)
        return {
            "RTL_FILE": self.rtl_file,
            "RESULT_DIR": str(self.result_dir),
            "NETLIST_FILE": str(self.netlist_file),
            "INPUT_DEF": str(self.def_file),  # it's `INPUT_DEF`!
            "OUTPUT_DEF": str(self.def_file),  # it's `OUTPUT_DEF`!
            "GDS_FILE": str(self.gds_file),
            "SDC_FILE": self.sdc_file,
        }


# test for single file rtl_file and list of rtl_file
if __name__ == "__main__":
    design_path = DesignPath(
        rtl_file="test.v",
        netlist_file="test.v",
        result_dir="test",
        sdc_file="test.sdc",
    )
    # print instance type of design_path.rtl_file
    print(type(design_path.rtl_file))
    print(design_path.to_env_dict())

    design_path = DesignPath(
        rtl_file=["test_a.v", "test_b.v", "test_c.v"],
        netlist_file="test.v",
        result_dir="test",
        sdc_file="test.sdc",
    )
    print(type(design_path.rtl_file))
    print(design_path.to_env_dict())