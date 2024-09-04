import clausewitz_parser
from clausewitz_root import ClausewitzRoot

import os
import itertools 
#C:\Users\Alex\Desktop\Projects\Vic3-World-War-One-Mod\scripts\game\files\common\combat_unit_types\00_combat_unit_types.txt

COMBAT_UNITS_PATH = os.path.join('game', 'files', 'common', 'combat_unit_types', '00_combat_unit_types.txt')

def unparse_combat_unit_types_file(file_path):
    unit_groups = {}
    combat_unit_types_root: ClausewitzRoot = clausewitz_parser.parse_path(file_path)
    for unit_type, unit_data in combat_unit_types_root.get_name_value_pairs().items():
        unit_group_type = unit_data[0].get_value_named('group')
        unit_group = unit_groups.get(unit_group_type, [])
        unit_group.append(unit_type)
        unit_groups[unit_group_type] = unit_group
    return unit_groups

if __name__ == '__main__':
    unit_groups = unparse_combat_unit_types_file(COMBAT_UNITS_PATH)
    print(','.join(unit_groups.keys()))
    for row in itertools.zip_longest(*unit_groups.values(), fillvalue=''):
        print(','.join(row))
