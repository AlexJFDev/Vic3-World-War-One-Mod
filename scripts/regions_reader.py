import os
import csv

import clausewitz_parser
from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

"""
STATE_NEW_SOUTH_WALES = {
    id = 558
    subsistence_building = "building_subsistence_farms"
    provinces = { "x027214" "x0274E2" "x0285F6" "x02DB56" "x045603" "x086D7B" "x0AA399" "x0E3317" "x0EA2A3" "x0F081C" "x116050" "x1160CF" "x11FF8C" "x16D521" "x18E220" "x19D5E4" "x1A3E4E" "x1AE650" "x1C487B" "x1F3DBB" "x20093A" "x20201C" "x234F3B" "x237F0D" "x24AEFA" "x24BF23" "x254626" "x267585" "x26EEF1" "x276C93" "x279D6E" "x27A4C5" "x28BA60" "x2ACD80" "x2BD326" "x2D0386" "x2FE431" "x30D9E5" "x31FF16" "x33409C" "x3354DD" "x36A22E" "x37807C" "x391526" "x3A6A72" "x3AC189" "x3ADE63" "x3C7D82" "x3D22B3" "x3D5CE8" "x40E057" "x447C79" "x44CFBA" "x4555A7" "x45975E" "x467A72" "x468CAB" "x482C38" "x4866D3" "x4A7137" "x4AAA58" "x4FF662" "x518D32" "x51BCDB" "x51E0D0" "x52D3F3" "x533071" "x53F27D" "x54F665" "x562717" "x5A4740" "x5BE1A4" "x5CAC91" "x5E0692" "x5E4B6A" "x617C46" "x628CE9" "x6334E0" "x6576A8" "x681CC6" "x68E6E2" "x698A94" "x6B877D" "x6C0833" "x6CBE17" "x6E5393" "x6FB312" "x6FD80D" "x704E84" "x70E720" "x722808" "x73D224" "x740B78" "x75A793" "x768B4D" "x798FE7" "x799B34" "x7E02ED" "x7E0DF6" "x821BC4" "x83B57F" "x840C5D" "x85E2DE" "x8A6B46" "x8ACD73" "x8B56F5" "x8CAAE6" "x8D65DF" "x8FD0F0" "x90F3AF" "x91A2E2" "x93A7A7" "x94099D" "x9453C1" "x95B28A" "x97B2F0" "x9907A8" "x99526E" "x996B4B" "x9A8050" "x9AFA6A" "x9D5FB1" "x9D61D1" "x9D8ACB" "xA39D9A" "xA681A6" "xA6D562" "xA8E040" "xA98344" "xAEC58F" "xAEFFEB" "xAF3A01" "xAFEC31" "xB01F74" "xB15C6D" "xB48C62" "xB62ED1" "xB6943C" "xB9104E" "xB96167" "xB9E4F4" "xBA0D99" "xBDF73B" "xBE5235" "xBEA265" "xC15B4F" "xC193DA" "xC1F3AD" "xC24514" "xC24AAA" "xC345CF" "xC41B96" "xC42012" "xC7A584" "xC7BC96" "xCB67EC" "xCBED4E" "xCD17C3" "xCDE6CE" "xCEDA26" "xCF4030" "xCFB449" "xD060D0" "xD2EE80" "xD65CBB" "xD74DB9" "xD9170D" "xDA4137" "xDBD9ED" "xDF754A" "xE02F70" "xE15846" "xE18B8E" "xE4FF76" "xE6B9A2" "xE6C282" "xE7C856" "xE7D61A" "xE85D89" "xE8CAF7" "xED82D9" "xEDA242" "xEF1DE2" "xF17F79" "xF22CA8" "xF4A6F5" "xF4CF93" "xF6ABF7" "xFA57CA" "xFAC1B2" "xFB0B72" "xFB3077" "xFD1F91" "xFDD3E6" "xFDDBE1" "xFDFB3F" }
    traits = { "state_trait_great_dividing_range" "state_trait_murray_darling_basin" }
    city = "xFDFB3F"
    port = "xAEFFEB"
    farm = "x8B56F5"
    mine = "x24AEFA"
    wood = "x799B34"
    arable_land = 40
    arable_resources = { "bg_wheat_farms" "bg_livestock_ranches" "bg_cotton_plantations" "bg_tea_plantations" "bg_sugar_plantations" "bg_vineyard_plantations" }
    capped_resources = {
        bg_coal_mining = 80
        bg_iron_mining = 36
        bg_logging = 7
        bg_whaling = 4
        bg_fishing = 8
    }
    resource = {
        type = "bg_gold_fields"
        depleted_type = "bg_gold_mining"
        undiscovered_amount = 12
    }
    resource = {
        type = "bg_oil_extraction"
        undiscovered_amount = 10
    }
    naval_exit_id = 3122
}
"""

STATE_REGIONS_PATH = os.path.join('game', 'files', 'map_data', 'state_regions')
STATE_REGION_FILE_NAMES = [
    '00_west_europe.txt',
    '01_south_europe.txt',
    '02_east_europe.txt',
    '03_north_africa.txt',
    '04_subsaharan_africa.txt',
    '05_north_america.txt',
    '06_central_america.txt',
    '07_south_america.txt',
    '08_middle_east.txt',
    '09_central_asia.txt',
    '10_india.txt',
    '11_east_asia.txt',
    '12_indonesia.txt',
    '13_australasia.txt',
    '14_siberia.txt',
    '15_russia.txt',
    '99_seas.txt',
]
STATE_REGION_PATHS = [os.path.join(STATE_REGIONS_PATH, file_name) for file_name in STATE_REGION_FILE_NAMES]

STATE_REGIONS_CSV_PATH = os.path.join('game', 'data', 'state_regions.csv')

def unparse_regions_file(file_path):
    state_regions = {}
    regions_root = clausewitz_parser.parse_path(file_path)
    state_region_names = regions_root.get_names()
    for state_region_name in state_region_names:
        state_region: ClausewitzObject = regions_root.get_value_named(state_region_name)
        id_value = state_region.get_value_named('id') # Id is a reserved keyword
        subsistence_building = state_region.get_value_named('subsistence_building')
        city = state_region.get_value_named('city')
        port = state_region.get_value_named('port')
        farm = state_region.get_value_named('farm')
        mine = state_region.get_value_named('mine')
        wood = state_region.get_value_named('wood')
        arable_land = state_region.get_value_named('arable_land')
        provinces = state_region.get_value_named('provinces').get_anonymous_values()
        traits = state_region.get_value_named('traits').get_anonymous_values()
        arable_resources = state_region.get_value_named('arable_resources').get_anonymous_values()
        capped_resources = state_region.get_value_named('capped_resources').get_name_value_pairs()