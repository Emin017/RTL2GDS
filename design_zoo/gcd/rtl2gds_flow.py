#!/usr/bin/env python3
"""test flow"""
# # Add Python rtl2gds module path if necessary
# import os
# import sys
# sys.path.insert(
#     0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
# )

from rtl2gds import Chip, flow


def main():
    """gcd + rtl2gds flow"""

    gcd = Chip.from_yaml("./gcd.yaml")

    flow.rtl2gd_flow.run(gcd)


if __name__ == "__main__":
    main()
