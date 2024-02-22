import os
import csv

import clausewitz_parser
from clausewitz_object import ClausewitzObject

FILE_PATH = os.path.join('data', 'combined_cultures.txt')
CSV_PATH = os.path.join('data', 'cultures.csv')

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


if __name__ == '__main__':
    file_as_object = clausewitz_parser.parse_file(FILE_PATH)

    with open(CSV_PATH, 'wt', newline='') as file:
        csv_writer = csv.writer(file)

        tag: str
        culture: ClausewitzObject
        for tag, culture in file_as_object.get_name_values().items():
            culture_object: ClausewitzObject = culture[0]
            row = [None] * 14

            row[TAG_COLUMN] = tag

            colors = culture_object.get_named_value('color').get_anonymous_values()
            row[COLOR_COLUMN] = ' '.join(colors)

            row[RELIGION_COLUMN] = culture_object.get_named_value('religion')

            traits = culture_object.get_named_value('traits').get_anonymous_values()
            row[TRAITS_COLUMN] = ' '.join(traits)

            obsessions = culture_object.get_named_value('obsessions')
            if obsessions is not None:
                row[OBSESSIONS_COLUMN] = ' '.join(obsessions.get_anonymous_values())

            male_common_names = culture_object.get_named_value('male_common_first_names').get_anonymous_values()
            row[MALE_COMMON_NAMES] = ' '.join(set(sorted(male_common_names)))

            female_common_names = culture_object.get_named_value('female_common_first_names').get_anonymous_values()
            row[FEMALE_COMMON_NAMES] = ' '.join(set(sorted(female_common_names)))

            common_last_names = culture_object.get_named_value('common_last_names').get_anonymous_values()
            row[COMMON_LAST_NAMES] = ' '.join(set(sorted(common_last_names)))

            male_regal_names = culture_object.get_named_value('male_regal_first_names')
            if male_regal_names is not None:
                row[MALE_REGAL_NAMES] = ' '.join(set(sorted(male_regal_names.get_anonymous_values())))
            
            female_regal_names = culture_object.get_named_value('female_regal_first_names')
            if female_regal_names is not None:
                row[FEMALE_REGAL_NAMES] = ' '.join(set(sorted(female_regal_names.get_anonymous_values())))
            
            noble_last_names = culture_object.get_named_value('noble_last_names').get_anonymous_values()
            row[NOBLE_LAST_NAMES] = ' '.join(set(sorted(noble_last_names)))

            ethnicities = ''
            for rate, ethnicity in culture_object.get_named_value('ethnicities').get_name_values().items():
                ethnicities = f'{ethnicities}{rate}={ethnicity[0]};'
            row[ETHNICITIES] = ethnicities

            row[GRAPHICS] = culture_object.get_named_value('graphics')

            csv_writer.writerow(row)