import csv
import os

NEW_STATES_PATH = os.path.join('game', 'data', 'new_states.csv')
OLD_STATES_PATH = os.path.join('data', 'state_ownership.csv')
COMBINED_STATES_PATH = os.path.join('data', 'combined_states.csv')

OWNERSHIP_REGION_TAG_COLUMN = 0
OWNERSHIP_COUNTRY_TAG_COLUMN = 3
OWNERSHIP_PROVINCES_COLUMN = 4

new_provinces = set()
new_states = {}
with open(NEW_STATES_PATH, 'r') as new_file:
    new_file_reader = csv.reader(new_file)
    for row in new_file_reader:
        owner = row[OWNERSHIP_REGION_TAG_COLUMN]
        region = row[OWNERSHIP_COUNTRY_TAG_COLUMN]
        owned_provinces = row[OWNERSHIP_PROVINCES_COLUMN].split(' ')
        owned_provinces = [p.upper() for p in owned_provinces]
        new_provinces.update(owned_provinces)
old_provinces = set()
old_states = {}
with open(OLD_STATES_PATH, 'r') as old_file:
    old_file_reader = csv.reader(old_file)
    for row in old_file_reader:
        owner = row[OWNERSHIP_REGION_TAG_COLUMN]
        region = row[OWNERSHIP_COUNTRY_TAG_COLUMN]
        owned_provinces = row[OWNERSHIP_PROVINCES_COLUMN].split(' ')
        owned_provinces = [p.upper() for p in owned_provinces]
        old_provinces.update(owned_provinces)

print('In old but not new:\n', old_provinces.difference(new_provinces))
print('\n'*10)
print('In new but not old:\n', new_provinces.difference(old_provinces))

# There are only provinces missing from the new states. In other words, provinces were removed and none were added.