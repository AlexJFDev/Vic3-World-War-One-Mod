from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os
import csv

CULTURE_DEFINITIONS = os.path.join('mod', 'data', 'cultures.csv')
CULTURES_FILE = os.path.join('mod', 'files', 'combined_cultures.txt')

NAME_COLUMN = 0
TAG_COLUMN = 1
COLOR_COLUMN = 2
RELIGION_COLUMN = 3
TRAITS_COLUMN = 4
OBSESSIONS_COLUMN = 5
MALE_COMMON_NAMES_COLUMN = 6
FEMALE_COMMON_NAMES_COLUMN = 7
COMMON_LAST_NAMES_COLUMN = 8
MALE_REGAL_NAMES_COLUMN = 9
FEMALE_REGAL_NAMES_COLUMN = 10
NOBLE_LAST_NAMES_COLUMN = 11
ETHNICITIES_COLUMN = 12
GRAPHICS_COLUMN = 13

def generate_cultures(file_path: str):
    cultures_root = ClausewitzRoot()

    with open(file_path, 'rt') as culture_definitions:
        culture_definitions.readline() # Skip header line
        definitions_reader = csv.reader(culture_definitions)
        for line_number, line in enumerate(definitions_reader):
            try:
                name = line[NAME_COLUMN]
                tag = line[TAG_COLUMN]
                color = line[COLOR_COLUMN]
                religion = line[RELIGION_COLUMN]
                traits = line[TRAITS_COLUMN]
                obsessions = line[OBSESSIONS_COLUMN]
                male_common_names = line[MALE_COMMON_NAMES_COLUMN]
                female_common_names = line[FEMALE_COMMON_NAMES_COLUMN]
                common_last_names = line[COMMON_LAST_NAMES_COLUMN]
                male_regal_names = line[MALE_REGAL_NAMES_COLUMN]
                female_regal_names = line[FEMALE_REGAL_NAMES_COLUMN]
                noble_last_names = line[NOBLE_LAST_NAMES_COLUMN]
                ethnicities = line[ETHNICITIES_COLUMN]
                graphics = line[GRAPHICS_COLUMN]
                
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
            except Exception as e:
                print(f'Error on line {line_number}: {e}')
    return cultures_root

if __name__ == '__main__':
    cultures_root = generate_cultures(CULTURE_DEFINITIONS)
    with open(CULTURES_FILE, 'w') as file:
        file.write(cultures_root.unparse())