# This script is to read the buildings in common/buildings/ and their production methods
import clausewitz_parser
from clausewitz_object import ClausewitzObject
from clausewitz_root import ClausewitzRoot

import os
import csv

FOLDER_PATH = os.path.join('game', 'files', 'buildings')
FILE_NAMES = [
    '01_industry.txt', '02_agro.txt', '03_mines.txt', '04_plantations.txt', '05_military.txt', '06_urban_center.txt', '07_government.txt',
    '08_monuments.txt', '09_misc_resource.txt', '10_canals.txt', '11_private_infrastructure.txt', '12_subsistence.txt', '13_construction.txt'
]

OUT_PATH = os.path.join('game', 'data', 'buildings.csv')

def unparse_buildings_file(file_path) -> dict[str: list[str]]:
    buildings_root: ClausewitzRoot = clausewitz_parser.parse_file(file_path)
    data = {}
    buildings = buildings_root.get_names()
    for building in buildings:
        building_object = buildings_root.get_named_value(building)
        production_methods = building_object.get_named_value('production_method_groups')
        data[building] = production_methods.get_anonymous_values()
    return data

if __name__ == '__main__':
    file_paths = [os.path.join(FOLDER_PATH, file_name) for file_name in FILE_NAMES]
    with open(OUT_PATH, 'wt', newline='') as file:
        csv_writer = csv.writer(file)
        for file_path in file_paths:
            building_data = unparse_buildings_file(file_path)
            for building, production_methods in building_data.items():
                csv_writer.writerow([building] + production_methods)


