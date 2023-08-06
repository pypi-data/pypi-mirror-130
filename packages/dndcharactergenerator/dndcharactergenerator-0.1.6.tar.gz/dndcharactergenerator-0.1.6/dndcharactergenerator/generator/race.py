from random import choice

from .rpggenerator import RpgGenerator
from .stats import Stats, EmptyStatsError
from .gamedata.race_data import RACEDATA


class Race(RpgGenerator):
    """
    A class to represent the character's D&D race.

    Attributes
    ----------
    name : str
        The name of the race
    first_name : str
        The first name of the character
    last_name : str
        The last name of the character
    speed : int
        The speed (in feet per turn) of the race
    subrace : str
        The name of the subrace
    stats_mod : generator.stats.Stats
        The stat modifiers that come with the race
    auto_generate : bool
        Indicate whether to automatically generate empty attributes

    Methods
    -------
    generate(race_name = None):
        Populates empty Race attributes based on existing parameters.
    generate_from_stats(stats):
        Selects the best D&D Race based on given stats values.
    generate_from_gameclass(gameclass):
        Selects the best D&D Race based on given D&D Class.
    """

    def __init__(
        self,
        name: str = None,
        first_name: str = None,
        last_name: str = None,
        speed: int = None,
        subrace: str = None,
        stats_mod=None,
        auto_generate=False,
    ) -> None:
        """
        Constructs a D&D Race object.

        Parameters
        ----------
            name : str, optional
                The name of the race
            first_name : str, optional
                The first name of the character
            last_name : str, optional
                The last name of the character
            speed : int, optional
                The speed (in feet per turn) of the race
            subrace : str, optional
                The name of the subrace
            stats_mod : generator.stats.Stats
                The stat modifiers that come with the race
            auto_generate : bool, optional
                Indicate whether to automatically generate empty attributes, default False
        """
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.speed = speed
        self.subrace = subrace
        self.stats_mod = stats_mod

        if auto_generate:
            self.generate()

    def __str__(self) -> str:
        return self.subrace if self.subrace else (self.race if self.race else "None")

    def generate(self, race_name: str = None) -> None:
        """
        Populates the object with random attributes generated from the D&D data
        based on a passed in race name.

        Attempts to use the passed in race name first, then the objects Race.name second,
        then finally generates a random race if neither is valid.

        Parameters
        ----------
        race_name : str, optional
            A valid race name within the d&d data you wish to populate, by default None
        """
        # Check arguments and attribute for race name, and check validity.
        # Get random race if not valid.
        # TODO: Update so that we can fit to a SUBRACE, not just a race

        race_names = list(RACEDATA.keys())

        if self.name and not race_name:
            race_name = self.name
        if not race_name:
            race_name = choice(race_names)
        if race_name not in race_names:
            raise ValueError(
                f"Race Name Argument (or Race.name) must match a race name in {race_names}."
            )

        # Populate object with random attributes, overwritting if necessary.
        race = RACEDATA[race_name]
        self.name = race_name
        self.first_name = choice(race["first_name"])
        self.last_name = choice(race["last_name"])
        self.speed = race["speed"]

        subrace_name = choice(list(race["subraces"]))
        self.subrace = subrace_name
        self.stats_mod = race["subraces"][subrace_name]["stats_mod"]
        return self

    def generate_from_stats(self, stats: Stats) -> None:
        """
        Selects an appropriate random race based on the passed in stats
        and populates the object with attributes from the D&D data.

        Parameters
        ----------
        stats : generator.stats.Stats
            The stat array you want to select a race with.
        """

        # check for bad stat attribute
        if not isinstance(stats, Stats):
            raise TypeError("stats must be a generator.stats.Stats object.")
        # check for empty Stat attribute.
        if not len([stat for stat, value in stats if value]):
            raise EmptyStatsError(
                "stats must have some non-zero stat values to generate for."
            )

        stat_dict = {stat: value for stat, value in stats}

        potential_races = []
        while not potential_races and stat_dict:
            max_stat = max(stat_dict, key=stat_dict.get)

            for race, racedata in RACEDATA.items():
                for subrace, subrace_data in racedata["subraces"].items():
                    if getattr(subrace_data["stats_mod"], max_stat):
                        potential_races.append(race)

            # Remove current maximum (but unmatched) stat for further iterations.
            max_stat = stat_dict.pop(max_stat)

        if potential_races:
            self.name = choice(potential_races)
        self.generate()

        # TODO: Update to search for specific SUBRACE, not just race when generate() function is updated.
        # In the meantime, here's an awful recursive fix:
        stats_preferred_stats = [stat for stat, value in stats if value]
        race_stats_mod = [stat for stat, value in self.stats_mod if value]
        if not (
            stats_preferred_stats[0] in race_stats_mod
            or stats_preferred_stats[1] in race_stats_mod
        ):
            self.generate_from_stats(stats)

        return self

    def generate_from_gameclass(self, gameclass) -> None:
        """
        Selects an appropriate random race based on the passed in stats
        and populates the object with attributes from that D&D data.

        Parameters
        ----------
        gameclass : generator.gameclass.GameClass
            The game class you want to select a race with.
        """
        # check for bad gameclass
        try:
            gameclass.preferred_stats
        except AttributeError:
            raise TypeError("gameclass must be a generator.gameclass.GameClass object.")

        # check for bad stat attribute
        if not isinstance(gameclass.preferred_stats, Stats):
            raise TypeError(
                "gameclass.preferred_stats must be a generator.stats.Stats object."
            )
        # check for empty Stat attribute.
        if not len([stat for stat, value in gameclass.preferred_stats if value]):
            raise EmptyStatsError(
                "gameclass.preferred_stats must have some non-zero stat values to generate for."
            )

        self.generate_from_stats(gameclass.preferred_stats)
        return self
