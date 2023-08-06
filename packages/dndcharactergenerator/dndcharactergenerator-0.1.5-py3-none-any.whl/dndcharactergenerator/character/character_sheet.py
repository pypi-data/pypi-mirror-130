import pdfrw
from os import getcwd

class IncompleteCharacterException(Exception):
    pass

def get_char_info(char):
    """
    Populates and returns a dictionary of information about the passed in
    character.

    Each key corresponds to a single field on the form-fillable pdf character
    sheet, while each value corresponds to that fields information held in the
    character object.

    Parameters
    ----------
    char : character.character.Character
        The character you wish to generate the info dictionary for.

    Returns
    -------
    dict
        The key-value pairs linking the pdf character sheet fields
        to the character values.
    """
    stats = char.get_stats()
    stat_mods = {stat: (value - 10) // 2 for stat, value in stats}
    skills = char.get_skills()

    char_info = {
        "ClassLevel": f"{char.game_class.subclass} {char.game_class.name}",
        "Race": char.race.subrace,
        "Background": char.background.name,
        # 'PlayerName': None,
        "CharacterName": char.race.first_name + " " + char.race.last_name,
        # 'Alignment': None,
        # 'XP': None,
        # 'Inspiration': None,
        "STR": stats.STR,
        "STRmod": stat_mods["STR"],
        "DEX": stats.DEX,
        "DEXmod": stat_mods["DEX"],
        "CON": stats.CON,
        "CONmod": stat_mods["CON"],
        "INT": stats.INT,
        "INTmod": stat_mods["INT"],
        "WIS": stats.WIS,
        "WISmod": stat_mods["WIS"],
        "CHA": stats.CHA,
        "CHamod": stat_mods["CHA"],
        "ProfBonus": 2,
        "AC": char.get_base_AC(),
        "Initiative": (stats.DEX - 10) // 2,
        "Speed": char.race.speed,
        "PersonalityTraits": char.background.trait,
        "ST Strength": stat_mods["STR"] + 2 * char.game_class.saving_throws.STR,
        "ST Dexterity": stat_mods["DEX"] + 2 * char.game_class.saving_throws.DEX,
        "ST Constitution": stat_mods["CON"] + 2 * char.game_class.saving_throws.CON,
        "ST Intelligence": stat_mods["WIS"] + 2 * char.game_class.saving_throws.WIS,
        "ST Wisdom": stat_mods["INT"] + 2 * char.game_class.saving_throws.INT,
        "ST Charisma": stat_mods["CHA"] + 2 * char.game_class.saving_throws.CHA,
        "Ideals": char.background.ideal,
        "Bonds": char.background.bond,
        "HDTotal": char.game_class.hit_dice,
        # 'HD': None,
        "Flaws": char.background.flaw,
        "Acrobatics": stat_mods["DEX"] + 2 * ("Acrobatics" in skills),
        "Animal": stat_mods["WIS"] + 2 * ("Animal Handling" in skills),
        "Arcana": stat_mods["INT"] + 2 * ("Arcana" in skills),
        "Athletics": stat_mods["STR"] + 2 * ("Athletics" in skills),
        "Deception": stat_mods["CHA"] + 2 * ("Deception" in skills),
        "History": stat_mods["INT"] + 2 * ("History" in skills),
        "Insight": stat_mods["WIS"] + 2 * ("Insight" in skills),
        "Intimidation": stat_mods["CHA"] + 2 * ("Intimidation" in skills),
        "Investigation": stat_mods["INT"] + 2 * ("Investigation" in skills),
        "Medicine": stat_mods["WIS"] + 2 * ("Medicine" in skills),
        "Nature": stat_mods["INT"] + 2 * ("Nature" in skills),
        "Perception": stat_mods["WIS"] + 2 * ("Perception" in skills),
        "Performance": stat_mods["CHA"] + 2 * ("Performance" in skills),
        "Persuasion": stat_mods["CHA"] + 2 * ("Persuasion" in skills),
        "Religion": stat_mods["INT"] + 2 * ("Religion" in skills),
        "SleightofHand": stat_mods["DEX"] + 2 * ("Sleight of Hand" in skills),
        "Stealth": stat_mods["DEX"] + 2 * ("Stealth" in skills),
        "Survival": stat_mods["WIS"] + 2 * ("Survival" in skills),
        "Passive": (stats.WIS - 10) // 2 + 10,
        "Check Box 11": char.game_class.saving_throws.STR,
        "Check Box 18": char.game_class.saving_throws.DEX,
        "Check Box 19": char.game_class.saving_throws.CON,
        "Check Box 20": char.game_class.saving_throws.INT,
        "Check Box 21": char.game_class.saving_throws.WIS,
        "Check Box 22": char.game_class.saving_throws.CHA,
        "Check Box 23": "Acrobatics" in skills,
        "Check Box 24": "Animal Handling" in skills,
        "Check Box 25": "Arcana" in skills,
        "Check Box 26": "Athletics" in skills,
        "Check Box 27": "Deception" in skills,
        "Check Box 28": "History" in skills,
        "Check Box 29": "Insight" in skills,
        "Check Box 30": "Intimidation" in skills,
        "Check Box 31": "Investigation" in skills,
        "Check Box 32": "Medicine" in skills,
        "Check Box 33": "Nature" in skills,
        "Check Box 34": "Perception" in skills,
        "Check Box 35": "Performance" in skills,
        "Check Box 36": "Persuasion" in skills,
        "Check Box 37": "Religion" in skills,
        "Check Box 38": "Sleight" in skills,
        "Check Box 39": "Stealth" in skills,
        "Check Box 40": "Survival" in skills
        # 'Check Box 12': False,   # Death Save Success 1
        # 'Check Box 13': False,   # Death Save Success 2
        # 'Check Box 14': False,   # Death Save Success 3
        # 'Check Box 15': False,   # Death Save Failure 1
        # 'Check Box 16': False,   # Death Save Failure 2
        # 'Check Box 17': False,   # Death Save Failure 3
        # 'HPMax': None,
        # 'HPCurrent': None,
        # 'HPTemp': None,
        # 'Wpn Name': None,
        # 'Wpn1 AtkBonus': None,
        # 'Wpn1 Damage': None,
        # 'Wpn Name 2': None,
        # 'Wpn2 AtkBonus': None,
        # 'Wpn2 Damage': None,
        # 'Wpn Name 3': None,
        # 'Wpn3 AtkBonus': None,
        # 'Wpn3 Damage': None,
        # 'AttacksSpellcasting': None,
        # 'ProficienciesLang': None,
        # 'CP': None,
        # 'SP': None,
        # 'EP': None,
        # 'GP': None,
        # 'PP': None,
        # 'Equipment': None,
        # 'Features and Traits': None
    }
    return char_info


def display(char):
    """
    Prints detailed information about the passed in character
    object to represent what would be seen on thir character
    sheet.

    Parameters
    ----------
    char : character.character.Character
        The character whose information you wish to display.
    """
    try:
        char_info = get_char_info(char)
    except:
        raise IncompleteCharacterException("Character object attributes are either not formatted correctly or missing.")

    ST_proficiencies = ""
    if char.game_class.saving_throws.STR:
        ST_proficiencies += "STR, "
    if char.game_class.saving_throws.DEX:
        ST_proficiencies += "DEX, "
    if char.game_class.saving_throws.CON:
        ST_proficiencies += "CON, "
    if char.game_class.saving_throws.INT:
        ST_proficiencies += "INT, "
    if char.game_class.saving_throws.WIS:
        ST_proficiencies += "WIS, "
    if char.game_class.saving_throws.CHA:
        ST_proficiencies += "CHA, "
    ST_proficiencies = ST_proficiencies[:-2]

    print(f'Name:\t\t\t\t{char_info["CharacterName"]}')
    print(f'Class:\t\t\t\t{char_info["ClassLevel"]}')
    print(f'Race:\t\t\t\t{char_info["Race"]}')
    print(f'Background:\t\t\t{char_info["Background"]}\n')

    print(f'Strength:\t\t\t{char_info["STR"]} ({char_info["STRmod"]})')
    print(f'Dexterity:\t\t\t{char_info["DEX"]} ({char_info["DEXmod"]})')
    print(f'Constitution:\t\t\t{char_info["CON"]} ({char_info["CONmod"]})')
    print(f'Intelligence:\t\t\t{char_info["INT"]} ({char_info["INTmod"]})')
    print(f'Wisdom:\t\t\t\t{char_info["WIS"]} ({char_info["WISmod"]})')
    print(f'Charisma:\t\t\t{char_info["CHA"]} ({char_info["CHamod"]})\n')

    print(f'Proficiency Bonus:\t\t{char_info["ProfBonus"]}')
    print(f"Saving Throw Proficiencies:\t{ST_proficiencies}")
    print(f'Skill Proficiencies:\t\t{", ".join(char.get_skills())}\n')

    print(f'Passive Perception:\t\t{char_info["Passive"]}')
    print(f'AC:\t\t\t\t{char_info["AC"]}')
    print(f'Initiative:\t\t\t{char_info["Initiative"]}')
    print(f'Speed:\t\t\t\t{char_info["Speed"]}')
    print(f'Hit Dice:\t\t\t{char_info["HDTotal"]}\n')

    print(f'Personality Trait:\t\t{char_info["PersonalityTraits"]}')
    print(f'Ideals:\t\t\t\t{char_info["Ideals"]}')
    print(f'Bonds:\t\t\t\t{char_info["Bonds"]}')
    print(f'Flaws:\t\t\t\t{char_info["Flaws"]}')


def save_to_pdf(char, flatten=False, destination=None):
    """
    Creates a pdf character sheet called charSheet_published.pdf
    from the passed in character object, populating all relevent fields.

    Parameters
    ----------
    char : character.character.Character
        The character to generate a pdf character sheet for.

    flatten : bool, optional
        If true, removes form-fillable boxes on output pdf,
        by default False
    """
    char_info = get_char_info(char)
    cs_pdf = pdfrw.PdfReader(
        __file__.replace("character_sheet.py", "charSheet_template.pdf")
    )
    annotations = cs_pdf.pages[0]["/Annots"]
    for annotation in annotations:
        if annotation["/Subtype"] == "/Widget":
            if annotation["/T"]:
                key = annotation["/T"][1:-1].strip()
                if key in char_info:
                    if "Check Box" in key and char_info[key]:
                        annotation.update(pdfrw.PdfDict(AS="Yes"))
                    else:
                        annotation.update(pdfrw.PdfDict(V=str(char_info[key]), AP=""))
                if flatten:
                    annotation.update(pdfrw.PdfDict(Ff=1))

    if not destination:
        destination = getcwd() + "\\"

    if destination[-4:] != ".pdf":
        if destination[-1] != "\\":
            destination += "\\"
        destination += f"{char_info['CharacterName'].strip()}.pdf".replace(" ", "_")

    pdfrw.PdfWriter().write(destination, cs_pdf)


# for testing
if __name__ == "__main__":
    save_to_pdf(character.Character(race="Elf", gameClass="Druid"), flatten=True)
    display(character.Character(race="Elf", gameClass="Druid"))
