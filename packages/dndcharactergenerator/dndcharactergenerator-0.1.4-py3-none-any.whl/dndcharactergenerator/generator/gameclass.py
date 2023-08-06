from random import choice, sample

from .rpggenerator import RpgGenerator
from .stats import Stats, EmptyStatsError
from .gamedata.gameclass_data import GAMECLASSDATA


class GameClass(RpgGenerator):
    """
    A class to represent the character's D&D class.

    Attributes
    ----------
    class_name : str
        The name of the class
    hit_dice : str
        The type of dice the class uses for hit dice (d6, d12, etc.)
    skills : list[str]
        The skill proficiencies that come with the class
    preferred_stats : generator.stats.Stats
        Indicates which stats the class prefers (non-zero values indicate preference)
    subclass : str
        The name of the subclass
    saving_throws : generator.stats.Stats
        Indicates which stats the class is proficient in for saving throws (non-zero values indicate proficiency)
    auto_generate : bool
        Indicate whether to automatically generate empty attributes

    Methods
    -------
    generate(class_name = None):
        Populates empty GameClass attributes based on existing parameters.
    generate_from_stats(stats):
        Selects the best D&D Class based on given stats values.
    generate_from_race(race):
        Selects the best D&D Class based on given race.
    """

    def __init__(
        self,
        class_name: str = None,
        hit_dice: str = None,
        skills: list[str] = None,
        preferred_stats=None,
        subclass: str = None,
        saving_throws=None,
        auto_generate=False,
    ) -> None:
        """
        Constructs a D&D Class object.

        Parameters
        ----------
            class_name : str, optional
                The name of the class
            hit_dice : str, optional
                The type of dice the class uses for hit dice (d6, d12, etc.)
            skills : list[str], optional
                The skill proficiencies that come with the class
            preferred_stats : generator.stats.Stats, optional
                Indicates which stats the class prefers (non-zero values indicate preference)
            subclass : str, optional
                The name of the subclass
            saving_throws : generator.stats.Stats, optional
                Indicates which stats the class is proficient in for saving throws (non-zero values indicate proficiency)
            auto_generate : bool, optional
                Indicate whether to automatically generate empty attributes, default False
        """
        self.name = class_name
        self.hit_dice = hit_dice
        self.skills = skills
        self.preferred_stats = preferred_stats
        self.subclass = subclass
        self.saving_throws = saving_throws

        if auto_generate:
            self.generate()

    def __str__(self) -> str:
        return self.name if self.name else "None"

    def generate(self, class_name: str = None):
        """
        Populates the attributes of the GameClass object with data from D&D,
        choosing a random class if no valid class is present first as an argument,
        then as an object attribute.

        Parameters
        ----------
        class_name : str, optional
            The name of the class to force the function to search for, by default None
        """
        # Check argument, then self.name for class name, checking validity.
        # If invalid, get a random class name.
        class_names = list(GAMECLASSDATA.keys())

        if self.name and not class_name:
            class_name = self.name
        if not class_name:
            class_name = choice(class_names)
        if class_name not in class_names:
            raise ValueError(
                f"class_name Argument (or GameClass.name) must match a race name in {class_names}."
            )

        # Populate object with random attributes, overwritting if necessary.
        gameclass = GAMECLASSDATA[class_name]
        self.name = class_name
        self.hit_dice = gameclass["hit_dice"]
        self.saving_throws = gameclass["saving_throws"]
        self.skills = sample(gameclass["skills"], 2)
        self.preferred_stats = gameclass["preferred_stats"]
        self.subclass = choice(gameclass["subclasses"])
        return self

    def generate_from_stats(self, stats):
        """
        Selects an appropriate D&D class and populates attributes based on a
        passed in D&D stats.

        Parameters
        ----------
        stats : Stats
            The desired Stat array to fit a class to.
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

        # Get list of class names that match max stat.
        # If none is found, iterates down to the next lowest stat and so on until one is.

        potential_gameclasses = False
        while not potential_gameclasses and stat_dict:
            max_stat = max(stat_dict, key=stat_dict.get)

            potential_gameclasses = [
                gameclass
                for gameclass, values in GAMECLASSDATA.items()
                if getattr(values["preferred_stats"], max_stat)
            ]
            # Remove current maximum (but unmatched) stat for further iterations.
            max_stat = stat_dict.pop(max_stat)

        # If no matching class is found, just randomize it.
        # If lots are, pick one and generate from it.
        if potential_gameclasses:
            self.name = choice(potential_gameclasses)
        self.generate()
        return self

    def generate_from_race(self, race):
        """
        Selects an appropriate D&D class and populates attributes based on a
        passed on D&D race.

        Parameters
        ----------
        race : Race
            The desired race to fit to.
        """
        # check for bad gameclass
        try:
            race.stats_mod
        except AttributeError:
            raise TypeError("race must be a generator.race.Race object.")

        # check for bad stat attribute
        if not isinstance(race.stats_mod, Stats):
            raise TypeError("race.stats_mod must be a generator.stats.Stats object.")
        # check for empty Stat attribute.
        if not len([stat for stat, value in race.stats_mod if value]):
            raise EmptyStatsError(
                "Race.stats_mod must have some non-zero stat values to generate for."
            )

        self.generate_from_stats(race.stats_mod)
        return self
