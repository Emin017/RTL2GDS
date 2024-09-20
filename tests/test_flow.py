import unittest

from rtl2gds import chip


class TestFlow(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_naive(self):
        gcd = chip.Chip("gcd")
        self.assertIsInstance(gcd, chip.Chip)
