def a_or_an(noun):
    """
    Returns "a" or "an" based on which word would naturally
    occur before the passed in noun.

    Parameters
    ----------
    noun : str
        The word you wish to determine an article for.

    Returns
    -------
    str
        "a" or "an"
    """
    if noun[0].lower() in "aeiou":
        return "an " + noun
    else:
        return "a " + noun


def stat_descriptor(stat, mod):
    """
    Returns a common-language string describing the magnitude and description
    of the passed in D&D stat and stat modifier.

    Parameters
    ----------
    stat : str
        An abbreviation of a D&D stat ("STR", "DEX", etc)
    mod : int
        A stat modifier for D&D, ideally between -6 and 6.

    Returns
    -------
    str
        A adverb-adjective pair describing the passed in stat and modifier.
    """
    if stat == "STR":
        if mod > 0:
            stat = "STRONG"
        else:
            stat = "WEAK"
    if stat == "DEX":
        if mod > 0:
            stat = "DEXTROUS"
        else:
            stat = "CLUMSY"
    if stat == "CON":
        if mod > 0:
            stat = "HEALTHY"
        else:
            stat = "SICKLY"
    if stat == "INT":
        if mod > 0:
            stat = "SMART"
        else:
            stat = "DUMB"
    if stat == "WIS":
        if mod > 0:
            stat = "WISE"
        else:
            stat = "FOOLISH"
    if stat == "CHA":
        if mod > 0:
            stat = "CHARISMATIC"
        else:
            stat = "UNLIKEABLE"

    mod = abs(mod)
    if mod > 5:
        return f"unfathomably {stat}"
    if mod > 4:
        return f"extremely {stat}"
    if mod > 3:
        return f"very {stat}"
    if mod > 2:
        return f"{stat}"
    if mod > 1:
        return f"quite {stat}"
    if mod > 0:
        return f"kind of {stat}"
    return None


def display(char):
    """
    Prints out fundamental information about the passed in character object,
    including the character's name, race, class, and stats.

    Parameters
    ----------
    char : character.character.Character
        The character object you wish to display.
    """
    print(f'You are {char.race.first_name} {char.race.last_name}, {a_or_an(char.race.subrace.upper())} {char.game_class.subclass.upper()} {char.game_class.name.upper()}.')

    stat_descriptors = []
    for stat, value in char.get_stats():
        mod = (value - 10) // 2
        if mod:
            stat_descriptors.append(stat_descriptor(stat, mod))

    if len(stat_descriptors):
        print(f"You are {stat_descriptors[0]}", end="")
        for i in range(1, len(stat_descriptors) - 1):
            print(f", {stat_descriptors[i]}", end="")
        if len(stat_descriptors) > 1:
            print(f", and {stat_descriptors[-1]}", end="")
        print(".")
    else:
        print("You are a very unremarkable individual.")


# for testing
if __name__ == "__main__":
    display(character.Character(race="Halfling", gameClass="Druid"))
