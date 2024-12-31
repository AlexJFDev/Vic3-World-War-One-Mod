import countries_generator
import cultures_generator
import laws_generator
import states_generator
import buildings_generator
import characters_generator
import military_generator

from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os

CURRENT_DIRECTORY = os.path.dirname(__file__)
PARENT_DIRECTORY = os.path.split(CURRENT_DIRECTORY)[0]

MOD_PATH = os.path.join(PARENT_DIRECTORY, 'mod', 'World-War-One')
COMMON_PATH = os.path.join(MOD_PATH, 'common')
HISTORY_PATH = os.path.join(COMMON_PATH, 'history')

COMBINED_CULTURES_PATH = os.path.join(COMMON_PATH, 'cultures', 'combined_cultures.txt')
COUNTRIES_PATH = os.path.join(COMMON_PATH, 'country_definitions', 'countries.txt')
DOMESTIC_LAWS_PATH = os.path.join(HISTORY_PATH, 'countries', 'domestic_laws.txt')
STATES_PATH = os.path.join(HISTORY_PATH, 'states', 'states.txt')
POPS_PATH = os.path.join(HISTORY_PATH, 'pops', 'pops.txt')
BUILDINGS_PATH = os.path.join(HISTORY_PATH, 'buildings', 'buildings.txt')
REGIONS_PATH = os.path.join(MOD_PATH, 'map_data', 'state_regions', 'state_regions.txt')
CHARACTER_MOD_FILE_PATH = os.path.join(HISTORY_PATH, 'characters', 'generated_characters.txt')
MILITARY_FORMATIONS_OUT_PATH = os.path.join(HISTORY_PATH, 'military_formations', 'military_formations.txt')
CULTURE_STANDARD_OF_LIVING_PATH = os.path.join(COMMON_PATH, 'static_modifiers', 'culture_standard_of_living.txt')

COUNTRY_DEFINITIONS_PATH = os.path.join('mod', 'data', 'country_definitions.csv')
COUNTRY_LAWS_PATH = os.path.join('mod', 'data', 'country_laws.csv')
COUNTRY_INSTITUTIONS_PATH = os.path.join('mod', 'data', 'country_institutions.csv')
CULTURES_PATH = os.path.join('mod', 'data', 'cultures.csv')
STATE_OWNERSHIP_PATH = os.path.join('mod', 'data', 'state_ownership.csv')
STATE_REGIONS_PATH = os.path.join('mod', 'data', 'state_regions.csv')
BUILDINGS_DATA_PATH = os.path.join('mod', 'data', 'state_buildings.csv')
CHARACTER_DATA_PATH = os.path.join('mod', 'data', 'character_definitions.csv')
MILITARY_DATA_PATH = os.path.join('mod', 'data', 'military_units.csv')

def write_object(path: str, clausewitzObject: ClausewitzObject):
    with open(path, 'w', encoding='utf-8-sig') as file:
        file.write(clausewitzObject.unparse())

if __name__ == '__main__':
    countries_root = countries_generator.generate_countries(COUNTRY_DEFINITIONS_PATH)
    cultures_root = cultures_generator.generate_cultures(CULTURES_PATH)
    culture_soi_root = cultures_generator.generate_standard_of_living(CULTURES_PATH)
    laws_root = laws_generator.generate_laws(COUNTRY_LAWS_PATH, COUNTRY_INSTITUTIONS_PATH)
    states_root, pops_root = states_generator.generate_states_and_pops(STATE_OWNERSHIP_PATH, STATE_REGIONS_PATH)
    buildings_root = buildings_generator.generate_buildings(BUILDINGS_DATA_PATH)
    #regions_root = states_generator.generate_regions(STATE_REGIONS_PATH)
    characters_root = characters_generator.generate_characters(CHARACTER_DATA_PATH)
    military_root = military_generator.generate_military_object(MILITARY_DATA_PATH)

    write_object(COMBINED_CULTURES_PATH, cultures_root)
    write_object(CULTURE_STANDARD_OF_LIVING_PATH, culture_soi_root)
    write_object(COUNTRIES_PATH, countries_root)
    write_object(DOMESTIC_LAWS_PATH, laws_root)
    write_object(STATES_PATH, states_root)
    write_object(POPS_PATH, pops_root)
    write_object(BUILDINGS_PATH, buildings_root)
    #write_object(REGIONS_PATH, regions_root)
    write_object(CHARACTER_MOD_FILE_PATH, characters_root)
    write_object(MILITARY_FORMATIONS_OUT_PATH, military_root)