import clausewitz_parser
from clausewitz_object import ClausewitzObject
from clausewitz_root import ClausewitzRoot

import os

GAME_TRAITS_PATH = os.path.join('game', 'files', 'common', 'character_traits')
GAME_TRAITS_FILES = ['condition_traits.txt', 'personality_traits.txt', 'skill_traits.txt']

GAME_IDEOLOGIES_PATH = os.path.join('game', 'files', 'common', 'ideologies')
GAME_IDEOLOGIES_FILES = [
    '00_leader_french_flavored.txt',
    '00_leader_ideologies_flavored.txt',
    '00_leader_ideologies.txt'
]

def read_traits_from_file(path):
    traits_root: ClausewitzRoot = clausewitz_parser.parse_path(path)
    return traits_root.get_name_value_pairs().keys()

def read_ideologies_from_file(path):
    ideologies_root: ClausewitzRoot = clausewitz_parser.parse_path(path)
    return ideologies_root.get_name_value_pairs().keys()

traits = set()
for file_name in GAME_TRAITS_FILES:
    file_path = os.path.join(GAME_TRAITS_PATH, file_name)
    traits = traits.union(read_traits_from_file(file_path))
print(traits)

ideologies = set()
for file_name in GAME_IDEOLOGIES_FILES:
    file_path = os.path.join(GAME_IDEOLOGIES_PATH, file_name)
    ideologies = ideologies.union(read_ideologies_from_file(file_path))
print(ideologies)