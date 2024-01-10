import os

import clausewitz_root
from clausewitz_parser import parse_file

DEFINITIONS_PATH: str = os.path.join('data', 'countries_small.txt')

definitions_root = parse_file(DEFINITIONS_PATH)

print(definitions_root.unparse())