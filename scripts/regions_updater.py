# This script is for updating state regions after a game update
import os
import csv

# The format of the file
# The file path

# Region Tag,ID Number,Homelands,Subsistence Building,City,Port,Farm,Mine,Wood,Arable Land,Provinces,Traits,Arable Resources,Caped Resources,Naval Exit
OLD_MOD_REGIONS_DATA_PATH = os.path.join('mod', 'data', 'old_state_regions.csv')
# Region Tag,ID Number,Subsistence Building,City,Port,Farm,Mine,Wood,Arable Land,Provinces,Traits,Arable Resources,Caped Resources,Naval Exit,Prime Land
NEW_GAME_REGIONS_DATA_PATH = os.path.join('game', 'data', 'state_regions.csv')
# Region Tag,ID Number,Homelands,Subsistence Building,City,Port,Farm,Mine,Wood,Arable Land,Provinces,Traits,Arable Resources,Caped Resources,Naval Exit, Prime Land
NEW_MOD_REGIONS_DATA_PATH = os.path.join('mod', 'data', 'state_regions.csv')

MOD_REGION_TAG_COLUMN = 0
MOD_REGION_ID_COLUMN = 1
MOD_REGION_HOMELANDS_COLUMN = 2
MOD_REGION_SUBSISTENCE_BUILDING_COLUMN = 3
MOD_REGION_CITY_COLUMN = 4
MOD_REGION_PORT_COLUMN = 5
MOD_REGION_FARM_COLUMN = 6
MOD_REGION_MINE_COLUMN = 7
MOD_REGION_WOOD_COLUMN = 8
MOD_REGION_ARABLE_LAND_COLUMN = 9
MOD_REGION_PROVINCES_COLUMN = 10
MOD_REGION_TRAITS_COLUMN = 11
MOD_REGION_ARABLE_RESOURCES_COLUMN = 12
MOD_REGION_CAPED_RESOURCES_COLUMN = 13
MOD_REGION_NAVAL_EXIT_COLUMN = 14
MOD_REGION_PRIME_LAND_COLUMN = 15

GAME_REGION_TAG_COLUMN = 0
GAME_REGION_ID_COLUMN = 1
GAME_REGION_SUBSISTENCE_BUILDING_COLUMN = 2
GAME_REGION_CITY_COLUMN = 3
GAME_REGION_PORT_COLUMN = 4
GAME_REGION_FARM_COLUMN = 5
GAME_REGION_MINE_COLUMN = 6
GAME_REGION_WOOD_COLUMN = 7
GAME_REGION_ARABLE_LAND_COLUMN = 8
GAME_REGION_PROVINCES_COLUMN = 9
GAME_REGION_TRAITS_COLUMN = 10
GAME_REGION_ARABLE_RESOURCES_COLUMN = 11
GAME_REGION_CAPED_RESOURCES_COLUMN = 12
GAME_REGION_NAVAL_EXIT_COLUMN = 13
GAME_REGION_PRIME_LAND_COLUMN = 14

def split_provinces(provinces: str) -> set[str]:
    """
    Take a string of space separated province IDs and return a set of strings
    with the 'x' prefix and the ID in uppercase.

    :param provinces: A string of space separated province IDs
    :return: A set of strings with the 'x' prefix and the ID in uppercase
    """
    return {'x' + province[1:].upper() for province in provinces.split()}

# First iterate through the old mod regions
old_mod_regions = {} # region_tag -> region data
old_mod_provinces = {} # province -> region_tag
with open(OLD_MOD_REGIONS_DATA_PATH, 'r') as file:
    file.readline() # Skip first line
    reader = csv.reader(file)
    for line in reader:
        region_tag = line[MOD_REGION_TAG_COLUMN]
        provinces = split_provinces(line[MOD_REGION_PROVINCES_COLUMN])
        old_mod_regions[region_tag] = line
        old_mod_regions[region_tag][MOD_REGION_PROVINCES_COLUMN] = provinces # Correct the provinces
        for province in provinces:
            old_mod_provinces[province] = region_tag

# Then iterate through the new game regions
new_game_regions = {}
new_game_provinces = {}
with open(NEW_GAME_REGIONS_DATA_PATH, 'r') as file:
    file.readline() # Skip first line
    reader = csv.reader(file)
    for line in reader:
        region_tag = line[GAME_REGION_TAG_COLUMN]
        provinces = split_provinces(line[GAME_REGION_PROVINCES_COLUMN])
        new_game_regions[region_tag] = line
        new_game_regions[region_tag][GAME_REGION_PROVINCES_COLUMN] = provinces
        for province in provinces:
            new_game_provinces[province] = region_tag

# Then combine
new_regions = {}
removed_regions = {}
modified_regions = {}
for region_tag, region_data in new_game_regions.items():
    provinces = region_data[GAME_REGION_PROVINCES_COLUMN]
    if region_tag not in old_mod_regions:
        new_regions[region_tag] = set()
    elif provinces != old_mod_regions[region_tag][MOD_REGION_PROVINCES_COLUMN]:
        modified_regions[region_tag] = set()

for region_tag in old_mod_regions.keys():
    if region_tag not in new_game_regions:
        removed_regions[region_tag] = set()

print(f'New regions: {new_regions}')
print(f'Removed regions: {removed_regions}')
print(f'Modified regions: {modified_regions}')
print(new_game_provinces.keys() - old_mod_provinces.keys())

for province, new_game_region in new_game_provinces.items():
    old_mod_region = old_mod_provinces[province]
    if old_mod_region in removed_regions.keys():
        removed_regions[old_mod_region].add(new_game_region)
    if old_mod_region in modified_regions.keys():
        modified_regions[old_mod_region].add(new_game_region)
print('\nDeleted:')
for removed_region, new_regions in removed_regions.items():
    print(f'Split region {removed_region} into:')
    for new_region in new_regions:
        print(f'  {new_region}')
print('\nModified:')
for modified_region, new_regions in modified_regions.items():
    print(f'Split region {modified_region} into:')
    for new_region in new_regions:
        print(f'  {new_region}')


# with open(NEW_MOD_REGIONS_DATA_PATH, 'w', newline='') as regions_file:
#     writer = csv.writer(regions_file, quoting=csv.QUOTE_ALL)
#     for line in lines:
#         writer.writerow(line)