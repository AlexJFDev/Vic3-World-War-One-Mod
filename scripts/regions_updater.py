import os
import csv

OLD_REGIONS_DATA_PATH = os.path.join('mod', 'data', 'old_state_regions.csv')
NEW_REGIONS_DATA_PATH = os.path.join('game', 'data', 'state_regions.csv')
REGIONS_DATA_PATH = os.path.join('mod', 'data', 'state_regions.csv')

OLD_REGION_NAME_COLUMN = 0
OLD_REGION_TAG_COLUMN = 1
OLD_REGION_HOMELANDS_COLUMN = 2

NEW_REGIONS_TAG_COLUMN = 0
NEW_REGIONS_ID_COLUMN = 1
NEW_REGIONS_PROVINCES_COLUMN = 9

old_regions = {}
with open(OLD_REGIONS_DATA_PATH, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        name = row[OLD_REGION_NAME_COLUMN]
        tag = row[OLD_REGION_TAG_COLUMN]
        homelands = row[OLD_REGION_HOMELANDS_COLUMN]
        old_regions[tag] = (name, homelands)

new_regions = {}
with open(NEW_REGIONS_DATA_PATH, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        tag = f's:{row[NEW_REGIONS_TAG_COLUMN]}'
        id = int(row[NEW_REGIONS_ID_COLUMN])
        provinces = row[NEW_REGIONS_PROVINCES_COLUMN]
        if id < 3000: # Ocean region
            new_regions[tag] = provinces

lines = []
for tag, provinces in new_regions.items():
    if tag in old_regions:
        old_name, old_homelands = old_regions[tag]
        lines.append([old_name, tag, old_homelands, provinces,'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
    else:
        lines.append(['', tag, '', provinces,'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

lines.sort(key=lambda line: line[1])

lines.insert(0, ['State Name', 'State Region Tag', 'Homelands', 'Provinces', 'Arable Land', 'Traits', 'Claims', 'Strategic Region', 'File Region', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

with open(REGIONS_DATA_PATH, 'w', newline='') as regions_file:
    writer = csv.writer(regions_file, quoting=csv.QUOTE_ALL)
    for line in lines:
        writer.writerow(line)