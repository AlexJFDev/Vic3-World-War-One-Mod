from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os
import csv

OWNERSHIP_FILE: str = os.path.join('data', 'state_ownership.csv')
REGIONS_FILE: str = os.path.join('data', 'state_regions.csv')

STATES_FILE: str = os.path.join('clausewitz_files', 'states.txt')
POPS_FILE: str = os.path.join('clausewitz_files', 'pops.txt')

OWNERSHIP_REGION_TAG_COLUMN = 0
OWNERSHIP_COUNTRY_TAG_COLUMN = 3
OWNERSHIP_PROVINCES_COLUMN = 4
OWNERSHIP_POPS_COLUMN = 5
REGIONS_STATE_TAG_COLUMN = 1
REGIONS_HOMELANDS_COLUMN = 2

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

states_root = ClausewitzRoot()
states_root.add_named_value('STATES', ClausewitzObject())
pops_root = ClausewitzRoot()
pops_root.add_named_value('POPS', ClausewitzObject())

states: ClausewitzObject = states_root.get_named_value('STATES')
pops: ClausewitzObject = pops_root.get_named_value('POPS')

with open(OWNERSHIP_FILE, 'r') as ownership_file:
    ownership_file.readline() # Skip the first line
    ownership_reader = csv.reader(ownership_file)
    for number, line in enumerate(ownership_reader):
        try:
            region_tag: str = line[OWNERSHIP_REGION_TAG_COLUMN]
            owner_tag: str = line[OWNERSHIP_COUNTRY_TAG_COLUMN]
            provinces: str = line[OWNERSHIP_PROVINCES_COLUMN].split(' ')
            pop_data: str = line[OWNERSHIP_POPS_COLUMN]

            if pop_data != '':
                pop: ClausewitzObject = pops.get_named_value(region_tag)
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

            state: ClausewitzObject = states.get_named_value(region_tag)
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

with open(REGIONS_FILE, 'r') as file:
    file.readline() # Skip the first line
    reader = csv.reader(file)
    for line in reader:
        region_tag: str = line[REGIONS_STATE_TAG_COLUMN]
        homelands = line[REGIONS_HOMELANDS_COLUMN].split(' ')
        state: ClausewitzObject = states.get_named_value(region_tag)
            
        for homeland in homelands:
            if homeland == '':
                continue
            state.add_named_value('add_homeland', homeland)


with open(STATES_FILE, 'w') as file:
    file.write(states_root.unparse())

with open(POPS_FILE, 'w') as file:
    file.write(pops_root.unparse())

print('Success!')