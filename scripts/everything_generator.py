import countries_generator
import cultures_generator
import laws_generator
import states_generator
import buildings_generator

from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os

COMBINED_CULTURES_PATH = os.path.join('mod_files', 'combined_cultures.txt')
COUNTRIES_PATH = os.path.join('mod_files', 'countries.txt')
DOMESTIC_LAWS_PATH = os.path.join('mod_files', 'domestic_laws.txt')
STATES_PATH = os.path.join('mod_files', 'states.txt')
POPS_PATH = os.path.join('mod_files', 'pops.txt')
BUILDINGS_PATH = os.path.join('mod_files', 'buildings.txt')

COUNTRY_DEFINITIONS_PATH = os.path.join('data', 'country_definitions.csv')
COUNTRY_LAWS_PATH = os.path.join('data', 'country_laws.csv')
COUNTRY_INSTITUTIONS_PATH = os.path.join('data', 'country_institutions.csv')
CULTURES_PATH = os.path.join('data', 'cultures.csv')
STATE_OWNERSHIP_PATH = os.path.join('data', 'state_ownership.csv')
STATE_REGIONS_PATH = os.path.join('data', 'state_regions.csv')
BUILDINGS_DATA_PATH = os.path.join('data', 'state_buildings.csv')

def write_object(path: str, clausewitzObject: ClausewitzObject):
    with open(path, 'w') as file:
        file.write(clausewitzObject.unparse())

if __name__ == '__main__':
    countries_root = countries_generator.generate_countries(COUNTRY_DEFINITIONS_PATH)
    cultures_root = cultures_generator.generate_cultures(CULTURES_PATH)
    laws_root = laws_generator.generate_laws(COUNTRY_LAWS_PATH, COUNTRY_INSTITUTIONS_PATH)
    states_root, pops_root = states_generator.generate_states_and_pops(STATE_OWNERSHIP_PATH, STATE_REGIONS_PATH)
    buildings_root = buildings_generator.generate_buildings(BUILDINGS_DATA_PATH)

    write_object(COMBINED_CULTURES_PATH, cultures_root)
    write_object(COUNTRIES_PATH, countries_root)
    write_object(DOMESTIC_LAWS_PATH, laws_root)
    write_object(STATES_PATH, states_root)
    write_object(POPS_PATH, pops_root)
    write_object(BUILDINGS_PATH, buildings_root)