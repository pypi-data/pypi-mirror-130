import unittest

from .rpggenerator import RpgGenerator

# The "RpgGenerator" class is beyond the 3 base classes for the assignment.
# Therefore, this test script is smaller than the others.
class TestRpgGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        pass

    def test_roll_4d6_drop_lowest(self):
        for i in range(100):
            self.assertTrue(3 <= RpgGenerator.roll_3d6_drop_lowest() <= 18)

    def test_virtual_methods(self):
        with self.assertRaises(TypeError):
            self.virtual_object = RpgGenerator()

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass
