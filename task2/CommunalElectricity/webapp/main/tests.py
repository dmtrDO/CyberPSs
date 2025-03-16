import unittest
from .views import calculate_total

# day   4,32
# night 2,16

class TestTotalPrice(unittest.TestCase):

    def test_total(self):
        self.assertEqual(calculate_total(10, 10, 15, 15), (5 * 4.32, 5 * 2.16, 5 * 4.32 + 5 * 2.16))
        self.assertEqual(calculate_total(2, 2, 3, 3), (4.32, 2.16, 4.32 + 2.16))


