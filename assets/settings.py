# game setup
GAME_WIDTH = 1280
GAME_HEIGHT = 720
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
# WINDOW_WIDTH = 1664
# WINDOW_HEIGHT = 936
FPS = 120
TILESIZE = 32

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
CHAR_BOX_SIZE = 80
UI_FONT = '../Demo/assests/font/bit5x3.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOUR = '#71ddee'
UI_BG_COLOUR = '#222222'
UI_BORDER_COLOUR = '#111111'
TEXT_COLOUR = '#EEEEEE'

# ui colors
HEALTH_COLOUR = 'red'
ENERGY_COLOUR = 'blue'
EXP_COLOUR = '#063201'
UI_BORDER_COLOUR_ACTIVE = 'gold'

# Quantum Circuit Grid Colours
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
CYAN = 0, 255, 255
MAGENTA = 255, 0, 255
BLUE = 0, 0, 255
GREEN = 0, 255, 0
YELLOW = 255, 255, 0
GRAY = 128, 128, 128

# Quantum Circuit Movement ENUM
MOVE_LEFT = 1
MOVE_RIGHT = 2
MOVE_UP = 3
MOVE_DOWN = 4

# Quantum Circuit Geometry
QUBIT_AMT = 2
WIDTH_UNIT = 12

# Quantum States
BASIS_STATES = [["|0>", "|1>"],
                ["|00>", "|01>", "|10>", "|11>"],
                ["|000>", "|001>", "|010>", "|011>", "|100>", "|101>", "|110>", "|111>"]]

# Account Settings
WORLD_LEVEL = 1

# Game Rules
LEVEL_10_BOUNDARIES = [100, 200, 400, 600, 900, 1200, 1600, 2000, 2500, 3000]

# Characters
TEAM = ['Q']
CHARACTER_DATABASE = {
    'Q': {'name': 'Q', 'class': 'mage', 'specialisation': 'quantum',
            'base_health': 900, 'energy_cost': 80, 'base_attack': 70,
            'skill_base_attack': 30, 'skill_duration': 5, 'skill_cooldown': 10, 'skill_type': 'instant',
            'skill_character_animation': '../BudgetGenshin/graphics/player/cyno/skill',
            'skill_construct_animation': None,
            'skill_additional_animation': None,
            'burst_base_attack': 80, 'burst_duration': 15, 'burst_cooldown': 18},
}

# Weapons - Graphics are extracted directly in weapon.py in __init__()
# WEAPON_DATA = {
#     'sword': {'cooldown': 100, 'attack': 15},
#     'polearm': {'cooldown': 70, 'attack': 10},
#     'catalyst': {'cooldown': 60, 'attack': 10},
#     'claymore': {'cooldown': 150, 'attack': 25},
#     'bow': {'cooldown': 50, 'attack': 8}
# }

# Enemies
ENEMY_DATA = {
    'bamboo': {'base_health': 500, 'base_attack': 10, 'base_exp': 16,
            'attack_type': 'leaf_attack', 'attack_cooldown': 10,
            'speed': 2, 'defence': 5, 'knockback_resistance': 10,  'attack_radius': 120, 'alert_radius': 300,
            'graphic': '../BudgetGenshin/graphics/enemies/bamboo',
            'attack_sound': '../BudgetGenshin/audio/slash.wav'},
    'spirit': {'base_health': 300, 'base_attack': 5, 'base_exp': 20,
            'attack_type': 'thunder', 'attack_cooldown': 3,
            'speed': 4, 'defence': 2, 'knockback_resistance': 10, 'attack_radius': 100, 'alert_radius': 400,
            'graphic': '../BudgetGenshin/graphics/enemies/spirit',
            'attack_sound': '../BudgetGenshin/audio/slash.wav'},
}

# Assets Used
# Player Sprite: https://doublesidedcreamsicle.itch.io/cute-wizard-pack-01-top-down
# level0 map: https://cainos.itch.io/pixel-art-top-down-basic
# Cat: https://elthen.itch.io/2d-pixel-art-cat-sprites?download
# Spells: https://bdragon1727.itch.io/750-effect-and-fx-pixel-all?download
# Misc