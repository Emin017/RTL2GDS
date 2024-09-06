import Flow
import Chip

if __name__ == '__main__':
    chip = Chip.Chip()
    chip.load_config('./gcd.yaml')

    rtl2gds_flow = Flow(chip)
    rtl2gds_flow.run()

    rtl2gds_flow.metrics.dump()
