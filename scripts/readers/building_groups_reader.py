# This script is to read the buildings in common/buildings/ and their production methods
import clausewitz_parser
from clausewitz_object import ClausewitzObject
from clausewitz_root import ClausewitzRoot

import os
import csv

BUILDING_FOLDER_PATH = os.path.join('game', 'files', 'buildings')
BUILDING_FILE_NAMES = [
    '01_industry.txt', '02_agro.txt', '03_mines.txt', '04_plantations.txt', '05_military.txt', '06_urban_center.txt', '07_government.txt',
    '08_monuments.txt', '09_misc_resource.txt', '10_canals.txt', '11_private_infrastructure.txt', '12_subsistence.txt', '13_construction.txt'
]

PM_GROUP_FOLDER_PATH = os.path.join('game', 'files', 'production_method_groups')
PM_GROUP_FILE_NAMES = [
    '00_dummy.txt', '01_industry.txt', '02_agro.txt', '03_mines.txt', '04_plantations.txt', '05_military.txt', '06_urban_center.txt', '07_government.txt',
    '08_monuments.txt', '09_misc_resource.txt', '10_canals.txt', '11_private_infrastructure.txt', '12_subsistence.txt', '13_construction.txt'
]

OUT_PATH = os.path.join('game', 'data', 'buildings.csv')

def unparse_buildings_file(file_path) -> dict[str: list[str]]:
    buildings_root: ClausewitzRoot = clausewitz_parser.parse_path(file_path)
    data = {}
    buildings = buildings_root.get_names()
    for building in buildings:
        building_object = buildings_root.get_value_named(building)
        production_groups = building_object.get_value_named('production_method_groups')
        data[building] = production_groups.get_anonymous_values()
    return data

def unparse_pm_group_file(file_path):
    pm_group_root: ClausewitzRoot = clausewitz_parser.parse_path(file_path)
    data = {}
    groups = pm_group_root.get_names()
    for group in groups:
        production_methods = pm_group_root.get_value_named(group).get_value_named('production_methods').get_anonymous_values()
        data[group] = production_methods
    return data


if __name__ == '__main__':
    building_file_paths = [os.path.join(BUILDING_FOLDER_PATH, file_name) for file_name in BUILDING_FILE_NAMES]
    pm_group_file_paths = [os.path.join(PM_GROUP_FOLDER_PATH, file_name) for file_name in PM_GROUP_FILE_NAMES]
    with open(OUT_PATH, 'wt', newline='') as file:
        csv_writer = csv.writer(file)
        pm_groups = {}
        for file_path in pm_group_file_paths:
            pm_group_data = unparse_pm_group_file(file_path)
            for group, production_methods in pm_group_data.items():
                pm_groups[group] = production_methods
        print(pm_groups)
        for file_path in building_file_paths:
            building_data = unparse_buildings_file(file_path)
            for building, production_method_groups in building_data.items():
                production_methods = []
                for production_method_group in production_method_groups:
                    production_methods += pm_groups[production_method_group]
                csv_writer.writerow([building] + production_methods)