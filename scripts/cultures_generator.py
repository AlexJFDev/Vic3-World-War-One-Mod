from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os
import csv

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