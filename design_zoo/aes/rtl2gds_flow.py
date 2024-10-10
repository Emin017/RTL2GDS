#!/usr/bin/env python3
"""test flow"""
import os
import sys

# Add Python module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from rtl2gds import chip, flow


def main():
    """aes + rtl2gds flow"""

    aes = chip.Chip("aes") # top name is not necessary
    aes.load_config("./aes.yaml")

    rtl2gds_flow = flow.RTL2GDS(aes)
    rtl2gds_flow.run()

    rtl2gds_flow.dump_metrics()
    rtl2gds_flow.dump_gds()


if __name__ == "__main__":
    main()
