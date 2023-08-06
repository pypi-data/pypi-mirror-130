import unittest

from .gameclass import GameClass
from .race import Race
from .stats import Stats, EmptyStatsError


class TestGameClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # update as gamedata grows
        cls.dex_classes = ["Ranger", "Rogue", "Bard"]
        cls.str_classes = ["Barbarian", "Paladin"]
        cls.dex_stats = Stats(DEX=True)
        cls.str_stats = Stats(STR=True)
        cls.invalid_stats = Stats()
        cls.elf_race = Race("Elf", auto_generate=True)
        cls.dwarf_race = Race("Dwarf", auto_generate=True)
        cls.invalid_race_1 = Race("Human")
        cls.invalid_race_2 = Race(stats_mod=Stats())

    def setUp(self) -> None:
        self.empty_class_1 = GameClass()
        self.empty_class_2 = GameClass()
        self.empty_class_3 = GameClass()
        self.empty_class_4 = GameClass()
        self.empty_class_5 = GameClass()
        self.barbarian_class = GameClass("Barbarian")
        self.invalid_class = GameClass("Hooligan")

    def test_gameclass_generate(self):
        self.assertIsNotNone(self.empty_class_1.generate().name)
        self.assertEqual(self.empty_class_2.generate("Rogue").name, "Rogue")
        self.assertEqual(self.barbarian_class.generate().name, "Barbarian")
        self.assertEqual(self.barbarian_class.generate().preferred_stats.STR, True)
        with self.assertRaises(ValueError):
            self.invalid_class.generate()

    def test_generate_from_stats(self):
        self.assertIn(
            self.empty_class_1.generate_from_stats(TestGameClass.dex_stats).name,
            TestGameClass.dex_classes,
        )

        self.assertIn(
            self.empty_class_2.generate_from_stats(TestGameClass.str_stats).name,
            TestGameClass.str_classes,
        )

        self.assertIsNot(
            self.barbarian_class.generate_from_stats(TestGameClass.dex_stats).name,
            "Barbarian",
        )

        with self.assertRaises(TypeError):
            self.empty_class_3.generate_from_stats("DEX")
        with self.assertRaises(EmptyStatsError):
            self.empty_class_4.generate_from_stats(TestGameClass.invalid_stats)

    def test_gameclass_generate_from_race(self):
        self.empty_class_1.generate_from_race(TestGameClass.elf_race)
        elf_race_preferred_stats = [
            stat for stat, value in TestGameClass.elf_race.stats_mod if value
        ]
        empty_class_1_stats_mod = [
            stat for stat, value in self.empty_class_1.preferred_stats if value
        ]
        self.assertTrue(
            elf_race_preferred_stats[0] in empty_class_1_stats_mod
            or elf_race_preferred_stats[1] in empty_class_1_stats_mod
        )
        self.empty_class_2.generate_from_race(TestGameClass.dwarf_race)
        gameclass_2_preferred_stats = [
            stat for stat, value in TestGameClass.dwarf_race.stats_mod if value
        ]
        empty_race_2_stats_mod = [
            stat for stat, value in self.empty_class_2.preferred_stats if value
        ]
        self.assertTrue(
            gameclass_2_preferred_stats[0] in empty_race_2_stats_mod
            or gameclass_2_preferred_stats[1] in empty_race_2_stats_mod
        )
        self.assertIsNot(
            self.barbarian_class.generate_from_race(TestGameClass.elf_race).name,
            "Barbarian",
        )
        with self.assertRaises(TypeError):
            self.empty_class_3.generate_from_race("Human")
        with self.assertRaises(TypeError):
            self.empty_class_4.generate_from_race(TestGameClass.invalid_race_1)
        with self.assertRaises(EmptyStatsError):
            self.empty_class_5.generate_from_race(TestGameClass.invalid_race_2)

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass
