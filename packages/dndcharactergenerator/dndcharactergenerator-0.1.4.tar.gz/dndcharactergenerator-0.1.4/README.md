# DATA533proj_dndCharGen [![Build Status](https://app.travis-ci.com/gavingro/DATA533proj3_dndCharGen.svg?token=JXMpGYnCxxPqFxVwgEV5&branch=main)](https://app.travis-ci.com/gavingro/DATA533proj3_dndCharGen)

## Intent

A program to generate random but reasonable dungeons and dragons player characters from information in the players handbook.

A user can input desired race, stats, class, or background names in order to generate the character around those attributes.

Includes functionality to display relevent information to the terminal, and to fill out a pdf character sheet with information from a character object.

---

## Example
*As found in `example.py`.*

``` {python}
# example.py

>>from character.character import Character
>>from character.character_idea import display as ci_display
>>from character.character_sheet import display as cs_display
>>from character.character_sheet import save_to_pdf
>>from generator.background import Background
>>from generator.gameclass import GameClass
>>from generator.race import Race
>>from generator.stats import Stats

# Generate and display a random character
>>mychar = Character()
>>ci_display(mychar)
You are Seipora Basha, a DAMARAN PATH OF THE BERSERKER BARBARIAN.
You are STRONG, kind of WISE, quite SMART, quite CHARISMATIC, and kind of HEALTHY.

>>print('-----------------------------------------------------------')
-----------------------------------------------------------

>>cs_display(mychar)
Name:				Seipora Basha
Class:				Path of the Berserker Barbarian
Race:				Damaran
Background:			Acolyte

Strength:			16 (3)
Dexterity:			11 (0)
Constitution:			13 (1)
Intelligence:			15 (2)
Wisdom:				13 (1)
Charisma:			14 (2)

Proficiency Bonus:		2
Saving Throw Proficiencies:	STR, CON
Skill Proficiencies:		Animal Handling, Perception, Insight, Religion

Passive Perception:		11
AC:				11
Initiative:			0
Speed:				30
Hit Dice:			d12

Personality Trait:		I idolize a particular hero of my faith, and constantly
Ideals:				Aspiration. I seek to prove myself worthy of my god's favor by matching my actions against his or her teachings. (Any)
Bonds:				I would die to recover an ancient relic of my faith that
Flaws:				I judge others harshly, and myself even more severely.

# Generate a custom character
>>base_stats = Stats(STR = 15, DEX = 3, CON = 20, INT = 10, WIS = 8, CHA = 7)
>>game_class = GameClass('Barbarian', auto_generate=True)
>>race = Race('Dwarf', auto_generate=True)
>>background = Background('Acolyte', auto_generate=True)

>>mychar = Character(base_stats, game_class, race, background, auto_generate=False)
>>save_to_pdf(mychar, flatten=True)

# output saved to character/charSheet_published.pdf
```

---

## Filetree
* *readme.md*
* *test.py*
* example.py

**genarator**/
* gamedata/
    * background_data.py
    * gameclass_data.py
    * race_data.py
* stats.py
* gameclass.py
* race.py
* background.py	


**character**/
* character.py
* character_idea.py
* character_sheet.py
* charSheet_template.pdf

---
## Generator Function Details
*Refer to docstrings within code for additional details on function parameters.*
### RpgGenerator
- *The virtual Generator Class to be overridden by child classes with generating capabilities. NOT INTENDED TO BE INSTANTIATED.*

*RpgGenerator.generate()*
- *The virtual function to randomly populate the attributes of an object that is inherited from the generator class.*

*RpgGenerator.roll_3d6_drop_lowest()*
- Rolls 4d6, and returns the sum of the top 3 dice.

### Stats
 - A class to represent the character's D&D stats.

*Stats.generate()*
 - Populates the Stats objects with random stats according to roll_3d6_drop_lowest().  

*Stats.maximize_for_stats(other_stats)*
 - Rolls for stats, populates stat values based on preferences inidcated in other_stats.  

*Stats.generate_from_gameclass(gameclass)*
 - Rolls for stats, prioritizes based on D&D class preferences.  

*Stats.generate_from_race(race)*
 - Rolls for stats, prioritizes based on D&D race preferences.  

### GameClass
 - A class to represent the character's D&D class.  

*GameClass.generate(class_name = None)*
 - Populates empty GameClass attributes based on existing parameters.  

*GameClass.generate_from_stats(stats)*
 - Selects the best D&D Class based on given stats values.  

*GameClass.generate_from_race(race)*
 - Selects the best D&D Class based on given race.  

### Race
 - A class to represent the character's D&D race.

*Race.generate(race_name = None)*
 - Populates empty Race attributes based on existing parameters.  

*Race.generate_from_stats(stats)*
 - Selects the best D&D Race based on given stats values.  

*Race.generate_from_gameclass(gameclass)*
 - Selects the best D&D Race based on given D&D Class.  

### Background
 - A class to represent a character's background.

*generate(background_name = None)*
 - Generates a random background from the D&D background based on the passed in name.  

---
## Character Function Details

### Character
- *A class to represent a D&D Character.*

*Character.generate()*

- Generates the missing information about a D&D character based on the information the character currently has.

*Character.get_stats()*

 - Returns the sum of a characters rolled base stats and the stats modifier from it's race.

*Character.get_base_AC()*

- Calculates and returns the base Armor Class of the object.

*Character.get_skills()*

- Combines together and returns a list made up of the skill proficiencies from a characters gameclass and it's background.
### Charater Idea

*a_or_an(noun)*

- Returns "a" or "an" based on which word would naturally occur before the passed in noun.

*stat_descriptor(stat, mod)*

- Returns a common-language string describing the magnitude and description of the passed in D&D stat and stat modifier.

*display(char)*

-  Prints out fundamental information about the passed in character object, including the character's name, race, class, and stats
    
### Character Sheet

*get_char_info(char)*

- Populates and returns a dictionary of information about the passed in character. Each key corresponds to a single field on the form-fillable pdf character sheet, while each value corresponds to that fields information held in the character object.

*display(char)*

- Prints detailed information about the passed in character object to represent what would be seen on thir character sheet.

*save_to_pdf(char, flatten=False)*

- Creates a pdf character sheet called charSheet_published.pdf from the passed in character object, populating all relevent fields.