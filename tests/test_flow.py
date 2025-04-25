import unittest

from rtl2gds import Chip


class TestFlow(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_naive(self):
        gcd = Chip("gcd")
        self.assertIsInstance(gcd, Chip)
