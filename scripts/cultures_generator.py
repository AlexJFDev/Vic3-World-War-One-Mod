from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os
import csv

CULTURE_DEFINITIONS = os.path.join('data', 'cultures.csv')
CULTURES_FILE = os.path.join('mod_files', 'combined_cultures.txt')

NAME_COLUMN = 0
TAG_COLUMN = 1
COLOR_COLUMN = 2
RELIGION_COLUMN = 3
TRAITS_COLUMN = 4
OBSESSIONS_COLUMN = 5
MALE_COMMON_NAMES = 6
FEMALE_COMMON_NAMES = 7
COMMON_LAST_NAMES = 8
MALE_REGAL_NAMES = 9
FEMALE_REGAL_NAMES = 10
NOBLE_LAST_NAMES = 11
ETHNICITIES = 12
GRAPHICS = 13

cultures_root = ClausewitzRoot()

with open(CULTURE_DEFINITIONS, 'rt') as culture_definitions:
    culture_definitions.readline() # Skip header line
    definitions_reader = csv.reader(culture_definitions)
    for name, tag, color, religion, traits, obsessions, male_common_names, female_common_names, common_last_names, male_regal_names, female_regal_names, noble_last_names, ethnicities, graphics in definitions_reader:
        culture_object = ClausewitzObject()

        if name == '': continue

        color_object = ClausewitzObject() # Color
        for component in color.split(' '):
            color_object.add_anonymous_value(component)
        traits_object = ClausewitzObject() # Traits
        for trait in traits.split(' '):
            traits_object.add_anonymous_value(trait)
        obsessions_object = ClausewitzObject() #Obsessions
        for obsession in obsessions.split(' '):
            obsessions_object.add_anonymous_value(obsession)

        male_common_names_object = ClausewitzObject() # Male Common First Names
        for name in male_common_names.split(' '):
            male_common_names_object.add_anonymous_value(name)
        female_common_names_object = ClausewitzObject() # Female Common First Names
        for name in female_common_names.split(' '):
            female_common_names_object.add_anonymous_value(name)
        common_last_names_object = ClausewitzObject() # Common Last Names
        for name in common_last_names.split(' '):
            common_last_names_object.add_anonymous_value(name)
        male_regal_names_object = ClausewitzObject() # Male Regal First Names
        for name in male_regal_names.split(' '):
            male_regal_names_object.add_anonymous_value(name)
        female_regal_names_object = ClausewitzObject() # Female Regal First Names
        for name in female_regal_names.split(' '):
            female_regal_names_object.add_anonymous_value(name)
        noble_last_names_object = ClausewitzObject() # Noble Last Names
        for name in noble_last_names.split(' '):
            noble_last_names_object.add_anonymous_value(name)
        
        has_obsession = len(obsessions) > 0
        has_male_regal = len(male_regal_names) > 0
        has_female_regal = len(female_regal_names) > 0

        ethnicities_object = ClausewitzObject()
        for ethnicity in ethnicities.split(';'):
            if ethnicity == '': continue
            rate, name = ethnicity.replace(' ', '').split('=')
            ethnicities_object.add_named_value(rate, name)

        culture_object.add_named_value('color', color_object)
        culture_object.add_named_value('religion', religion)
        culture_object.add_named_value('traits', traits_object)
        if has_obsession:
            culture_object.add_named_value('obsessions', obsessions_object)
        culture_object.add_named_value('male_common_first_names', male_common_names_object)
        culture_object.add_named_value('female_common_first_names', female_common_names_object)
        culture_object.add_named_value('common_last_names', common_last_names_object)
        if has_male_regal:
            culture_object.add_named_value('male_regal_first_names', male_regal_names_object)
        if has_female_regal:
            culture_object.add_named_value('female_regal_first_names', female_regal_names_object)
        culture_object.add_named_value('noble_last_names', noble_last_names_object)
        culture_object.add_named_value('ethnicities', ethnicities_object)
        culture_object.add_named_value('graphics', graphics)
        
        cultures_root.add_named_value(tag, culture_object)

with open(CULTURES_FILE, 'w') as file:
    file.write(cultures_root.unparse())