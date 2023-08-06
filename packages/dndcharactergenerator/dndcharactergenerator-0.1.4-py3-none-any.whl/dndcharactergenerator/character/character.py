from ..generator.stats import Stats
from ..generator.race import Race
from ..generator.gameclass import GameClass
from ..generator.background import Background


class Character:
    """
    A D&D Character.

        Parameters
        ----------
        base_stats : generator.stats.Stats, optional
            The character's rolled stats, by default None
        game_class : generator.gameclass.GameClass, optional
            The character's selected D&D class, by default None
        race : generator.race.Race, optional
            The character's selected D&D race, by default None
        background : generator.background.Background, optional
            The character's selected D&D background, by default None
        auto_generate : bool, optional
            If True, will immediately call self.generate() to
            populate missing fields, by default True

        Methods
        -------
        generate()
            Generates the missing information about a D&D character based on the
            information the character currently has.

        get_stats()
            Returns the sum of a characters rolled base stats and
            the stats modifier from it's race.

        get_base_ac()
            Calculates and returns the base Armor Class of the object.

        get_skills()
            Combines together and returns a list made up of the skill
            proficiencies from a characters gameclass and it's background.
    """

    def __init__(
        self,
        base_stats=None,
        game_class=None,
        race=None,
        background=None,
        auto_generate=True,
    ):
        """
        A D&D Character.

        Parameters
        ----------
        base_stats : generator.stats.Stats, optional
            The character's rolled stats, by default None
        game_class : generator.gameclass.GameClass, optional
            The character's selected D&D class, by default None
        race : generator.race.Race, optional
            The character's selected D&D race, by default None
        background : generator.background.Background, optional
            The character's selected D&D background, by default None
        auto_generate : bool, optional
            If True, will immediately call self.generate() to
            populate missing fields, by default True

        Example
        -----------
        >> Character(game_class = GameClass("Rogue"))

        """
        self.base_stats = base_stats
        self.game_class = game_class
        self.race = race
        self.background = background

        if auto_generate:
            self.generate()

    def generate(self):
        """
        Generates the missing information about a D&D character based on the
        information the character currently has.

        Generates and fits remaining attributes based first on Stats if present,
        then Class, then Race.
        """
        can_generate_for = [False, False, False]

        if isinstance(self.base_stats, Stats):
            can_generate_for[0] = True

        if isinstance(self.game_class, GameClass):
            can_generate_for[1] = True
        elif isinstance(self.game_class, str):
            self.game_class = GameClass(self.game_class, auto_generate=True)
            can_generate_for[1] = True

        if isinstance(self.race, Race):
            can_generate_for[2] = True
        elif isinstance(self.race, str):
            self.race = Race(self.race, auto_generate=True)
            can_generate_for[2] = True

        if isinstance(self.background, str):
            self.background = Background(self.background, auto_generate=True)
        elif not isinstance(self.background, Background):
            self.background = Background(auto_generate=True)

        if can_generate_for[0]:
            if not isinstance(self.game_class, GameClass):
                self.game_class = GameClass()
                self.game_class.generate_from_stats(self.base_stats)
            if not isinstance(self.race, Race):
                self.race = Race()
                self.race.generate_from_stats(self.base_stats)
        elif can_generate_for[1]:
            if not isinstance(self.base_stats, Stats):
                self.base_stats = Stats()
                self.base_stats.generate_from_gameclass(self.game_class)
            if not isinstance(self.race, Race):
                self.race = Race()
                self.race.generate_from_gameclass(self.game_class)
        elif can_generate_for[2]:
            if not isinstance(self.base_stats, Stats):
                self.base_stats = Stats()
                self.base_stats.generate_from_race(self.race)
            if not isinstance(self.game_class, GameClass):
                self.game_class = GameClass()
                self.game_class.generate_from_stats(self.base_stats)
        else:
            self.base_stats = Stats(auto_generate=True)

            self.game_class = GameClass()
            self.game_class.generate_from_stats(self.base_stats)

            self.race = Race()
            self.race.generate_from_stats(self.base_stats)

    def get_stats(self):
        """
        Returns the sum of a characters rolled base stats and
        the stats modifier from it's race.

        Returns
        -------
        generator.stats.Stats
            The calculated true stats of a character.
        """
        return self.base_stats + self.race.stats_mod

    def get_base_AC(self):
        """
        Calculates and returns the base Armor Class of the object.

        Currently supports Barbarian and Monk Unarmoured Defense,
        but no actual equipment yet.

        Returns
        -------
        int
            The calculated base Armor Class
        """
        AC = 10 + (self.get_stats().DEX - 10) // 2

        if self.game_class.name == "Barbarian":
            AC += (self.get_stats().CON - 10) // 2
        elif self.game_class.name == "Monk":
            AC += (self.get_stats().WIS - 10) // 2

        return AC

    def get_skills(self):
        """
        Combines together and returns a list made up of the skill
        proficiencies from a characters gameclass and it's background.

        Returns
        -------
        list
            The combined list of skill proficiencies.
        """
        return self.game_class.skills + self.background.skills
