import os
import csv

import clausewitz_parser
from clausewitz_object import ClausewitzObject
from clausewitz_root import ClausewitzRoot

NEW_STATES_PATH = os.path.join('game', 'files', 'new_states.txt')
MOD_STATES_PATH = os.path.join('mod', 'files', 'states.txt')
NEW_STATES_CSV = os.path.join('game', 'data', 'new_states.csv')

OWNERSHIP_REGION_TAG_COLUMN = 0
OWNERSHIP_COUNTRY_TAG_COLUMN = 3
OWNERSHIP_PROVINCES_COLUMN = 4

def unparse_states(states_root: ClausewitzRoot):
    states = {}
    state_names = states_root.get_value_named('STATES').get_names()
    for state_name in state_names:
        state: ClausewitzObject = states_root.get_value_named('STATES').get_value_named(state_name)
        created_states: list[ClausewitzObject] = state.get_values_named('create_state')
        for created_state in created_states:
            owner: str = created_state.get_value_named('country')[2:]
            owned_provinces: list[str] = created_state.get_value_named('owned_provinces').get_anonymous_values()
            states[f'{owner}:{state_name}'] = owned_provinces

    return states

def save_states(states: dict[str: list[str]]):
    with open(NEW_STATES_CSV, 'w', newline='') as states_file:
        csv_writer = csv.writer(states_file)
        for state, provinces in states.items():
            owner, region = state.split(':', 1)
            csv_writer.writerow([region, '', '', owner, ' '.join(provinces[:-1])])

if __name__ == '__main__':
    with open(NEW_STATES_PATH, 'rt') as states_file:
        new_states_root = clausewitz_parser.parse_file(states_file)
    new_states = unparse_states(new_states_root)
    save_states(new_states)
