#!/usr/bin/env python3
"""test flow"""
import os
import sys

# Add Python module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from rtl2gds import chip, flow


def main():
    """picorv32 + rtl2gds flow"""

    picorv32 = chip.Chip("picorv32") # top name is not necessary
    picorv32.load_config("./pico.yaml")

    rtl2gds_flow = flow.RTL2GDS(picorv32)
    rtl2gds_flow.run()

    rtl2gds_flow.dump_metrics()
    rtl2gds_flow.dump_gds()


if __name__ == "__main__":
    main()
