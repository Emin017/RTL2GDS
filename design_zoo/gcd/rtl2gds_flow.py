#!/usr/bin/env python3
"""test flow"""

from rtl2gds import Chip, flow


def main():
    """gcd + rtl2gds flow"""

    gcd = Chip("./gcd.yaml")

    flow.rtl2gds_flow.run(gcd)


if __name__ == "__main__":
    main()
