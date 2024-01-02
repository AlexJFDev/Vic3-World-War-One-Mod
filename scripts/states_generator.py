from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os
import csv

OWNERSHIP_FILE: str = os.path.join('data', 'state_ownership.csv')
REGIONS_FILE: str = os.path.join('data', 'state_regions.csv')

OUTPUT_FILE: str = os.path.join('data', '00_states.txt')

OWNERSHIP_REGION_TAG_COLUMN = 2
OWNERSHIP_COUNTRY_TAG_COLUMN = 3
OWNERSHIP_PROVINCES_COLUMN = 4
REGIONS_STATE_TAG_COLUMN = 1
REGIONS_HOMLANDS_COLUMN = 2

root = ClausewitzRoot()
root.add_named_value('STATES', ClausewitzObject())

states: ClausewitzObject = root.get_named_value('STATES')

with open(OWNERSHIP_FILE, 'r') as file:
    file.readline() # Skip the first line
    reader = csv.reader(file)
    for line in reader:
        region_tag: str = line[OWNERSHIP_REGION_TAG_COLUMN]
        owner_tag: str = line[OWNERSHIP_COUNTRY_TAG_COLUMN]
        provinces: str = line[OWNERSHIP_PROVINCES_COLUMN]
        state: ClausewitzObject = states.get_named_value(region_tag)
        if state is None:
            state = ClausewitzObject()
            states.add_named_value(region_tag, state)
        state.add_named_value('create_state', ClausewitzObject(name_values={
            'owned_provinces': [ClausewitzObject(anonymous_values=provinces.split(' '))],
            'country': [owner_tag]
        }))


with open(OUTPUT_FILE, 'w') as file:
    file.write(root.unparse())
