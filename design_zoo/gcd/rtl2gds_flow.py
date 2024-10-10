#!/usr/bin/env python3
"""test flow"""
import os
import sys

# Add Python module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from rtl2gds import chip, flow


def main():
    """gcd + rtl2gds flow"""

    gcd = chip.Chip("gcd") # top name is not necessary
    gcd.load_config("./gcd.yaml")

    rtl2gds_flow = flow.RTL2GDS(gcd)
    rtl2gds_flow.run()

    rtl2gds_flow.dump_metrics()
    rtl2gds_flow.dump_gds()


if __name__ == "__main__":
    main()
