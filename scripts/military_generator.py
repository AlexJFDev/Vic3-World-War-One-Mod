from clausewitz_object import ClausewitzObject
from clausewitz_root import ClausewitzRoot

import os
import csv
import math

MILITARY_CSV_PATH = os.path.join('mod', 'data', 'military_units.csv')
MILITARY_OUT_PATH = os.path.join('mod', 'files', 'military_formations.txt')

OWNER_TAG_COLUMN = 0
FORMATION_NAME_COLUMN = 1
TYPE_COLUMN = 2
HQ_REGION_COLUMN = 3
COMMANDER_COLUMN = 4
UNITS_START_COLUMN = 5

TYPE_INDEX = 0
STATES_INDEX = 1
SIZE_INDEX = 2

def generate_military_object(path):
    military_root = ClausewitzRoot()
    military_formations = ClausewitzObject()
    military_root.add_named_value('MILITARY_FORMATIONS', military_formations)
    with open(path) as file:
        reader = csv.reader(file)
        next(reader) # skip header
        for row in reader:
            owner_tag = row[OWNER_TAG_COLUMN]
            formation_name = row[FORMATION_NAME_COLUMN]
            formation_type = row[TYPE_COLUMN]
            hq_region = row[HQ_REGION_COLUMN]
            commander = row[COMMANDER_COLUMN]

            formation = ClausewitzObject()
            if formation_name != '':
                formation.add_named_value('name', formation_name)
            formation.add_named_value('type', formation_type)
            formation.add_named_value('hq_region', hq_region)

            raw_units: list[str] = row[UNITS_START_COLUMN:]
            units = [
                (raw_units[i], raw_units[i+1], raw_units[i+2]) 
                for i in range(0, len(raw_units), 3) 
                if raw_units[i] != '' and raw_units[i+1] != '' and raw_units[i+2] != ''
            ]

            for unit in units:
                unit_type = unit[TYPE_INDEX]
                unit_states = unit[STATES_INDEX].split(';')
                unit_size = math.ceil(int(unit[SIZE_INDEX]) / len(unit_states))

                for unit_state in unit_states:
                    combat_unit = ClausewitzObject()
                    combat_unit.add_named_value('type', f'unit_type:{unit_type}')
                    combat_unit.add_named_value('state_region', f's:{unit_state}')
                    combat_unit.add_named_value('count', unit_size)
                    formation.add_named_value('combat_unit', combat_unit)

            military = military_formations.get_value_named(owner_tag)
            if military is None:
                military = ClausewitzObject()
                military_formations.add_named_value(owner_tag, military)
            military.add_named_value('create_military_formation', formation)
    
    return military_root

if __name__ == '__main__':
    military_root = generate_military_object(MILITARY_CSV_PATH)
    with open(MILITARY_OUT_PATH, 'w') as output_file:
        output_file.write(military_root.unparse())