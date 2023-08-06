import unittest

from .character import Character
from ..generator.stats import Stats
from ..generator.gameclass import GameClass
from ..generator.race import Race
from ..generator.background import Background

class TestCharacter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.strongGameClasses = ["Paladin", "Barbarian"]
        cls.randomChar = Character()
        cls.strongHuman = Character(base_stats=Stats(STR=20), race='Human')
        cls.zeroStats = Character(base_stats=Stats(), race=Race(stats_mod=Stats()), auto_generate=False)
        cls.c1 = Character(base_stats=Stats(STR=1), race=Race(stats_mod=Stats(DEX=1)), auto_generate=False)
        cls.c2 = Character(base_stats=Stats(DEX=10), race=Race(stats_mod=Stats()), game_class=GameClass(), auto_generate=False)
        cls.c3 = Character(base_stats=Stats(DEX=10, CON=12), race=Race(stats_mod=Stats()), game_class=GameClass('Barbarian'), auto_generate=False)
        cls.c4 = Character(base_stats=Stats(DEX=10, WIS=12), race=Race(stats_mod=Stats()), game_class=GameClass('Monk'), auto_generate=False)
        cls.c5 = Character(base_stats=Stats(DEX=10, CON=12, WIS=10), race=Race(stats_mod=Stats()), game_class=GameClass('Monk'), auto_generate=False)
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass
    def test_generate(self):

        self.assertIsInstance(self.randomChar.base_stats, Stats)
        self.assertIsInstance(self.randomChar.race, Race)
        self.assertIsInstance(self.randomChar.background, Background)
        self.assertIsInstance(self.randomChar.game_class, GameClass)
        self.assertIn(self.strongHuman.game_class.name, TestCharacter.strongGameClasses)

    def test_get_stats(self):
        self.assertIsInstance(self.randomChar.get_stats(), Stats)
        self.assertEqual(self.strongHuman.get_stats(), Stats(STR=20) + Race('Human', auto_generate=True).stats_mod)
        self.assertEqual(self.zeroStats.get_stats(), Stats())
        self.assertEqual(self.c1.get_stats(), Stats(STR=1, DEX=1))
        self.assertNotEqual(self.randomChar.get_stats(), Stats())

    def test_get_base_ac(self):
        self.assertIsInstance(self.randomChar.get_base_AC(), int)
        self.assertEqual(self.c2.get_base_AC(), 10)
        self.assertEqual(self.c3.get_base_AC(), 11)
        self.assertEqual(self.c4.get_base_AC(), 11)
        self.assertEqual(self.c5.get_base_AC(), 10)

