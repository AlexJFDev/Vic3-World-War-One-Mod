import clausewitz_parser
from clausewitz_root import ClausewitzRoot

import os
import itertools 


STRATEGIC_REGIONS_PATH = os.path.join('game', 'files', 'common', 'strategic_regions')
STRATEGIC_REGIONS_FILE_NAMES = [
    'african_strategic_regions.txt',
    'east_asia_strategic_regions.txt',
    'europe_strategic_regions.txt',
    'north_america_strategic_regions.txt',
    'south_america_strategic_regions.txt',
    'water_strategic_regions.txt',
    'west_south_asia_strategic_regions.txt'
]
STRATEGIC_REGIONS_PATHS = [os.path.join(STRATEGIC_REGIONS_PATH, file_name) for file_name in STRATEGIC_REGIONS_FILE_NAMES]

def unparse_strategic_regions_file(file_path):
    strategic_regions = []
    strategic_regions_root: ClausewitzRoot = clausewitz_parser.parse_path(file_path)
    for strategic_region in strategic_regions_root.get_name_value_pairs().keys():
        strategic_regions.append(strategic_region)
    return strategic_regions

if __name__ == '__main__':
    strategic_regions = []
    for strategic_regions_path in STRATEGIC_REGIONS_PATHS:
        strategic_regions.append(unparse_strategic_regions_file(strategic_regions_path))
    print(','.join(STRATEGIC_REGIONS_PATHS))
    for row in itertools.zip_longest(*strategic_regions, fillvalue=''):
        print(','.join(row))
    
