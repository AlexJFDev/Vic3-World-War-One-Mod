import clausewitz_parser
from clausewitz_object import ClausewitzObject
from clausewitz_root import ClausewitzRoot

import os
import csv
import re

CHARACTER_DATA_PATH = os.path.join('mod', 'data', 'character_definitions.csv')

CHARACTER_MOD_FILE_PATH = os.path.join('mod', 'files', 'generated_characters.txt')
CHARACTER_MOD_FILE_NAME = 'generated characters.txt'

INTEREST_GROUPS = {
    'ig_armed_forces', 'ig_devout', 'ig_industrialists', 'ig_intelligentsia', 'ig_landowners', 'ig_petty_bourgeoisie', 'ig_rural_folk', 'ig_trade_unions'
}
TRAITS = {
    'expert_political_operator', 'cruel', 'wrathful', 'political_appointee', 'direct', 'cocaine_addiction', 'celebrity_commander', 'surveyor', 'basic_naval_commander', 'senile', 'literary', 
    'hedonist', 'master_bureaucrat', 'romantic', 'experienced_convoy_raider', 'expert_naval_commander', 'scarred', 'syphilis', 'bigoted', 'basic_diplomat', 'mountain_commander', 
    'basic_colonial_administrator', 'honorable', 'innovative', 'experienced_artillery_commander', 'trench_rat', 'cautious', 'masterful_diplomat', 'expert_artillery_commander', 
    'brave', 'pious', 'experienced_diplomat', 'experienced_offensive_planner', 'cancer', 'expensive_tastes', 'ambitious', 'expert_defensive_strategist', 'erudite', 'inspirational_orator', 
    'persistent', 'reckless', 'engineer', 'experienced_naval_commander', 'pillager', 'bandit', 'basic_political_operator', 'war_criminal', 'defense_in_depth_specialist', 'sickly', 'kidney_stones', 
    'forest_commander', 'tactful', 'expert_convoy_raider', 'experienced_defensive_strategist', 'firebrand', 'beetle_ear', 'dockyard_master', 'expert_colonial_administrator', 'expert_offensive_planner', 
    'imposing', 'explorer', 'imperious', 'alcoholic', 'grifter', 'reserved', 'convoy_raider_commander', 'basic_offensive_planner', 'arrogant', 'trait_child', 'demagogue', 'stalwart_defender', 
    'meticulous', 'basic_artillery_commander', 'popular_commander', 'psychological_affliction', 'wounded', 'resupply_commander', 'experienced_political_operator', 'experienced_colonial_administrator', 
    'plains_commander', 'charismatic', 'traditionalist_commander', 'opium_addiction', 'shellshocked', 'basic_defensive_strategist'
}
IDEOLOGIES = {
    'ideology_moderate', 'ideology_traditionalist', 'ideology_atheist', 'ideology_republican_leader', 'ideology_radical', 'ideology_abolitionist', 'ideology_slaver', 'ideology_feminist', 'ideology_reformer', 
    'ideology_pacifist', 'ideology_jingoist_leader', 'ideology_royalist', 'ideology_social_democrat', 'ideology_communist', 'ideology_vanguardist', 'ideology_fascist', 'ideology_anarchist', 'ideology_ethno_nationalist', 
    'ideology_theocrat', 'ideology_market_liberal', 'ideology_liberal_leader', 'ideology_republican_paternalistic', 'ideology_scholar_paternalistic', 'ideology_junker_paternalistic', 'ideology_papal_paternalistic', 
    'ideology_confucian', 'ideology_bakufu', 'ideology_shinto_moralist', 'ideology_caudillismo', 'ideology_heavenly_kingdom_theocratic', 'ideology_papal_moralist', 'ideology_liberal_modern', 'ideology_egalitarian_modern', 
    'ideology_luddite', 'ideology_jacksonian_democrat', 'ideology_authoritarian', 'ideology_socialist', 'ideology_humanitarian', 'ideology_protectionist', 'ideology_humanitarian_royalist', 'ideology_positivist', 
    'ideology_corporatist_leader', 'ideology_land_reformer', 'ideology_integralist',
    # Mod Ideologies
    'ideology_rooseveltian_progressivism', 'ideology_wilsonian_progressivism'
}

YES_VALUES = {
    'ruler', 'ig_leader', 'historical', 'female', 'noble', 'is_admiral', 'is_general', 'is_agitator', 'heir'
}

FULL_NAME_COLUMN = 0
FIRST_NAME_COLUMN = 1
LAST_NAME_COLUMN = 2
COUNTRY_TAG_COLUMN = 3
CULTURE_COLUMN = 4
INTEREST_GROUP_COLUMN = 5
IDEOLOGY_COLUMN = 6
YES_VALUES_COLUMN = 7
BIRTH_DATE_COLUMN = 8
CHARACTER_TRAITS_COLUMN = 9

def parse_character_data(data_path: str):
    countries_with_characters: dict[str, list] = {}
    with open(data_path, 'rt', encoding="utf8") as data_file:
        data_file.readline() # Skip first line
        reader = csv.reader(data_file)
        for line_num, line in enumerate(reader, 2):
            full_name = line[FULL_NAME_COLUMN]
            first_name = line[FIRST_NAME_COLUMN]
            last_name = line[LAST_NAME_COLUMN]
            country_tag = line[COUNTRY_TAG_COLUMN]
            culture = line[CULTURE_COLUMN]
            interest_group = line[INTEREST_GROUP_COLUMN]
            ideology = line[IDEOLOGY_COLUMN]
            yes_values = set(re.split(r'[;]\s*', line[YES_VALUES_COLUMN].lower())) - {''}
            if len(yes_values) == 0:
                yes_values = set()
            birth_date = line[BIRTH_DATE_COLUMN]
            character_traits = set(re.split(r'[;]\s*', line[CHARACTER_TRAITS_COLUMN].lower())) - {''}
            if len(character_traits) == 0:
                character_traits = set()
            
            if full_name[0] == '#':
                continue
            if first_name == '' or last_name == '':
                continue

            if interest_group not in INTEREST_GROUPS:
                print(f'Unknown interest group: {interest_group} on line {line_num}')
                i = input('Press enter to continue, type "q" to quit, or type "s" to skip\n')
                if i == 'q':
                    exit()
                if i == 's':
                    continue
            if ideology not in IDEOLOGIES:
                print(f'Unknown ideology: {ideology} on line {line_num}')
                i = input('Press enter to continue, type "q" to quit, or type "s" to skip\n')
                if i == 'q':
                    exit()
                if i == 's':
                    continue
            if yes_values - YES_VALUES:
                print(f'Unknown yes values: {yes_values - YES_VALUES} on line {line_num}')
                i = input('Press enter to continue, type "q" to quit, or type "s" to skip\n')
                if i == 'q':
                    exit()
                if i == 's':
                    continue
            if character_traits - TRAITS:
                print(f'Unknown character traits: {character_traits - TRAITS} on line {line_num}')
                i = input('Press enter to continue, type "q" to quit, or type "s" to skip\n')
                if i == 'q':
                    exit()
                if i == 's':
                    continue

            character = {}

            character['first_name'] = first_name
            character['last_name'] = last_name
            character['culture'] = culture
            character['interest_group'] = interest_group
            character['ideology'] = ideology
            character['yes_values'] = yes_values
            character['birth_date'] = birth_date
            character['character_traits'] = character_traits

            country = countries_with_characters.get(country_tag, [])
            country.append(character)
            countries_with_characters[country_tag] = country
    return countries_with_characters

def generate_characters_objects(countries_with_characters: dict):
    root = ClausewitzRoot()
    charactersObject = ClausewitzObject()
    root.add_named_value('CHARACTERS', charactersObject)
    for country_tag, characters in countries_with_characters.items():
        countryObject = ClausewitzObject()
        for character in characters:
            characterObject = ClausewitzObject()
            characterObject.add_named_value('first_name', character['first_name'])
            characterObject.add_named_value('last_name', character['last_name'])
            characterObject.add_named_value('culture', character['culture'])
            characterObject.add_named_value('interest_group', character['interest_group'])
            characterObject.add_named_value('ideology', character['ideology'])
            characterObject.add_named_value('birth_date', character['birth_date'])
            for value in character['yes_values']:
                characterObject.add_named_value(value, 'yes')
            characterObject.add_named_value('historical', 'yes')
            traitsObject = ClausewitzObject()
            for trait in character['character_traits']:
                traitsObject.add_anonymous_value(trait)
            characterObject.add_named_value('traits', traitsObject)

            countryObject.add_named_value(f'create_character', characterObject)
        charactersObject.add_named_value(f'c:{country_tag}', countryObject)

    return root

def generate_characters(data_path: str):
    countries_with_characters = parse_character_data(data_path)
    characters = generate_characters_objects(countries_with_characters)
    return characters

if __name__ == '__main__':
    characters = generate_characters(CHARACTER_DATA_PATH)
    with open(CHARACTER_MOD_FILE_PATH, 'w') as file:
        file.write(characters.unparse())

            
