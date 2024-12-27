# This script is for updating state regions after a game update
import os
import csv

# The format of the file
# The file path
# Region Tag,ID Number,Homelands,Subsistence Building,City,Port,Farm,Mine,Wood,Arable Land,Provinces,Traits,Arable Resources,Caped Resources,Naval Exit
OLD_MOD_REGIONS_DATA_PATH = os.path.join('mod', 'data', 'old_state_regions.csv')
# Region Tag,ID Number,Subsistence Building,City,Port,Farm,Mine,Wood,Arable Land,Provinces,Traits,Arable Resources,Caped Resources,Naval Exit,Prime Land
NEW_GAME_REGIONS_DATA_PATH = os.path.join('game', 'data', 'state_regions.csv')
# Region Tag,ID Number,Homelands,Subsistence Building,City,Port,Farm,Mine,Wood,Arable Land,Provinces,Traits,Arable Resources,Caped Resources,Naval Exit,Prime Land
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

def split_traits(traits: str) -> set[str]:
    """
    Takes a space delimited string and returns a set of strings.

    :param traits: A string of space separated traits
    :return: A set of strings
    """
    return set(traits.split())

def update_regions(old_mod_regions_path, new_game_regions_path) -> dict[str, list]:
    # First iterate through the old mod regions
    """
    IMPORTANT: THIS FUNCTION WAS MADE FOR THE 1.7 TO 1.8 TRANSITION. IT WILL NEED TO BE UPDATED FOR THE 1.8 TO 1.9 TRANSITION.\n

    This function takes two paths to CSV files containing region data and returns a combined version of the data. 
    The first file is the old mod regions, and the second is the new game regions. 
    The function first reads in the old mod regions and the new game regions, storing them in dictionaries. 
    It then combines the two dictionaries, giving precedence to the new game regions. 
    If a state existed previously, then the function keeps the homelands, arable resources, and caped resources from the old mod regions.\n

    The old mod regions CSV file should have the following format:\n
    Region Tag,ID Number,Homelands,Subsistence Building,City,Port,Farm,Mine,Wood,Arable Land,Provinces,Traits,Arable Resources,Caped Resources,Naval Exit\n

    The new game regions CSV file should have the following format:\n
    Region Tag,ID Number,Subsistence Building,City,Port,Farm,Mine,Wood,Arable Land,Provinces,Traits,Arable Resources,Caped Resources,Naval Exit,Prime Land\n

    The dictionary returned uses a region tag string as the key and a list of strings as the value. The list is ordered as follows:\n
    Region Tag,ID Number,Homelands,Subsistence Building,City,Port,Farm,Mine,Wood,Arable Land,Provinces(a set of province IDs),Traits,Arable Resources,Caped Resources,Naval Exit,Prime Land

    :param old_mod_regions_path: The path to the old mod regions CSV file
    :param new_game_regions_path: The path to the new game regions CSV file
    :return: A dictionary, region_tag -> region data, of the combined region data
    """
    old_mod_regions = {} # region_tag -> region data
    old_mod_provinces = {} # province -> region_tag
    with open(old_mod_regions_path, 'r') as file:
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
    with open(new_game_regions_path, 'r') as file:
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
    combined_mod_regions = {}
    for region_tag, region_data in new_game_regions.items():
        region_data.insert(MOD_REGION_HOMELANDS_COLUMN, '')
        if region_tag in old_mod_regions: # If the state existed previously then keep the homelands, arable resources, and caped resources
            region_data[MOD_REGION_HOMELANDS_COLUMN] = old_mod_regions[region_tag][MOD_REGION_HOMELANDS_COLUMN]
            region_data[MOD_REGION_ARABLE_RESOURCES_COLUMN] = old_mod_regions[region_tag][MOD_REGION_ARABLE_RESOURCES_COLUMN]
            region_data[MOD_REGION_CAPED_RESOURCES_COLUMN] = old_mod_regions[region_tag][MOD_REGION_CAPED_RESOURCES_COLUMN]
        combined_mod_regions[region_tag] = region_data

    return combined_mod_regions

if __name__ == '__main__':
    combined_mod_regions = update_regions(OLD_MOD_REGIONS_DATA_PATH, NEW_GAME_REGIONS_DATA_PATH)
    with open(NEW_MOD_REGIONS_DATA_PATH, 'w', newline='') as regions_file:
        regions_file.write('Region Tag,ID Number,Homelands,Subsistence Building,City,Port,Farm,Mine,Wood,Arable Land,Provinces,Traits,Arable Resources,Caped Resources,Naval Exit,Prime Land\n')
        writer = csv.writer(regions_file)
        for region_tag, region_data in combined_mod_regions.items():
            region_data[MOD_REGION_PROVINCES_COLUMN] = ' '.join(region_data[MOD_REGION_PROVINCES_COLUMN])
            writer.writerow(region_data)