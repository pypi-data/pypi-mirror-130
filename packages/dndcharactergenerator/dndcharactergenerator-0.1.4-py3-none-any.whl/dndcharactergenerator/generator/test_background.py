import unittest

from .background import Background

# The "Background" class is beyond the 3 base classes for the assignment.
# Therefore, this test script is smaller than the others.
class TestBackground(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.acolyte_skills = ["Insight", "Religion"]

    def setUp(self) -> None:
        self.acolyte_background = Background("Acolyte", auto_generate=True)
        self.empty_background_1 = Background()
        self.empty_background_2 = Background()
        self.invalid_background = Background("Boss Hog")

    def test_background_generate(self):
        self.assertIsNotNone(self.empty_background_1.generate().name)
        self.assertEqual(self.empty_background_2.generate("Criminal").name, "Criminal")
        self.assertEqual(self.acolyte_background.generate().name, "Acolyte")
        self.assertListEqual(
            self.acolyte_background.generate().skills, TestBackground.acolyte_skills
        )
        with self.assertRaises(ValueError):
            self.invalid_background.generate()

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass
