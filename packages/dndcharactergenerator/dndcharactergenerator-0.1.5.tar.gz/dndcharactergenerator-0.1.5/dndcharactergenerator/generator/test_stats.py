import unittest
from random import seed

from .stats import Stats, EmptyStatsError
from .gameclass import GameClass
from .race import Race


class TestStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.known_stats = {
            "STR": 10,
            "DEX": 10,
            "WIS": 10,
            "INT": 10,
            "CHA": 10,
            "CON": 20,
        }
        cls.gameclass_1 = GameClass("Barbarian", auto_generate=True)
        cls.gameclass_2 = GameClass("Wizard", auto_generate=True)
        cls.race_1 = Race("Elf", auto_generate=True)
        cls.race_2 = Race("Dwarf", auto_generate=True)

    def setUp(self) -> None:
        seed(2021)
        self.stats_random = Stats(auto_generate=True)
        self.stats_known = Stats(**TestStats.known_stats)
        self.stats_dex = Stats(DEX=20)
        self.stats_linear = Stats(*range(1, 7))
        self.empty_stats_1 = Stats()
        self.empty_stats_2 = Stats()

    def test_generate(self):
        self.assertIsNotNone(self.empty_stats_1.generate().STR)
        self.assertEqual(self.stats_dex.generate().DEX, 20)
        self.assertEqual(self.stats_known.generate().CON, 20)
        self.assertTrue(3 <= self.stats_random.WIS <= 18)
        self.assertTrue(3 <= self.empty_stats_2.generate().WIS <= 18)

    def test_maximize_for_stats(self):
        self.assertEqual(self.stats_known.maximize_for_stats(Stats(STR=True)).STR, 20)
        self.assertNotEqual(self.stats_dex.maximize_for_stats(Stats(INT=True)).DEX, 20)
        self.assertListEqual(
            list(range(1, 7)),
            sorted(
                [
                    value
                    for stat, value in self.stats_linear.maximize_for_stats(
                        Stats(INT=True)
                    )
                ]
            ),
        )
        with self.assertRaises(EmptyStatsError):
            self.stats_random.maximize_for_stats(Stats())
        with self.assertRaises(TypeError):
            self.empty_stats_2.maximize_for_stats("WIS")

    def test_generate_from_gameclass(self):
        self.assertIsNotNone(
            self.empty_stats_1.generate_from_gameclass(TestStats.gameclass_1).CHA
        )
        self.stats_known.generate_from_gameclass(TestStats.gameclass_1)
        self.assertTrue(self.stats_known.STR == 20 or self.stats_known.CON == 20)
        self.stats_linear.generate_from_gameclass(TestStats.gameclass_2)
        self.assertTrue(self.stats_linear.INT == 6 or self.stats_linear.DEX == 6)
        with self.assertRaises(TypeError):
            self.empty_stats_2.generate_from_gameclass(GameClass())
        with self.assertRaises(TypeError):
            self.stats_dex.generate_from_gameclass("Rogue")

    def test_generate_from_race(self):
        self.assertIsNotNone(
            self.empty_stats_1.generate_from_race(TestStats.race_1).CHA
        )
        self.stats_known.generate_from_race(TestStats.race_1)
        self.assertTrue(
            self.stats_known.DEX == 20
            or self.stats_known.INT == 20
            or self.stats_known.CHA == 20
        )
        self.stats_linear.generate_from_race(TestStats.race_2)
        self.assertTrue(
            self.stats_linear.STR == 6
            or self.stats_linear.CON == 6
            or self.stats_linear.WIS == 6
        )
        with self.assertRaises(TypeError):
            self.empty_stats_2.generate_from_race(Race())
        with self.assertRaises(TypeError):
            self.stats_dex.generate_from_race("Human")

    def test_stat_addition(self):
        self.combined_stats = self.stats_known + self.stats_linear
        self.assertEqual(
            self.combined_stats.STR, (self.stats_known.STR + self.stats_linear.STR)
        )
        self.assertEqual(
            self.combined_stats.CON, (self.stats_known.CON + self.stats_linear.CON)
        )
        self.double_random_stats = self.stats_random + self.stats_random
        self.assertEqual(self.double_random_stats.INT, (2 * self.stats_random.INT))
        self.stats_dex_2 = self.stats_dex + self.empty_stats_1
        self.assertEqual(self.stats_dex_2.DEX, self.stats_dex.DEX)
        self.assertEqual(self.stats_dex_2.CHA, 0)

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass


if __name__ == "__main__":
    from stats import Stats

    unittest.main()
