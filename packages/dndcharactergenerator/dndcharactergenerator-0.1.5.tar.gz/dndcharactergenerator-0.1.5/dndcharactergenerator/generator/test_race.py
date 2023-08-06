from random import seed
import unittest

from .race import Race
from .stats import Stats, EmptyStatsError
from .gameclass import GameClass

SEED = 2021


class TestRace(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # update as gamedata grows
        cls.dex_stats = Stats(DEX=25, auto_generate=True)
        cls.dex_races = ["Human", "Elf", "Gnome"]
        cls.str_stats = Stats(STR=25, auto_generate=True)
        cls.str_races = ["Human", "Dwarf", "Half-Orc"]
        cls.invalid_stats = Stats()
        cls.gameclass1 = GameClass("Barbarian", auto_generate=True)
        cls.gameclass2 = GameClass("Rogue", auto_generate=True)
        cls.invalid_gameclass_1 = GameClass(preferred_stats=None)
        cls.invalid_gameclass_2 = GameClass(preferred_stats=Stats())

    def setUp(self) -> None:
        seed(2021)
        self.empty_race_1 = Race()
        self.empty_race_2 = Race()
        self.empty_race_3 = Race()
        self.empty_race_4 = Race()
        self.empty_race_5 = Race()
        self.elf_race = Race("Elf")
        self.invalid_race = Race("Francisco")

    def test_race_generate(self):
        self.assertIsNotNone(self.empty_race_1.generate().name)
        self.assertEqual(self.empty_race_2.generate("Dwarf").name, "Dwarf")
        self.assertEqual(self.elf_race.generate().name, "Elf")
        self.assertEqual(self.elf_race.generate().speed, 30)
        with self.assertRaises(ValueError):
            self.invalid_race.generate()

    def test_generate_from_stats(self):
        self.assertIn(
            self.empty_race_1.generate_from_stats(TestRace.dex_stats).name,
            TestRace.dex_races,
        )
        self.assertIn(
            self.empty_race_2.generate_from_stats(TestRace.str_stats).name,
            TestRace.str_races,
        )
        self.assertIsNot(
            self.elf_race.generate_from_stats(TestRace.str_stats).name, "Elf"
        )
        with self.assertRaises(TypeError):
            self.empty_race_3.generate_from_stats("DEX")
        with self.assertRaises(EmptyStatsError):
            self.empty_race_4.generate_from_stats(TestRace.invalid_stats)

    def test_race_generate_from_gameclass(self):
        self.empty_race_1.generate_from_gameclass(TestRace.gameclass1)
        gameclass_1_preferred_stats = [
            stat for stat, value in TestRace.gameclass1.preferred_stats if value
        ]
        empty_race_1_stats_mod = [
            stat for stat, value in self.empty_race_1.stats_mod if value
        ]
        self.assertTrue(
            gameclass_1_preferred_stats[0] in empty_race_1_stats_mod
            or gameclass_1_preferred_stats[1] in empty_race_1_stats_mod
        )
        self.empty_race_2.generate_from_gameclass(TestRace.gameclass2)
        gameclass_2_preferred_stats = [
            stat for stat, value in TestRace.gameclass2.preferred_stats if value
        ]
        empty_race_2_stats_mod = [
            stat for stat, value in self.empty_race_2.stats_mod if value
        ]

        self.assertTrue(
            gameclass_2_preferred_stats[0] in empty_race_2_stats_mod
            or gameclass_2_preferred_stats[1] in empty_race_2_stats_mod
        )
        self.assertIsNot(
            self.elf_race.generate_from_gameclass(TestRace.gameclass1).name, "Elf"
        )
        with self.assertRaises(TypeError):
            self.empty_race_3.generate_from_gameclass("Rogue")
        with self.assertRaises(TypeError):
            self.empty_race_4.generate_from_gameclass(TestRace.invalid_gameclass_1)
        with self.assertRaises(EmptyStatsError):
            self.empty_race_5.generate_from_gameclass(TestRace.invalid_gameclass_2)

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass


if __name__ == "__main__":
    from race import Race

    unittest.main()
