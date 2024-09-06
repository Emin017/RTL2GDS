import Flow
import Chip

if __name__ == '__main__':
    chip = Chip.Chip()
    chip.load_config('./gcd.yaml')

    rtl2gds_flow = Flow.rtl2gds(chip)
    rtl2gds_flow.run()

    rtl2gds_flow.design_metrics.dump()

