from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os
import csv

BUILDINGS_CSV_PATH = os.path.join('data', 'state_buildings.csv')
BUILDINGS_OUT_PATH = os.path.join('mod_files', 'buildings.txt')

REGION_TAG_COLUMN = 0
REGION_NAME_COLUMN = 1
OWNER_NAME_COLUMN = 2
OWNER_TAG_COLUMN = 3

def generate_buildings(file_path: str):
    buildings_root = ClausewitzRoot()

    with open(file_path, 'r') as buildings_file:
        buildings_file.readline()
        buildings_reader = csv.reader(buildings_file)
        for line in buildings_reader:
            region_tag = line[REGION_TAG_COLUMN]
            owner_tag = line[OWNER_TAG_COLUMN]

            