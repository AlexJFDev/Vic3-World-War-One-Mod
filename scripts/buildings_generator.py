from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os
import csv

PRODUCTION_METHODS_PATH = os.path.join('game', 'data', 'production_methods.csv')

BUILDINGS_CSV_PATH = os.path.join('mod', 'data', 'state_buildings.csv')
BUILDINGS_OUT_PATH = os.path.join('mod', 'files', 'buildings.txt')

STATE_TAG_COLUMN = 0
REGION_NAME_COLUMN = 1
OWNER_NAME_COLUMN = 2
OWNER_TAG_COLUMN = 3
BUILDINGS_START_COLUMN = 4 # Update column number in generate_region_object if changed

BUILDING_TYPE_INDEX = 0
BUILDING_LEVEL_INDEX = 1
BUILDING_PRODUCTION_METHOD_INDEX = 2
BUILDING_OWNER_TYPE_INDEX = 3
BUILDING_OWNER_INDEX = 4

SKIP_URBAN_CENTERS = True

# Global variables for line and column to track errors
line_number = 1
column_number = 1

def fetch_production_methods(file_path: str):
    with open(file_path, 'r') as production_methods_file:
        production_methods_reader = csv.reader(production_methods_file)
        production_methods = {}
        for line in production_methods_reader:
            production_methods[line[0]] = set(line[1:])
        return production_methods
    
production_methods_map = fetch_production_methods(PRODUCTION_METHODS_PATH)
building_types = production_methods_map.keys()

def generate_region_object(country_tag: str, state_tag: str, buildings: list[tuple[str, str, str, str, str]]):
    global line_number
    global column_number

    column_number = 5 # Buildings start at column 5

    region_object = ClausewitzObject()
    for building in buildings:
        building_object = ClausewitzObject()
        building_type = building[BUILDING_TYPE_INDEX]
        building_level = building[BUILDING_LEVEL_INDEX]
        production_methods = set(building[BUILDING_PRODUCTION_METHOD_INDEX].strip().split(' '))
        owner_type = building[BUILDING_OWNER_TYPE_INDEX]
        owner = building[BUILDING_OWNER_INDEX]
        
        if (building_type == 'building_urban_center' and SKIP_URBAN_CENTERS) or building_type == '':
            column_number += 5 # Data per building is 5 columns wide
            continue

        if building_type not in building_types:
            raise ValueError(f'type', building_type)
        if not production_methods.issubset(production_methods_map[building_type]):
            raise ValueError(f'production', building_type, production_methods.difference(production_methods_map[building_type]))

        ownership_object = ClausewitzObject()
        if owner_type == 'country':
            ownership_object.add_named_value('country', ClausewitzObject())
            ownership_object.get_value_named('country').add_named_value('country', f'c:{owner}')
            ownership_object.get_value_named('country').add_named_value('levels', building_level)
        elif owner_type == '':
            ownership_object.add_named_value('country', ClausewitzObject())
            ownership_object.get_value_named('country').add_named_value('country', f'c:{country_tag}')
            ownership_object.get_value_named('country').add_named_value('levels', building_level)
        elif owner_type == 'local':
            ownership_object.add_named_value('building', ClausewitzObject())
            ownership_object.get_value_named('building').add_named_value('type', building_type)
            ownership_object.get_value_named('building').add_named_value('country', f'c:{country_tag}')
            ownership_object.get_value_named('building').add_named_value('levels', building_level)
            ownership_object.get_value_named('building').add_named_value('region', state_tag.split(':')[1])
        else:
            owner_region, owner_country = owner.split('.')
            ownership_object.add_named_value('building', ClausewitzObject())
            ownership_object.get_value_named('building').add_named_value('type', owner_type)
            ownership_object.get_value_named('building').add_named_value('country', f'c:{owner_country}')
            ownership_object.get_value_named('building').add_named_value('levels', building_level)
            ownership_object.get_value_named('building').add_named_value('region', owner_region)

        building_object.add_named_value('building', building_type)
        building_object.add_named_value('add_ownership', ownership_object)
        building_object.add_named_value('reserves', '1')
        building_object.add_named_value('activate_production_methods', ClausewitzObject(anonymous_values=production_methods))
        region_object.add_named_value('create_building', building_object)
        
        column_number += 5 # Data per building is 5 columns wide
    return region_object

def generate_buildings(file_path: str):
    global line_number
    global column_number

    if SKIP_URBAN_CENTERS:
        print('Skipping Urban Centers')
    buildings_root = ClausewitzRoot()
    buildings_object = ClausewitzObject()
    buildings_root.add_named_value('BUILDINGS', buildings_object)

    with open(file_path, 'r') as buildings_file:
        buildings_file.readline()
        line_number += 1 # Skip header
        buildings_reader = csv.reader(buildings_file)
        for line in buildings_reader:
            state_tag = line[STATE_TAG_COLUMN]
            owner_tag = line[OWNER_TAG_COLUMN]
            raw_buildings = line[BUILDINGS_START_COLUMN:]
            buildings = []
            for i in range(0, len(raw_buildings), 5):
                building_type = raw_buildings[i]
                building_quantity = raw_buildings[i+1]
                production_method = raw_buildings[i+2]
                if i + 3 >= len(raw_buildings):
                    owner_type = ''
                    owner = ''
                else:
                    owner_type = raw_buildings[i+3]
                    owner = raw_buildings[i+4]
                
                buildings.append((building_type, building_quantity, production_method, owner_type, owner))

            state_object = buildings_object.get_value_named(state_tag)
            if state_object is None:
                state_object = ClausewitzObject()
                buildings_object.add_named_value(state_tag, state_object)
            try:
                region_object = generate_region_object(owner_tag, state_tag, buildings)
                state_object.add_named_value(f'region_state:{owner_tag}', region_object)
            except ValueError as e:
                if e.args[0] == 'type':
                    print(f'Error in cell {number_to_alphabet(column_number)}{line_number}: Unknown building type: {e.args[1]}')
                elif e.args[0] == 'production':
                    print(f'Error in cell {number_to_alphabet(column_number)}{line_number}: Unknown production method {e.args[2]} for type {e.args[1]}')
                else:
                    print(f'Unknown error in cell {number_to_alphabet(column_number)}{line_number}: {e.args[0]}')
                i = input('Press enter to continue or type "q" to quit')
                if i == 'q':
                    exit()
            line_number += 1
            
            
    return buildings_root

def number_to_alphabet(num): # Thanks ChatGPT
    result = ""
    while num > 0:
        num -= 1  # Adjust for 0-based index
        result = chr(num % 26 + ord('A')) + result
        num //= 26
    return result

if __name__ == '__main__':
    buildings_root = generate_buildings(BUILDINGS_CSV_PATH)
    with open(BUILDINGS_OUT_PATH, 'w') as output_file:
        output_file.write(buildings_root.unparse())
    print('Done')