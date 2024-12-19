import os
import csv

import clausewitz_parser
from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

STATE_REGIONS_PATH = os.path.join('game', 'files', 'map_data', 'state_regions')
STATE_REGION_FILE_NAMES = [
    '00_west_europe.txt',
    '01_south_europe.txt',
    '02_east_europe.txt',
    '03_north_africa.txt',
    '04_subsaharan_africa.txt',
    '05_north_america.txt',
    '06_central_america.txt',
    '07_south_america.txt',
    '08_middle_east.txt',
    '09_central_asia.txt',
    '10_india.txt',
    '11_east_asia.txt',
    '12_indonesia.txt',
    '13_australasia.txt',
    '14_siberia.txt',
    '15_russia.txt',
    '99_seas.txt',
]
STATE_REGION_PATHS = [os.path.join(STATE_REGIONS_PATH, file_name) for file_name in STATE_REGION_FILE_NAMES]

STATE_REGIONS_CSV_PATH = os.path.join('game', 'data', 'state_regions.csv')

EMPTY_OBJECT = ClausewitzObject()

def unparse_regions_file(file_path: str):
    state_regions = {}
    regions_root = clausewitz_parser.parse_path(file_path)
    state_region_names = regions_root.get_names()
    for state_region_name in state_region_names:
        state_region: ClausewitzObject = regions_root.get_value_named(state_region_name)
        id_number = state_region.get_value_named('id') # Id is a reserved keyword
        subsistence_building = state_region.get_value_named('subsistence_building', default='').replace('"', '')
        city = state_region.get_value_named('city', default='').replace('"', '')
        port = state_region.get_value_named('port', default='').replace('"', '')
        farm = state_region.get_value_named('farm', default='').replace('"', '')
        mine = state_region.get_value_named('mine', default='').replace('"', '')
        wood = state_region.get_value_named('wood', default='').replace('"', '')
        arable_land = state_region.get_value_named('arable_land', default='').replace('"', '')
        provinces = state_region.get_value_named('provinces', default=EMPTY_OBJECT).get_anonymous_values()
        traits = state_region.get_value_named('traits', default=EMPTY_OBJECT).get_anonymous_values()
        arable_resources = state_region.get_value_named('arable_resources', default=EMPTY_OBJECT).get_anonymous_values()
        capped_resources = state_region.get_value_named('capped_resources', default=EMPTY_OBJECT).get_name_value_pairs()
        undiscovered_resources = [resource.get_name_value_pairs() for resource in state_region.get_values_named('resource', default=[])]
        naval_exit_id = state_region.get_value_named('naval_exit_id', default='').replace('"', '')
        prime_land = state_region.get_value_named('prime_land', default=EMPTY_OBJECT).get_anonymous_values()
        state_regions[state_region_name] = {
            'id': id_number,
            'subsistence_building': subsistence_building,
            'city': city,
            'port': port,
            'farm': farm,
            'mine': mine,
            'wood': wood,
            'arable_land': arable_land,
            'provinces': provinces,
            'traits': traits,
            'arable_resources': arable_resources,
            'capped_resources': capped_resources,
            'undiscovered_resources': undiscovered_resources,
            'naval_exit_id': naval_exit_id,
            'prime_land': prime_land
        }
    return state_regions

def save_regions(regions: dict):
    with open(STATE_REGIONS_CSV_PATH, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Region Tag', 'ID Number', 'Subsistence Building', 'City', 'Port', 'Farm', 'Mine', 'Wood', 'Arable Land', 'Provinces', 'Traits', 'Arable Resources', 'Caped Resources', 'Naval Exit', 'Prime Land'])
        for state_name, region_data in regions.items():
            id = region_data['id']
            subsistence_building = region_data['subsistence_building']
            city = region_data['city']
            port = region_data['port']
            farm = region_data['farm']
            mine = region_data['mine']
            wood = region_data['wood']
            arable_land = region_data['arable_land']
            
            provinces = ' '.join(region_data['provinces']).replace('"', '')
            traits = ' '.join(region_data['traits']).replace('"', '')
            arable_resources = ' '.join(region_data['arable_resources']).replace('"', '')

            capped_resources: dict[str: list[str]] = region_data['capped_resources']
            for resource in region_data['undiscovered_resources']:
                resource_type = resource.get('type', [''])[0].replace('"', '')
                depleted_type = resource.get('depleted_type', [''])[0].replace('"', '')
                undiscovered_amount = int(resource.get('undiscovered_amount', ['0'])[0].replace('"', ''))
                discovered_amount = int(resource.get('discovered_amount', ['0'])[0].replace('"', ''))

                if depleted_type != '':
                    capped_amount = int(capped_resources.get(depleted_type, ['0'])[0].replace('"', ''))
                    total_amount = undiscovered_amount + discovered_amount + capped_amount
                    capped_resources[depleted_type] = [str(total_amount)]
                else:
                    capped_resources[resource_type] = [str(undiscovered_amount + discovered_amount)]
            capped_resources = [f'{resource}={amount[0]}' for resource, amount in capped_resources.items()]
            capped_resources = ' '.join(capped_resources)

            naval_exit_id = region_data['naval_exit_id']

            prime_land = ' '.join(region_data['prime_land']).replace('"', '')

            writer.writerow([state_name, id, subsistence_building, city, port, farm, mine, wood, arable_land, provinces, traits, arable_resources, capped_resources, naval_exit_id, prime_land])


if __name__ == '__main__':
    regions = {}
    for path in STATE_REGION_PATHS:
        regions.update(unparse_regions_file(path))
    save_regions(regions)