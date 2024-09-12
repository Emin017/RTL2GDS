"""test flow"""

from rtl2gds import chip, flow


def main():
    """gcd + rtl2gds flow"""

    gcd = chip.Chip()
    gcd.load_config("./gcd.yaml")

    rtl2gds_flow = flow.RTL2GDS(gcd)
    rtl2gds_flow.run()

    rtl2gds_flow.dump_metrics()
    rtl2gds_flow.dump_gds()


if __name__ == "__main__":
    main()
