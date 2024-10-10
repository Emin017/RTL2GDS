# RTL2GDS-GCD Example

This README provides instructions on how to run the RTL-to-GDS flow for the Greatest Common Divisor (GCD) design.

There are two methods to run the RTL-to-GDS flow for the GCD design:

## Method 1: Using the RTL2GDS Module

Execute the following shell command, replacing `RTL2GDS_ROOT` with the actual project path directory:

```bash
PYTHONPATH="${RTL2GDS_ROOT}/src:$PYTHONPATH" python3 -m rtl2gds -c gcd.yaml
```

## Method 2: Using RTL2GDS Python API

```bash
python3 rtl2gds_flow.py
```
