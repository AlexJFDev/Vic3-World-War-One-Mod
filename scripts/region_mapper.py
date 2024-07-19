import os
import csv
import numpy as np
from PIL import Image, ImageOps
import random

PROVINCE_DATA: str = os.path.join('game', 'data', 'state_regions.csv')
INPUT_MAP: str = os.path.join('game', 'files', 'map_data', 'provinces.png')
OUTPUT_MAP: str = os.path.join('game', 'data', 'state_regions2.png')

def convert_colors(provinces: list[str]) -> list[np.ndarray]:
    colors = []
    for province in provinces:
        #print(province)
        red = int(province[1:3], 16)
        blue = int(province[3:5], 16)
        green = int(province[5:7], 16)

        colors.append(np.array([red, blue, green]))
    return colors

if __name__ == '__main__':
    map = Image.open(INPUT_MAP)
    #map.show()

    map_array = np.array(map)
    #print(np_map)

    print('Generating color map')
    color_map = {}
    with open(PROVINCE_DATA, 'r') as province_file:
        province_reader = csv.reader(province_file)
        for line in province_reader:
            province_ids = line[9].split(' ')
            province_colors = convert_colors(province_ids)
            if int(line[1]) >= 3000: # Is ocean
                state_color = np.array([255, 255, 255])
            else: # Is land
                state_color = province_colors[0]
            #print(provinces)
            for province_color in province_colors:
                color_map[str(province_color)] = state_color
    print('Generating new map')
    for row_num, row in enumerate(map_array):
        print(f'    Row: {row_num}')
        for col_num, col in enumerate(row):
            col_string = str(col)
            new_color = color_map.get(col_string)
            if new_color is not None:
                map_array[row_num][col_num] = new_color
    
    new_map = Image.fromarray(map_array)
    new_map.show()
    new_map.save(OUTPUT_MAP)
    