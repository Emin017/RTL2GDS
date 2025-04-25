#!/usr/bin/env python3
"""test flow"""

from rtl2gds import Chip, flow


def main():
    """
    gcd + rtl2gds flow

    # design_setting:
    TOP_NAME: gcd

    # path_setting:
    RTL_FILE: ../gcd/gcd.v
    NETLIST_FILE: ./gcd_results/gcd_netlist.v
    RESULT_DIR: ./gcd_results
    GDS_FILE: ./gcd_results/gcd.gds
    """

    gcd = Chip("gcd")
    gcd.constrain = {
        "CLK_PORT_NAME": "clk",
        "CLK_FREQ_MHZ": "200",
        "DIE_AREA": " 0  0 120 120",
        "CORE_AREA": "10 10 110 110",
    }
    gcd.load_config("./gcd.yaml")

    rtl2gds_flow = flow.RTL2GDS(gcd)
    rtl2gds_flow.run()

    rtl2gds_flow.dump_metrics()
    rtl2gds_flow.dump_gds()


if __name__ == "__main__":
    main()
