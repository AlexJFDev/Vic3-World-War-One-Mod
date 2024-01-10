import os
import csv

from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject
from clausewitz_parser import parse_file

DEFINITIONS_PATH: str = os.path.join('data', 'countries.txt')
CSV_OUT_PATH: str = os.path.join('data', 'definitions.csv')

definitions_root: ClausewitzRoot = parse_file(DEFINITIONS_PATH)

with open(CSV_OUT_PATH, 'w') as file:
    csv_writer = csv.writer(file)
    for tag, values in definitions_root.name_values.items():
        definition: ClausewitzObject = values[0]

        is_dynamic = definition.get_named_value('dynamic_country_definition')
        if is_dynamic == 'yes':
            csv_writer.writerow(['', tag, '', '', '', '', True])
            continue
        
        tier = definition.get_named_value('tier')
        capital = definition.get_named_value('capital')
        cultures: list = definition.get_named_value('cultures').get_anonymous_values()
        while '' in cultures:
            cultures.remove('')
        color: list = definition.get_named_value('color').get_anonymous_values()
        while '' in color:
            color.remove('')

        csv_writer.writerow(['', tag, ' '.join(color), tier, ' '.join(cultures), capital, False])