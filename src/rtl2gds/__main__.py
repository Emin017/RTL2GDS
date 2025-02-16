#!/usr/bin/env python3
"""module main"""
import argparse
import logging
import pathlib

from . import flow
from .chip import Chip


def main():
    """rtl2gds flow"""
    parser = argparse.ArgumentParser(prog="rtl2gds")
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="log level",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=pathlib.Path,
        required=True,
        help="design config file",
    )
    args = parser.parse_args()

    logging.basicConfig(
        format="[%(asctime)s - %(levelname)s - %(name)s]: %(message)s",
        level=args.log_level,
    )

    logging.info("rtl2gds starting...")

    chip_design = Chip(args.config)

    flow.rtl2gds_flow.run(chip_design)

    logging.info("rtl2gds finished")
    # rtl2gds_flow.dump_metrics()
    # rtl2gds_flow.dump_gds()


if __name__ == "__main__":
    main()
