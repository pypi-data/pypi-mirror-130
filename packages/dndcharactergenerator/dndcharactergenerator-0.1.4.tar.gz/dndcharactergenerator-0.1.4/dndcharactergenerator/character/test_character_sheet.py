import unittest
import io
import os
import pdfrw
from contextlib import redirect_stdout

from .character_sheet import get_char_info
from .character_sheet import display
from .character_sheet import save_to_pdf
from .character import Character
from ..generator.stats import Stats


class TestCharacterSheet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wise_dwarf = Character(
            base_stats=Stats(DEX=17, WIS=18),
            race="Dwarf",
            game_class="Barbarian",
            background="Acolyte",
        )

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_char_info(self):
        self.assertIsInstance(get_char_info(self.wise_dwarf), dict)
        self.assertTrue("Dwarf" in get_char_info(self.wise_dwarf)["Race"])
        self.assertEqual(get_char_info(self.wise_dwarf)["DEX"], 17)
        self.assertEqual(get_char_info(self.wise_dwarf)["WISmod"], 4)
        self.assertEqual(get_char_info(self.wise_dwarf)["Passive"], 14)

    def test_display(self):
        with redirect_stdout(io.StringIO()) as f:
            display(self.wise_dwarf)
        self.assertGreater(len(f.getvalue()), 0)
        self.assertTrue("Dwarf" in f.getvalue())
        self.assertTrue("Dexterity:\t\t\t17 (3)" in f.getvalue())
        self.assertTrue("Insight" in f.getvalue())
        self.assertTrue("Passive Perception:\t\t14" in f.getvalue())

    def test_save_to_pdf(self):
        # Delete output PDF if already exists
        pdf_template_fpath = __file__.replace(
            "test_character_sheet.py", "test_charsheet.pdf"
        )
        if os.path.exists(pdf_template_fpath):
            os.remove(pdf_template_fpath)

        # Run save_to_pdf()
        save_to_pdf(self.wise_dwarf, destination=pdf_template_fpath)

        # Test assertions
        self.assertTrue(
            os.path.exists(pdf_template_fpath)
        )  # assertion 1 (file was created)
        cs_pdf = pdfrw.PdfReader(pdf_template_fpath)
        annotations = cs_pdf.pages[0]["/Annots"]
        for annotation in annotations:
            if annotation["/Subtype"] == "/Widget":
                if annotation["/T"]:
                    key = annotation["/T"][1:-1].strip()
                    if key == "ClassLevel":
                        self.assertTrue("Barbarian" in annotation["/V"])  # assertion 2
                    elif key == "Race":
                        self.assertTrue("Dwarf" in annotation["/V"])  # assertion 3
                    elif key == "DEX":
                        self.assertTrue("17" in annotation["/V"])  # assertion 4
                    elif key == "Speed":
                        self.assertTrue("25" in annotation["/V"])  # assertion 5

        os.remove(pdf_template_fpath)
