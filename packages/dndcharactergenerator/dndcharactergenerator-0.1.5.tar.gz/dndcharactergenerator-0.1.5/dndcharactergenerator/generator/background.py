from random import choice

from .gamedata.background_data import BACKGROUNDDATA


class Background:
    """
    A class to represent a character's background.

    Attributes
    ----------
    name : str
        The name of the background
    skills : list[str]
        The skill proficiencies that come with the background
    detail : str
        Further description to flesh out the background
    trait : str
        Personality traits of the character
    ideal : str
        What drives the character (goals, core beliefs, etc.)
    bond : str
        What ties the character to their background (connections to world, people, etc.)
    flaw : str
        Character flaws of the character
    auto_generate : bool
        Indicate whether to automatically generate empty attributes

    Methods
    -------
    generate(background_name = None):
        Generates a random background from the D&D background based on the passed in name.
    """

    def __init__(
        self,
        name: str = None,
        skills: list[str] = None,
        detail: str = None,
        trait: str = None,
        ideal: str = None,
        bond: str = None,
        flaw: str = None,
        auto_generate=False,
    ) -> None:
        """
        Constructs a Background object.

        Parameters
        ----------
            name : str, optional
                The name of the background
            skills : list[str], optional
                The skill proficiencies that come with the background
            detail : str, optional
                Further description to flesh out the background
            trait : str, optional
                Personality traits of the character
            ideal : str, optional
                What drives the character (goals, core beliefs, etc.)
            bond : str, optional
                What ties the character to their background (connections to world, people, etc.)
            flaw : str, optional
                Character flaws of the character
            auto_generate : bool, optional
                Indicate whether to randomly automatically empty attributes, default False
        """

        self.name = name
        self.skills = skills
        self.detail = detail
        self.trait = trait
        self.ideal = ideal
        self.bond = bond
        self.flaw = flaw
        if auto_generate:
            self.generate()

    def __str__(self) -> str:
        return self.name

    def generate(self, background_name: str = None) -> None:
        """
        Generates a random background from the D&D background based on the passed
        in name.

        Attempts to use the objects Background.name if no argument is present,
        the finally selects a random background if none is present.

        Parameters
        ----------
        background_name : str, optional
            Name of the D&D background to force a generation for, by default None
        """
        # Check argument, then self.name for class name, checking validity. If invalid,
        # get a random class name.
        background_names = list(BACKGROUNDDATA.keys())

        if self.name and not background_name:
            background_name = self.name
        if not background_name:
            background_name = choice(background_names)
        if background_name not in background_names:
            raise ValueError(
                f"Background Name Argument (or Background.name) must match a race name in {background_names}."
            )

        # Populate object with random attributes, overwritting if necessary.
        background = BACKGROUNDDATA[background_name]
        self.name = background_name
        self.skills = background["skills"]
        self.detail = choice(background["details"])
        self.trait = choice(background["traits"])
        self.ideal = choice(background["ideals"])
        self.bond = choice(background["bonds"])
        self.flaw = choice(background["flaws"])

        return self
