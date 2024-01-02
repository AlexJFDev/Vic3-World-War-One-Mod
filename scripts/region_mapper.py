import os
import csv
import numpy as np
from PIL import Image, ImageOps
import random

PROVINCE_DATA: str = os.path.join('data', 'state_regions.csv')
INPUT_MAP: str = os.path.join('data', 'provinces.png')
OUTPUT_MAP: str = os.path.join('data', 'state_regions.png')

def random_color():
    return np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])

def convert_colors(provinces):
    province_ids = provinces.split(' ')
    colors = []
    for province in province_ids:
        red = int(province[1:3], 16)
        blue = int(province[3:5], 16)
        green = int(province[5:7], 16)

        colors.append([red, blue, green])
    return colors

if __name__ == '__main__':
    map = Image.open(INPUT_MAP)
    #map.show()

    np_map = np.array(map)
    #print(np_map)

    print('Generating color map')
    color_map = {}
    with open(PROVINCE_DATA, 'r') as province_file:
        province_reader = csv.reader(province_file)
        for state_name, provinces in province_reader:
            #print(provinces)
            colors = convert_colors(provinces)
            state_color = random_color()
            for color in colors:
                color_map[str(np.array(color))] = state_color
    print('Generating new map')
    for row_num, row in enumerate(np_map):
        print(f'    Row: {row_num}')
        for col_num, col in enumerate(row):
            col_string = str(col)
            new_color = color_map.get(col_string)
            if new_color is not None:
                np_map[row_num][col_num] = new_color
    
    new_map = Image.fromarray(np_map)
    new_map.show()
    new_map.save(OUTPUT_MAP)
    