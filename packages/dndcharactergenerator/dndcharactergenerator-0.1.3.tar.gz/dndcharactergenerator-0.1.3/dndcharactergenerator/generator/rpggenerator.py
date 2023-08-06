from abc import ABC, abstractmethod
from random import randint


class RpgGenerator(ABC):
    """
    The virtual Generator Class to be overridden by
    child classes with generating capabilities.

    Not to be instatiated.

    METHODS
    -------
    generate()
        The virtual function to randomly populate the attributes of an object
        that is inherited from the generator class.

    roll_3d6_drop_lowest()
        Rolls 4d6, and returns the sum of the top 3 dice.
    """

    def __init__(self) -> None:
        pass

    def __iter__(self):
        for field, fieldvalue in self.__dict__.items():
            yield field, fieldvalue

    @abstractmethod
    def generate(self):
        """
        The virtual function to randomly populate the attributes of an object
        that is inherited from the generator class.

        VIRTUAL FUNCTION - must be overridden in child class.
        """
        pass

    @staticmethod
    def roll_3d6_drop_lowest() -> int:
        """
        Rolls 4d6, and returns the sum of the top 3 dice.

        Returns
        -------
        int
            Sum of Dice
        """
        rolls = [randint(1, 6) for i in range(4)]
        rolls.remove(min(rolls))
        return sum(rolls)
