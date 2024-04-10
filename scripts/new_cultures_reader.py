import clausewitz_parser
from clausewitz_object import ClausewitzObject
from clausewitz_root import ClausewitzRoot

import os
import csv

CULTURES_PATH = os.path.join('game', 'files', '00_cultures.txt')
ADDITIONAL_CULTURES_PATH = os.path.join('game', 'files', '00_additional_cultures.txt')

DATA_PATH = os.path.join('game', 'data', 'cultures.csv')

cultures_object: ClausewitzRoot = clausewitz_parser.parse_file(CULTURES_PATH)
additional_cultures_object: ClausewitzRoot = clausewitz_parser.parse_file(ADDITIONAL_CULTURES_PATH)

with open(DATA_PATH, 'w') as data_file:
    data_writer = csv.writer(data_file)
    cultures = cultures_object.get_names()
    for culture in cultures:
        culture_object: ClausewitzObject = cultures_object.get_named_value(culture)
        color = None
        religion = culture_object.get_named_value('religion')
        traits = culture_object.get_named_value('traits').get_anonymous_values()
        obsessions = culture_object.get_named_value('obsessions').get_anonymous_values()
        male_common_first_names = culture_object.get_named_value('male_common_first_names').get_anonymous_values()
        female_common_first_names = culture_object.get_named_value('female_common_first_names').get_anonymous_values()
        common_last_names = culture_object.get_named_value('common_last_names').get_anonymous_values()
        male_regal_first_names = culture_object.get_named_value('male_regal_first_names').get_anonymous_values()
        female_regal_first_names = culture_object.get_named_value('female_regal_first_names').get_anonymous_values()
        noble_last_names = culture_object.get_named_value('noble_last_names').get_anonymous_values()

    print(cultures)
