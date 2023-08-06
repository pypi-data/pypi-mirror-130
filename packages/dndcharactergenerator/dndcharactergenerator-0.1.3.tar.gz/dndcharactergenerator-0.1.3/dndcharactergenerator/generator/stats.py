from .rpggenerator import RpgGenerator


class EmptyStatsError(Exception):
    pass


class Stats(RpgGenerator):
    """
    A class to represent the character's D&D stats.

    Attributes
    ----------
    STR : int
        The character Strength value
    DEX : int
        The character Dexterity value
    CON : int
        The character Constitution value
    INT : int
        The character Intelligence value
    WIS : int
        The character Wisdom value
    CHA : int
        The character Charisma value
    auto_generate : bool
        Indicate whether to automatically generate empty parameters

    Methods
    -------
    generate():
        Populates the Stats objects with random stats according to roll_3d6_drop_lowest().
    maximize_for_stats(other_stats):
        Rolls for stats, populates stat values based on preferences inidcated in other_stats.
    generate_from_gameclass(gameclass):
        Rolls for stats, prioritizes based on D&D class preferences.
    generate_from_race(race):
        Rolls for stats, prioritizes based on D&D race preferences
    """

    def __init__(
        self,
        STR: int = 0,
        DEX: int = 0,
        WIS: int = 0,
        INT: int = 0,
        CHA: int = 0,
        CON: int = 0,
        auto_generate=False,
    ):
        """
        Constructs a D&D Stats object.

        Parameters
        ----------
            STR : int, optional
                The character Strength value, default zero
            DEX : int, optional
                The character Dexterity value, default zero
            CON : int, optional
                The character Constitution value, default zero
            INT : int, optional
                The character Intelligence value, default zero
            WIS : int, optional
                The character Wisdom value, default zero
            CHA : int, optional
                The character Charisma value, default zero
            auto_generate : bool, optional
                Indicate whether to automatically generate empty parameters, default False
        """
        self.STR = STR
        self.DEX = DEX
        self.WIS = WIS
        self.INT = INT
        self.CHA = CHA
        self.CON = CON
        if auto_generate:
            self.generate()

    def __str__(self) -> str:
        return str("\t".join([f"{stat} = {value}" for stat, value in self]))

    def generate(self):
        """
        Populates the Stats objects with random stats according to roll_3d6_drop_lowest().
        """
        if not self.STR:
            self.STR = RpgGenerator.roll_3d6_drop_lowest()
        if not self.DEX:
            self.DEX = RpgGenerator.roll_3d6_drop_lowest()
        if not self.WIS:
            self.WIS = RpgGenerator.roll_3d6_drop_lowest()
        if not self.INT:
            self.INT = RpgGenerator.roll_3d6_drop_lowest()
        if not self.CHA:
            self.CHA = RpgGenerator.roll_3d6_drop_lowest()
        if not self.CON:
            self.CON = RpgGenerator.roll_3d6_drop_lowest()
        return self

    def maximize_for_stats(self, other_stats):
        try:
            other_stats.STR
        except AttributeError:
            raise TypeError("other_stats must be a generator.stats.Stats object.")

        if not len([stat for stat, value in other_stats if value]):
            raise EmptyStatsError(
                "other_stats must have some non-zero stat values to generate for."
            )

        self.generate()
        previous_stat_values = [value for stat, value in self]
        priority_stats = [stat for stat, value in other_stats if value]
        remaining_stats = [stat for stat, value in other_stats if not value]

        # Null out stats before assigning new ones
        for stat, value in self:
            setattr(self, stat, None)

        # Assign the max from stats list to match statsmods bonuses,
        # then assign the remaining 4 stats randomly to the remaining stats
        for priority_stat in priority_stats:
            setattr(
                self,
                priority_stat,
                previous_stat_values.pop(
                    previous_stat_values.index(max(previous_stat_values))
                ),
            )
        for remaining_stat in remaining_stats:
            setattr(self, remaining_stat, previous_stat_values.pop())
        return self

    def generate_from_gameclass(self, gameclass):
        """
        Populates the missing Stats in the stats objects, then re-arranges them to best
        fit the needs of the passed in D&D class.

        Parameters
        ----------
        gameclass : generator.gameclass.GameClass
            the D&D class that you want to fit the stats to.
        """
        try:
            gameclass.preferred_stats.STR
        except AttributeError:
            raise TypeError(
                "gameclass must be a valid generator.gameclass.Gameclass object with preferred_stats."
            )

        self.maximize_for_stats(gameclass.preferred_stats)
        return self

    def generate_from_race(self, race):
        """
        Populates the missing Stats in the stats objects, then re-arranges them to best
        fit the needs of the passed in D&D race.

        Parameters
        ----------
        race : generator.race.Race
            the D&D race that you want to fit the stats to.
        """
        try:
            race.stats_mod.STR
        except AttributeError:
            raise TypeError(
                "race must be a valid generator.race.Race object with stats_mod."
            )

        self.maximize_for_stats(race.stats_mod)
        return self

    def __add__(self, other):
        """
        Returns another stats object where each stat is the sum of the individual stats

        Parameters
        ----------
        other : Stats
            Other stats object.

        Returns
        -------
        Stats
            The resulting Stats object.
        """
        new_STR = self.STR + other.STR
        new_DEX = self.DEX + other.DEX
        new_WIS = self.WIS + other.WIS
        new_INT = self.INT + other.INT
        new_CHA = self.CHA + other.CHA
        new_CON = self.CON + other.CON
        return Stats(
            STR=new_STR, DEX=new_DEX, WIS=new_WIS, INT=new_INT, CHA=new_CHA, CON=new_CON
        )

    def __eq__(self, other):
        """
        Returns a boolean indicating whether two stats objects have identical values.

        Parameters
        ----------
        other : Stats
            Other stats object.

        Returns
        -------
        bool
            The result of testing equivalency of each stat.
        """

        return (
            self.STR == other.STR
            and self.DEX == other.DEX
            and self.CON == other.CON
            and self.WIS == other.WIS
            and self.INT == other.INT
            and self.CHA == other.CHA
        )
