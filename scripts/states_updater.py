import os
import csv

OLD_STATE_OWNERSHIP_DATA_PATH = os.path.join('mod', 'data', 'old_state_ownership.csv')
NEW_STATE_REGION_DATA_PATH = os.path.join('game', 'data', 'state_regions.csv')
STATE_OWNERSHIP_DATA_PATH = os.path.join('mod', 'data', 'state_ownership.csv')

OWNERSHIP_REGION_TAG_COLUMN = 0
OWNERSHIP_STATE_NAME_COLUMN = 1
OWNERSHIP_OWNER_NAME_COLUMN = 2
OWNERSHIP_OWNER_TAG_COLUMN = 3
OWNERSHIP_PROVINCES_COLUMN = 4
OWNERSHIP_POPS_COLUMN = 5
OWNERSHIP_INCORPORATION_COLUMN = 6

STATE_REGIONS_TAG_COLUMN = 0
STATE_REGIONS_ID_COLUMN = 1
STATE_REGIONS_PROVINCES_COLUMN = 9

# Provinces are the smallest geographic unit
# State Regions are a set of provinces
# States have owners and are a subset of a region. States also include pop and building data.

def fix_province_id(province: str) -> str:
    return f'x{province[1:].upper()}'

old_states = {}
old_provinces = {}
with open(OLD_STATE_OWNERSHIP_DATA_PATH, 'r') as old_ownership_file:
    old_ownership_file.readline()
    old_ownership_reader = csv.reader(old_ownership_file)
    for row in old_ownership_reader:
        region_tag = row[OWNERSHIP_REGION_TAG_COLUMN].replace('s:', '').replace('ï»¿', '')
        state_name = row[OWNERSHIP_STATE_NAME_COLUMN]
        owner_name = row[OWNERSHIP_OWNER_NAME_COLUMN]
        owner_tag = row[OWNERSHIP_OWNER_TAG_COLUMN]
        provinces = set(map(fix_province_id, row[OWNERSHIP_PROVINCES_COLUMN].split(' ')))
        pop_data = row[OWNERSHIP_POPS_COLUMN]
        incorporation = row[OWNERSHIP_INCORPORATION_COLUMN]

        state = old_states.get(region_tag, {})
        state[owner_tag] = (state_name, owner_name, provinces, pop_data, incorporation)

        old_states[region_tag] = state

        for province in provinces:
            old_provinces[province] = (region_tag, owner_tag)

new_regions = set()
new_provinces = {}
with open(NEW_STATE_REGION_DATA_PATH, 'r') as new_region_file:
    new_region_reader = csv.reader(new_region_file)
    for row in new_region_reader:
        region_tag = row[STATE_REGIONS_TAG_COLUMN].replace('ï»¿', '')
        region_id = int(row[STATE_REGIONS_ID_COLUMN])
        provinces = set(map(fix_province_id, row[STATE_REGIONS_PROVINCES_COLUMN].split(' ')))
        if region_id >= 3000: # Ocean region
            continue
        new_regions.add(region_tag)
        for province in provinces:
            new_provinces[province] = region_tag

new_states = {}
for province, (old_region_tag, owner_tag) in old_provinces.items():
    new_region_tag = new_provinces[province]
    old_region_data = old_states[old_region_tag]
    old_state_data = old_region_data[owner_tag]
    combo_tag = f's:{new_region_tag}-{owner_tag}'
    
    if old_region_tag in new_regions:
        # We have data for the state
        state_name, owner_name, provinces, pop_data, incorporation = old_state_data
        new_state = new_states.get(combo_tag, {
            'state_name' : state_name,
            'owner_name' : owner_name,
            'provinces' : set(),
            'pop_data' : pop_data,
            'incorporation' : incorporation
        })
        new_state['provinces'].add(province)
        new_states[combo_tag] = new_state
    else:
        new_state = new_states.get(combo_tag, {
            'state_name' : '',
            'owner_name' : '',
            'provinces' : set(),
            'pop_data' : '',
            'incorporation' : ''
        })
        new_state['provinces'].add(province)
        new_states[combo_tag] = new_state

lines = []
for combo_tag, data in new_states.items():
    region_tag, owner_tag = combo_tag.split('-')
    state_name = data['state_name']
    owner_name = data['owner_name']
    provinces = ' '.join(sorted(data['provinces']))
    pop_data = data['pop_data']
    incorporation = data['incorporation']
    lines.append([region_tag, state_name, owner_name, owner_tag, provinces, pop_data, incorporation])

lines.sort(key=lambda line: (line[3], line[0]))

lines.insert(0, ['State Region Tag','State Name','Owner','Owner Tag','Provinces','Pops','Incorporated'])

with open(STATE_OWNERSHIP_DATA_PATH, 'w', newline='') as state_ownership_file:
    writer = csv.writer(state_ownership_file, quoting=csv.QUOTE_ALL)
    for line in lines:
        writer.writerow(line)
