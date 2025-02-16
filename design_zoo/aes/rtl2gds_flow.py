#!/usr/bin/env python3
"""test flow"""
# # Add Python rtl2gds module path if necessary
# import os
# import sys
# sys.path.insert(
#     0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
# )

import logging

from rtl2gds import Chip, flow


def main():
    """aes + rtl2gds flow"""

    logging.basicConfig(
        format="[%(asctime)s - %(levelname)s - %(name)s]: %(message)s",
        level=logging.INFO,
    )

    aes = Chip("./aes.yaml")

    flow.rtl2gds_flow.run(aes)


if __name__ == "__main__":
    main()
