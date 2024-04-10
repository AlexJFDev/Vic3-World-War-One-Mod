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
    print(cultures)