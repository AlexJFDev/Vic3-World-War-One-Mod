import os
import csv
import numpy as np
from PIL import Image, ImageOps
import random

PROVINCE_DATA: str = os.path.join('game', 'data', 'state_regions.csv')
INPUT_MAP: str = os.path.join('game', 'files', 'map_data', 'provinces.png')
OUTPUT_MAP: str = os.path.join('game', 'data', 'state_regions2.png')

def convert_colors(provinces: list[str]):
    colors = []
    for province in provinces:
        if len(province) != 7:
            continue
        red = int(province[1:3], 16)
        blue = int(province[3:5], 16)
        green = int(province[5:7], 16)

        colors.append((red, blue, green))
    return colors

def map_color(color: tuple[int, int, int]):
    new_color = color_map.get(tuple(color))
    if new_color is None: return (0, 0, 0)
    return new_color

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
                state_color = (255, 255, 255)
            else: # Is land
                state_color = province_colors[0]
            #print(provinces)
            for province_color in province_colors:
                color_map[province_color] = state_color
    print('Generating new map')
    # map_array = np.apply_along_axis(map_color, 2, map_array)
    for row_num, row in enumerate(map_array):
        print(f'    Row: {row_num}')
        for col_num, col in enumerate(row):
            color = tuple(col)
            new_color = color_map.get(color)
            if new_color is None:
                map_array[row_num][col_num] = (0, 0, 0)
            else:
                map_array[row_num][col_num] = new_color
    print('Finished generating map')

    new_map = Image.fromarray(map_array)
    new_map.show()
    new_map.save(OUTPUT_MAP)
    