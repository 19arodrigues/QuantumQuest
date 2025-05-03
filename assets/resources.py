#
# Copyright 2022 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Utilities for loading assests (fonts, images and sounds)
"""

import os
import pygame
import re

from pathlib import Path
from csv import reader
from os import walk
from assets.settings import WIDTH_UNIT

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "..", "assets")

def load_image(name, colorkey=None, scale=WIDTH_UNIT / 13):
    """
    Load image with pygame

    Parameters:
    name (string): file name
    """
    if not pygame.get_init():
        pygame.init()

    full_name = os.path.join(data_dir, "images", name)
    try:
        image = pygame.image.load(full_name)
    except pygame.error:
        print("Cannot load image:", full_name)
        error_message = pygame.get_error()
        raise SystemExit(error_message) from pygame.error
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    image = pygame.transform.scale(
        image, tuple(round(scale * x) for x in image.get_rect().size)
    )
    return image, image.get_rect()

def load_sound(name):
    """
    Load sound with pygame mixer

    Parameters:
    name (string): file name
    """
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    full_name = os.path.join(data_dir, "sound", name)
    try:
        sound = pygame.mixer.Sound(full_name)
    except pygame.error:
        print("Cannot load sound: %s" % full_name)
        error_message = pygame.get_error()
        raise SystemExit(error_message) from pygame.error
    return sound

def load_font(name, size=2 * WIDTH_UNIT):
    """
    Load font with pygame font

    Parameters:
    name (string): file name
    """
    if not pygame.font.get_init():
        pygame.font.init()

    full_name = os.path.join(data_dir, "font", name)
    try:
        font = pygame.font.Font(full_name, size)
    except pygame.error:
        print("Cannot load font: %s" % full_name)
        error_message = pygame.get_error()
        raise SystemExit(error_message) from pygame.error
    return font

class Font:
    def __init__(self, fontSize = 5 * WIDTH_UNIT):
        font = "Retro2.ttf" # bit5x3.ttf
        self.font = load_font(font, fontSize)

# Takes in a csv file path, opens and reads it and returns a list of values
def importCSVLayout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',') # takes in csv map and the separation char = delimiter
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

# Import animations
def importFolder(path):
    if path is None:
        return None

    surface_list = []
    # for X,XX,images in walk(path):
    #     for image in images:
    #         if '.png' in image:
    #             complete_path = path + '/' + image
    #             image_surf = pygame.image.load(complete_path).convert_alpha()
    #             surface_list.append(image_surf)

    # Get all file names
    folder_path = Path(path)
    file_names = [file.name for file in folder_path.iterdir() if file.is_file() and file.name.lower().endswith(".png")]

    # Utility method for sorting files by number
    def extract_number(filename):
        match = re.search(r'\d+', filename)  # Get tile id
        return int(match.group()) if match else float('inf')  # Use 'infinity' to deprioritise files with no number

    # Sort using the custom key
    sorted_files = sorted(file_names, key=lambda x: (extract_number(x), x))

    for file in sorted_files:
        complete_path = path + '/' + file
        image_surf = pygame.image.load(complete_path).convert_alpha()
        surface_list.append(image_surf)

    return surface_list

# image_cache = {}

def loadImages(base_path, save_path):
    # eg: base_path = 'cat/tutorials'
    # eg: save-path = 'Cat'
    # global image_cache
    image_cache = {}  # Reset cache

    base_path = os.path.abspath(base_path)

    if save_path not in image_cache:
        image_cache[save_path] = {}

    for folder_name in sorted(os.listdir(base_path)):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path) and folder_name.isdigit():
            folder_num = int(folder_name)
            image_cache[save_path][folder_num] = {}

            for file in os.listdir(folder_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    full_path = os.path.join(folder_path, file)
                    # print(f"Attempting to load: {full_path}")
                    try:
                        image = pygame.image.load(full_path).convert_alpha()
                        image_cache[save_path][folder_num][file] = image
                    except Exception as e:
                        print(f"Failed to load image {full_path}: {e}")
    return image_cache
