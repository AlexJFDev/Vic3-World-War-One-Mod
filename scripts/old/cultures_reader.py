import os
import csv

import clausewitz_parser
from clausewitz_object import ClausewitzObject

FILE_PATH = os.path.join('mod', 'data', 'combined_cultures.txt')
CSV_PATH = os.path.join('mod', 'data', 'cultures.csv')

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
    file_as_object = clausewitz_parser.parse_path(FILE_PATH)

    with open(CSV_PATH, 'wt', newline='') as file:
        csv_writer = csv.writer(file)

        tag: str
        culture: ClausewitzObject
        for tag, culture in file_as_object.get_name_value_pairs().items():
            culture_object: ClausewitzObject = culture[0]
            row = [None] * 14

            colors = culture_object.get_value_named('color').get_anonymous_values()
            traits = culture_object.get_value_named('traits').get_anonymous_values()
            obsessions = culture_object.get_value_named('obsessions')
            male_common_names = culture_object.get_value_named('male_common_first_names').get_anonymous_values()
            female_common_names = culture_object.get_value_named('female_common_first_names').get_anonymous_values()
            common_last_names = culture_object.get_value_named('common_last_names').get_anonymous_values()
            male_regal_names = culture_object.get_value_named('male_regal_first_names')
            female_regal_names = culture_object.get_value_named('female_regal_first_names')
            noble_last_names = culture_object.get_value_named('noble_last_names').get_anonymous_values()
            ethnicities = ''
            for rate, ethnicity in culture_object.get_value_named('ethnicities').get_name_value_pairs().items():
                ethnicities = f'{ethnicities}{rate}={ethnicity[0]};'

            row[TAG_COLUMN] = tag
            row[COLOR_COLUMN] = ' '.join(colors)
            row[RELIGION_COLUMN] = culture_object.get_value_named('religion')
            row[TRAITS_COLUMN] = ' '.join(traits)
            if obsessions is not None:
                row[OBSESSIONS_COLUMN] = ' '.join(obsessions.get_anonymous_values())
            row[MALE_COMMON_NAMES] = ' '.join(set(sorted(male_common_names)))
            row[FEMALE_COMMON_NAMES] = ' '.join(set(sorted(female_common_names)))
            row[COMMON_LAST_NAMES] = ' '.join(set(sorted(common_last_names)))
            if male_regal_names is not None:
                row[MALE_REGAL_NAMES] = ' '.join(set(sorted(male_regal_names.get_anonymous_values())))
            if female_regal_names is not None:
                row[FEMALE_REGAL_NAMES] = ' '.join(set(sorted(female_regal_names.get_anonymous_values())))
            row[ETHNICITIES] = ethnicities
            row[GRAPHICS] = culture_object.get_value_named('graphics')

            csv_writer.writerow(row)