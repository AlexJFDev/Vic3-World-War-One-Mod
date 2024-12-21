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

# First iterate through the old mod regions
old_mod_regions = {}
with open(OLD_MOD_REGIONS_DATA_PATH, 'r') as file:
    file.readline() # Skip first line
    reader = csv.reader(file)
    for line in reader:
        pass

# Then iterate through the new game regions
new_game_regions = {}
with open(NEW_GAME_REGIONS_DATA_PATH, 'r') as file:
    file.readline() # Skip first line
    reader = csv.reader(file)
    for line in reader:
        pass

# with open(NEW_MOD_REGIONS_DATA_PATH, 'w', newline='') as regions_file:
#     writer = csv.writer(regions_file, quoting=csv.QUOTE_ALL)
#     for line in lines:
#         writer.writerow(line)