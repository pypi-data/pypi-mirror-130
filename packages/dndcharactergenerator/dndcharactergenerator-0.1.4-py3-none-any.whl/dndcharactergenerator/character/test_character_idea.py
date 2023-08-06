import unittest
import io
from contextlib import redirect_stdout

from .character import Character
from .character_idea import a_or_an
from .character_idea import stat_descriptor
from .character_idea import display
from ..generator.stats import Stats

class TestCharacterIdea(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a_or_an_test = a_or_an('test')
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_a_or_an(self):
        self.assertIsInstance(self.a_or_an_test, str)
        self.assertEqual(self.a_or_an_test, 'a test')
        self.assertEqual(a_or_an('TEST'), 'a TEST')
        self.assertEqual(a_or_an('elf'), 'an elf')
        self.assertEqual(a_or_an('ELF'), 'an ELF')

    def test_stat_descriptor(self):
        self.assertIsInstance(stat_descriptor('STR', 1), str)
        self.assertIsNone(stat_descriptor('STR', 0))
        self.assertEqual(stat_descriptor('STR', 4), 'very STRONG')
        self.assertEqual(stat_descriptor('STR', -4), 'very WEAK')
        self.assertEqual(stat_descriptor('not a stat', 5), 'extremely not a stat')

    def test_display(self):
        with redirect_stdout(io.StringIO()) as f:
            display(Character())
        self.assertGreater(len(f.getvalue()), 0)
        with redirect_stdout(io.StringIO()) as f:
            display(Character(base_stats=Stats(9, 9, 9, 9, 9, 9), race='Human'))
        self.assertEqual(f.getvalue()[-40:-1], "You are a very unremarkable individual.")
        with redirect_stdout(io.StringIO()) as f:
            display(Character(base_stats=Stats(STR=30, auto_generate=True)))
        self.assertTrue('unfathomably STRONG' in f.getvalue())
        with redirect_stdout(io.StringIO()) as f:
            display(Character(race='Dwarf'))
        self.assertTrue('DWARF' in f.getvalue())
        with redirect_stdout(io.StringIO()) as f:
            display(Character(game_class='Barbarian'))
        self.assertTrue('BARBARIAN' in f.getvalue())

        