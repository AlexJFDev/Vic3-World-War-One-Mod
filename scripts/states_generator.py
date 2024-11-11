from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os
import csv

OWNERSHIP_FILE: str = os.path.join('mod', 'data', 'state_ownership.csv')
REGION_DATA_FILE: str = os.path.join('mod', 'data', 'state_regions.csv')

STATES_FILE: str = os.path.join('mod', 'files', 'states.txt')
POPS_FILE: str = os.path.join('mod', 'files', 'pops.txt')
REGIONS_FILE: str = os.path.join('mod', 'files', 'state_regions.txt')

OWNERSHIP_REGION_TAG_COLUMN = 0
OWNERSHIP_COUNTRY_TAG_COLUMN = 3
OWNERSHIP_PROVINCES_COLUMN = 4
OWNERSHIP_POPS_COLUMN = 5

REGIONS_REGION_TAG_COLUMN = 0
REGIONS_ID_COLUMN = 1
REGIONS_HOMELANDS_COLUMN = 2
REGIONS_SUBSISTENCE_BUILDING_COLUMN = 3
REGIONS_CITY_COLUMN = 4
REGIONS_PORT_COLUMN = 5
REGIONS_FARM_COLUMN = 6
REGIONS_MINE_COLUMN = 7
REGIONS_WOOD_COLUMN = 8
REGIONS_ARABLE_LAND_COLUMN = 9
REGIONS_PROVINCES_COLUMN = 10
REGIONS_TRAITS_COLUMN = 11
REGIONS_ARABLE_RESOURCES_COLUMN = 12
REGIONS_CAPPED_RESOURCES_COLUMN = 13
REGIONS_NAVAL_EXIT_COLUMN = 14

ENCODING = 'utf-8-sig'

def split_pops(pops: str) -> list[str]:
    groups = pops.split(',')
    pop_list = []
    for group in groups:
        size, traits = group.split(':')
        traits = traits.split(';')
        new_traits = [['size', size]]
        for trait in traits:
            trait_name, value = trait.split('=')
            new_traits.append([trait_name, value])
        pop_list.append(new_traits)
    return pop_list

def generate_states_and_pops(ownership_path: str, regions_path: str):
    states_root = ClausewitzRoot()
    states_root.add_named_value('STATES', ClausewitzObject())
    pops_root = ClausewitzRoot()
    pops_root.add_named_value('POPS', ClausewitzObject())

    states: ClausewitzObject = states_root.get_value_named('STATES')
    pops: ClausewitzObject = pops_root.get_value_named('POPS')

    with open(ownership_path, 'r') as ownership_file:
        ownership_file.readline() # Skip the first line
        ownership_reader = csv.reader(ownership_file)
        for number, line in enumerate(ownership_reader):
            try:
                region_tag: str = line[OWNERSHIP_REGION_TAG_COLUMN]
                owner_tag: str = line[OWNERSHIP_COUNTRY_TAG_COLUMN]
                provinces: str = line[OWNERSHIP_PROVINCES_COLUMN].split(' ')
                pop_data: str = line[OWNERSHIP_POPS_COLUMN]

                if pop_data != '':
                    pop: ClausewitzObject = pops.get_value_named(region_tag)
                    if pop is None:
                        pop = ClausewitzObject()
                        pops.add_named_value(region_tag, pop)
                    state_pops = ClausewitzObject()
                    pop.add_named_value(f'region_state:{owner_tag[2:]}', state_pops)
                    pop_groups = split_pops(pop_data)
                    for pop_group in pop_groups:
                        create_pop = ClausewitzObject()
                        state_pops.add_named_value('create_pop', create_pop)
                        for trait, value in pop_group:
                            create_pop.add_named_value(trait, value)

                state: ClausewitzObject = states.get_value_named(region_tag)
                if state is None:
                    state = ClausewitzObject()
                    states.add_named_value(region_tag, state)
                state.add_named_value('create_state', ClausewitzObject(name_values={
                    'owned_provinces': [ClausewitzObject(anonymous_values=provinces)],
                    'country': [owner_tag]
                }))
            except Exception as error:
                print(f'Error on line {number + 2} of the file.\n----------------------------------')
                print(error)
                quit()

    # This iterates over the pop data per entire state. It calculates the total number of pops in a state and the total number per culture in a state.
    # States that have more than 10% of their total population in a culture are considered homelands for that culture.
    for region_tag, state_data in pops.get_name_value_pairs().items():
        state_size = 0
        culture_sizes = {}
        homelands = []

        state_regions:list[list[ClausewitzObject]] = state_data[0].get_name_value_pairs().values()
        for state_region in state_regions:
            create_pops: ClausewitzObject = state_region[0].get_values_named('create_pop')
            for create_pop in create_pops:
                size = int(create_pop.get_value_named('size'))
                culture = create_pop.get_value_named('culture')

                state_size += size
                culture_sizes[culture] = culture_sizes.get(culture, 0) + size

        for culture, size in culture_sizes.items():
            if size > state_size / 10:
                homelands.append(f'cu:{culture}')

        state_object = states.get_value_named(region_tag)
        if state_object is None:
            continue
        for homeland in homelands:
            if homeland == '':
                continue
            state_object.add_named_value('add_homeland', homeland)

    return states_root, pops_root

def generate_regions(regions_path: str):
    regions_root = ClausewitzRoot()
    with open(regions_path, 'r') as regions_file:
        regions_file.readline() # Skip the first line

        reader = csv.reader(regions_file)
        for line_num, line in enumerate(reader, 2):
            region_tag: str = line[REGIONS_REGION_TAG_COLUMN]
            region_id = line[REGIONS_ID_COLUMN]
            subsistence_building_type = line[REGIONS_SUBSISTENCE_BUILDING_COLUMN]
            city_province = line[REGIONS_CITY_COLUMN]
            port_province = line[REGIONS_PORT_COLUMN]
            farm_province = line[REGIONS_FARM_COLUMN]
            mine_province = line[REGIONS_MINE_COLUMN]
            wood_province = line[REGIONS_WOOD_COLUMN]
            arable_land = line[REGIONS_ARABLE_LAND_COLUMN]
            provinces = line[REGIONS_PROVINCES_COLUMN].split(' ')
            traits = line[REGIONS_TRAITS_COLUMN].split(' ')
            arable_resources = line[REGIONS_ARABLE_RESOURCES_COLUMN].split(' ')
            capped_resources = line[REGIONS_CAPPED_RESOURCES_COLUMN].split(' ')
            naval_exit = line[REGIONS_NAVAL_EXIT_COLUMN]

            region_object = ClausewitzObject()
            region_object.add_named_value('id', region_id)
            region_object.add_named_value('provinces', ClausewitzObject(anonymous_values=provinces))
            if (subsistence_building_type != ''):
                region_object.add_named_value('subsistence_building', subsistence_building_type)
            if (city_province != ''):
                region_object.add_named_value('city', city_province)
            if (port_province != ''):
                region_object.add_named_value('port', port_province)
            if (farm_province != ''):
                region_object.add_named_value('farm', farm_province)
            if (mine_province != ''):
                region_object.add_named_value('mine', mine_province)
            if (wood_province != ''):
                region_object.add_named_value('wood', wood_province)
            if (arable_land != ''):
                region_object.add_named_value('arable_land', arable_land)
            if (traits[0] != ''):
                region_object.add_named_value('traits', ClausewitzObject(anonymous_values=traits))
            if (arable_resources[0] != ''):
                region_object.add_named_value('arable_resources', ClausewitzObject(anonymous_values=arable_resources))
            if (capped_resources[0] != ''):
                capped_resources_object = ClausewitzObject()
                for capped_resource in capped_resources:
                    resource, quantity = capped_resource.split('=')
                    capped_resources_object.add_named_value(resource, quantity)
                region_object.add_named_value('capped_resources', capped_resources_object)
            if (naval_exit != ''):
                region_object.add_named_value('naval_exit_id', naval_exit)

            regions_root.add_named_value(region_tag, region_object)
    return regions_root

if __name__ == '__main__':
    states_root, pops_root = generate_states_and_pops(OWNERSHIP_FILE, REGION_DATA_FILE)
    regions_root = generate_regions(REGION_DATA_FILE)
    with open(STATES_FILE, 'w', encoding=ENCODING) as file:
        file.write(states_root.unparse())

    with open(POPS_FILE, 'w', encoding=ENCODING) as file:
        file.write(pops_root.unparse())

    with open(REGIONS_FILE, 'w', encoding=ENCODING) as file:
        file.write(regions_root.unparse())
    
    print('Success!')