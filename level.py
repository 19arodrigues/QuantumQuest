# 
from random import randint
import pygame

from state import State
from assets.settings import *
from assets.circuit_grid import CircuitGrid
from assets.circuit_grid_model import CircuitGridModel
from assets import stateUI
from assets import levelUI
from assets.quantum_computer import QuantumComputer
from camera import Camera
from assets.resources import importCSVLayout, importFolder
from tile import Tile
from assets.player import Player
from assets.cat import Cat
from superSprite import SuperSprite, SuperSpriteGroup
from assets.entity import Entity


class Level(State):
    def __init__(self, game): 
        super().__init__(game, 'level')
        # Init player and window
        self.player = None
        self.window = pygame.display.get_surface()
        self.game = game
        self.levelState = 0
        self.game.actions["toggleCircuitGrid"] = False
        self.level = 0
        self.loadResources()

        # sprite groups setup
        # self.visible_sprites = pygame.sprite.Group()
        # self.camera = Camera(self) # Visible with no collision
        self.visible_sprites = Camera(self)
        self.superposition_player_sprites = [] # Label for multiple player sprites for superposition states
        self.obstacle_sprites = pygame.sprite.Group() # Not inherently visible, but has collision
        self.quantumGate_sprites = pygame.sprite.Group() # Quantum gates

        self.interactableSprites = SuperSpriteGroup(name='interactables')
        self.visibleSprites = SuperSpriteGroup(name='visible')
        self.obstacleSprites = SuperSpriteGroup(name='obstacles')

        # Level Properties
        self.levelProperties = {0: {"spawn point": (128, 768), "qubit amount": 1, "progress": 0},
                                1: {"stairs down unlocked": False, "spawn point": (800, 160), "qubit amount": 2, "progress": 0},
                                2: {"spawn point": (64, 768), "bell state": 0, "bell": None, "qubit amount": 1, "progress": 0, "pressedCooldown": 0, "bellStateDetermined": False},
                                3: {"spawn point": (480, 352), "stairs down unlocked": False, "platform toggle": False, "qubit amount": 2, "progress": 0}}

        # Draw maps and sprites
        self.loadLevel()

        # Init Level UI
        self.levelUI = levelUI.LevelUI(self)
        # Init Quantum UI
        FIELD_HEIGHT = round(WINDOW_HEIGHT * 0.7)
        self.qubitNo = self.levelProperties[self.level]["qubit amount"]
        circuit_model = CircuitGridModel(self.qubitNo, 4)

        self.circuitGrid = CircuitGrid(circuit_model, game)
        self.stateMarkers = stateUI.StateMarkers(self.qubitNo)
        self.quantumComputer = QuantumComputer(self.stateMarkers, self.circuitGrid)
        # self.moving_sprites = pygame.sprite.Group()
        # self.moving_sprites.add(self.stateMarkers.markers)

    def loadResources(self):
        self.csvLayouts = {
            20: {
                "interactions_passable": importCSVLayout("assets/levels/leveltest/level2_interactions_passable.csv"),
                "interactions_passable2": importCSVLayout("assets/levels/leveltest/level2_interactions_passable2.csv"),
                "interactions": importCSVLayout("assets/levels/leveltest/level2_interactions.csv"),
                "interactions_ceiling": importCSVLayout("assets/levels/leveltest/level2_interactions_ceiling.csv"),
                "player": importCSVLayout("assets/levels/leveltest/level2_player.csv"),
                "npc": importCSVLayout("assets/levels/leveltest/level2_npc.csv"),
                "wall_ceiling": importCSVLayout("assets/levels/leveltest/level2_wall_ceiling.csv"), # Ceiling
                "wall_stem": importCSVLayout("assets/levels/leveltest/level2_wall_stem.csv"), # Stem
            },
                # 101: {
                #     "interactions": importCSVLayout("assets/levels/level3/level3_interactions.csv"),
                #     "player": importCSVLayout("assets/levels/level3/level3_player.csv"),
                #     "npc": importCSVLayout("assets/levels/level3/level3_npc.csv"),
                #     "wall_ceiling": importCSVLayout("assets/levels/level3/level3_wall_ceiling.csv"), # Ceiling
                #     "wall_stem": importCSVLayout("assets/levels/level3/level3_wall_stem.csv"), # Stem
                # },
            0: {
                "player": importCSVLayout("assets/levels/level0/level0_player.csv"),
                "npc": importCSVLayout("assets/levels/level0/level0_npc.csv"),
                "wall_stem": importCSVLayout("assets/levels/level0/level0_wall_stem.csv"), # Stem
                "wall_ceiling": importCSVLayout("assets/levels/level0/level0_wall_ceiling.csv"), # Ceiling
                "void": importCSVLayout("assets/levels/level0/level0_void.csv"),
                "interactions": importCSVLayout("assets/levels/level0/level0_interactions.csv"),
            },
            1: {
                "player": importCSVLayout("assets/levels/level1/level1_player.csv"),
                "npc": importCSVLayout("assets/levels/level1/level1_npc.csv"),
                "wall_stem": importCSVLayout("assets/levels/level1/level1_wall_stem.csv"), # Stem
                "wall_ceiling": importCSVLayout("assets/levels/level1/level1_wall_ceiling.csv"), # Ceiling
                "interactions": importCSVLayout("assets/levels/level1/level1_interactions.csv"),
                "interactions_ceiling": importCSVLayout("assets/levels/level1/level1_interactions_ceiling.csv"),
                "interactions_passable": importCSVLayout("assets/levels/level1/level1_interactions_passable.csv"),
                "void_toggle": importCSVLayout("assets/levels/level1/level1_void_toggle.csv")
            },
            2: {
                "player": importCSVLayout("assets/levels/level2/level2_player.csv"),
                "npc": importCSVLayout("assets/levels/level2/level2_npc.csv"),
                "wall_stem": importCSVLayout("assets/levels/level2/level2_wall_stem.csv"), # Stem
                "wall_ceiling": importCSVLayout("assets/levels/level2/level2_wall_ceiling.csv"), # Ceiling
                "void": importCSVLayout("assets/levels/level2/level2_void.csv"),
                "interactions": importCSVLayout("assets/levels/level2/level2_interactions.csv"),
            },
            3: {
                "player": importCSVLayout("assets/levels/level3/level3_player.csv"),
                "npc": importCSVLayout("assets/levels/level3/level3_npc.csv"),
                "wall_stem": importCSVLayout("assets/levels/level3/level3_wall_stem.csv"), # Stem
                "wall_ceiling": importCSVLayout("assets/levels/level3/level3_wall_ceiling.csv"), # Ceiling
                "void": importCSVLayout("assets/levels/level3/level3_void.csv"),
                "interactions": importCSVLayout("assets/levels/level3/level3_interactions.csv"),
                "void_toggle": importCSVLayout("assets/levels/level3/level3_void_toggle.csv")
            },
            4: {
                # "plants": importCSVLayout("assets/levels/level0/level0_plants.csv"),
                # "player": importCSVLayout("assets/levels/level0/level0_player.csv"),
                # "npc": importCSVLayout("assets/levels/level0/level0_npc.csv"),
                # "props_stem": importCSVLayout("assets/levels/level0/level0_props_stem.csv"), # Stem
                # "props": importCSVLayout("assets/levels/level0/level0_props.csv"), 
                # "props2_stem": importCSVLayout("assets/levels/level0/level0_props2_stem.csv"), # Stem
                # "props2": importCSVLayout("assets/levels/level0/level0_props2.csv"), 
                # "shadow_plant": importCSVLayout("assets/levels/level0/level0_shadow_plant.csv"),
                # "shadow": importCSVLayout("assets/levels/level0/level0_shadow.csv"),
                # "shadow2": importCSVLayout("assets/levels/level0/level0_shadow2.csv"),
                # "struct_ceiling": importCSVLayout("assets/levels/level0/level0_struct_ceiling.csv"), # Ceiling
                # "struct": importCSVLayout("assets/levels/level0/level0_struct.csv"),
                # "trees_ceiling": importCSVLayout("assets/levels/level0/level0_trees_ceiling.csv"), # Ceiling
                # "trees_stem": importCSVLayout("assets/levels/level0/level0_trees_stem.csv"), # Stem
                # "wall_ceiling": importCSVLayout("assets/levels/level0/level0_wall_ceiling.csv"), # Ceiling
                # "wall_stem": importCSVLayout("assets/levels/level0/level0_wall_stem.csv"), # Stem
                # "wall": importCSVLayout("assets/levels/level0/level0_wall.csv"),
                # "wall2_stem": importCSVLayout("assets/levels/level0/level0_wall2_stem.csv"), # Stem
                # "wall2_ceiling": importCSVLayout("assets/levels/level0/level0_wall2_ceiling.csv"), # Ceiling
                }
        }

        self.tilesGraphics = {
            # Level 0
            0: {
                # "plant": importFolder("assets/levels/level0/plant"),
                # "props": importFolder("assets/levels/level0/props"),
                # "props2": importFolder("assets/levels/level0/props2"),
                # "shadow": importFolder("assets/levels/level0/shadow"),
                # "shadow_plant": importFolder("assets/levels/level0/shadow_plant"),
                # "struct": importFolder("assets/levels/level0/struct"),
                # "wall": importFolder("assets/levels/level0/wall"),
            },
            # Level 2
            20: {
                "interactions": importFolder("assets/levels/leveltest/interactions"),
                "wall": importFolder("assets/levels/leveltest/wall"),
            },
            1: {
                "qgates": importFolder("assets/levels/tilesets/qgates"),
                "wall": importFolder("assets/levels/tilesets/wall"),
            }

        }

        self.floorGrpahics = {
            0: pygame.image.load('assets/levels/level0/level0.png').convert_alpha(),
            1: pygame.image.load('assets/levels/level1/level1.png').convert_alpha(),
            2: pygame.image.load('assets/levels/level2/level2.png').convert_alpha(),
            3: pygame.image.load('assets/levels/level3/level3.png').convert_alpha(),
        }

    def loadLevel(self):
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        self.interactableSprites.empty()
        csvLayouts = self.csvLayouts
        tilesGraphics = self.tilesGraphics
        for style, layout in csvLayouts[self.level].items():  # iterate, read and add each layer in the level
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row): # Cal is the value in the csv file at (row_index, col_index)
                    # Load respective level
                    if self.level == 0:
                        if val != '-1':
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            if style == 'void':
                                Tile((x, y), [], [self.interactableSprites], 'void', self.level, tilesGraphics[1]['qgates'][int(val)], 1, deflate=(-40, -40))
                            elif style == 'interactions':
                                if 25 <= col_index <=26 and 7 <= row_index <= 9:
                                    if row_index == 9:
                                        Tile((x, y), [self.visible_sprites], [self.visibleSprites, self.interactableSprites], 'stairs down', self.level, tilesGraphics[1]['qgates'][int(val)], 1)
                                    else:
                                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], [self.visibleSprites, self.obstacleSprites], 'stairs down', self.level, tilesGraphics[1]['qgates'][int(val)], 1)
                                if col_index == 12 and row_index == 6: 
                                    Tile((x, y), [self.visible_sprites], [self.visibleSprites, self.interactableSprites], 'X Gate', self.level, tilesGraphics[1]['qgates'][int(val)], 1)
                            elif style == 'player' and val == '0':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.game)
                                print(x, y)
                            elif style == 'npc' and val == '0':
                                self.cat = Cat((x, y), [self.visible_sprites], self.obstacle_sprites, self.player, self.game)
                            elif style == 'wall_stem':
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], [self.visibleSprites, self.obstacleSprites], 'wall', self.level, tilesGraphics[1]['wall'][int(val)], 1)
                            elif style == 'wall_ceiling':
                                Tile((x, y), [self.visible_sprites], [self.visibleSprites], 'wall',  self.level,tilesGraphics[1]['wall'][int(val)], 21)
                    elif self.level == 4:
                        if val != '-1':
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            # print(f"[{row_index}, {col_index}, {val}]")
                            if style == 'shadow':
                                Tile((x, y), [self.visible_sprites], 'shadow', self.level, tilesGraphics[self.level]['shadow'][int(val)], 0)
                            elif style == 'shadow2':
                                Tile((x, y), [self.visible_sprites], 'shadow', self.level, tilesGraphics[self.level]['props2'][int(val)], 0)
                            elif style == 'shadow_plant':
                                Tile((x, y), [self.visible_sprites], 'shadow', self.level, tilesGraphics[self.level]['shadow_plant'][int(val)], 0)
                            elif style == 'plants':
                                Tile((x, y), [self.visible_sprites], 'plant', self.level, tilesGraphics[self.level]['plant'][int(val)], 1)
                            elif style == 'wall2_stem':
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], self.level, 'wall', tilesGraphics[self.level]['wall'][int(val)], 2)
                            elif style == 'wall_stem':
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], self.level, 'wall', tilesGraphics[self.level]['wall'][int(val)], 3)
                            elif style == 'props_stem':
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], self.level, 'prop', tilesGraphics[self.level]['props'][int(val)], 4)
                            elif style == 'props2_stem':
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], self.level, 'prop', tilesGraphics[self.level]['props2'][int(val)], 4)
                            elif style == 'trees_stem':
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], self.level, 'tree', tilesGraphics[self.level]['plant'][int(val)], 4)
                            elif style == 'struct':
                                Tile((x, y), [self.visible_sprites], self.level, 'struct', tilesGraphics[self.level]['struct'][int(val)], 4)
                            elif style == 'props':
                                Tile((x, y), [self.visible_sprites], self.level, 'prop', tilesGraphics[self.level]['props'][int(val)], 10)
                            elif style == 'props2':
                                Tile((x, y), [self.visible_sprites], self.level, 'prop', tilesGraphics[self.level]['props2'][int(val)], 20)
                            elif style == 'trees_ceiling':
                                Tile((x, y), [self.visible_sprites], self.level, 'tree', tilesGraphics[self.level]['plant'][int(val)], 20)
                            elif style == 'struct_ceiling':
                                Tile((x, y), [self.visible_sprites], self.level, 'struct', tilesGraphics[self.level]['struct'][int(val)], 20)
                            elif style == 'wall2_ceiling':
                                Tile((x, y), [self.visible_sprites], self.level, 'wall', tilesGraphics[self.level]['wall'][int(val)], 20)
                            elif style == 'wall_ceiling':
                                Tile((x, y), [self.visible_sprites], self.level, 'wall', tilesGraphics[self.level]['wall'][int(val)], 21)
                            elif style == 'player' and val == '0':
                                self.player = Player((x, y),
                                                    [self.visible_sprites],
                                                    self.obstacle_sprites, self.game)
                                                    #  self.create_attack,
                                                    #  self.destroy_attack,
                                                    #  self.create_skill,
                                                    #  self.destroy_skill,
                                                    #  self.create_burst,
                                                    #  self.destroy_burst)
                            elif style == 'npc' and val == '0':
                                self.cat = Cat((x, y), [self.visible_sprites], self.obstacle_sprites, self.player, self.game)
                    elif self.level == 10:
                        if val != '-1':
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            # print(f"[{row_index}, {col_index}, {val}]")
                            if style == 'void_toggle':
                                Tile((x, y), [self.visible_sprites], 'interactable', self.level, tilesGraphics[self.level]['props'][int(val)], 1)
                            elif style == 'interactions_passable':
                                Tile((x, y), [self.visible_sprites], 'interactable', self.level, tilesGraphics[self.level]['props'][int(val)], 1)
                            elif style == 'interactions_passable2':
                                Tile((x, y), [self.visible_sprites], 'interactable', self.level, tilesGraphics[self.level]['props2'][int(val)], 1)
                            elif style == 'interactions':
                                Tile((x, y), [self.visible_sprites], 'interactable', self.level, tilesGraphics[self.level]['props'][int(val)], 1)
                            elif style == 'interactions_ceiling':
                                Tile((x, y), [self.visible_sprites], 'interactable', self.level, tilesGraphics[self.level]['props'][int(val)], 20)
                            elif style == 'wall_ceiling':
                                Tile((x, y), [self.visible_sprites], self.level, 'wall', tilesGraphics[self.level]['wall'][int(val)], 20)
                            elif style == 'wall_stem':
                                Tile((x, y), [self.visible_sprites], self.level, 'wall', tilesGraphics[self.level]['wall'][int(val)], 21)
                            elif style == 'player' and val == '0':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.game)
                            elif style == 'npc' and val == '0':
                                self.cat = Cat((x, y), [self.visible_sprites], self.obstacle_sprites, self.player, self.game)
                    elif self.level == 1:
                        if val != '-1':
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            if style == 'wall_stem':
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], [self.visibleSprites, self.obstacleSprites], 'wall', self.level, tilesGraphics[self.level]['wall'][int(val)], 1)
                            elif style == 'wall_ceiling':
                                Tile((x, y), [self.visible_sprites], [self.visibleSprites], 'wall',  self.level,tilesGraphics[self.level]['wall'][int(val)], 21)
                            elif style == 'interactions':
                                if 3 <= col_index <=5 and 24 <= row_index <= 25:
                                    if col_index == 5:
                                        Tile((x, y), [self.visible_sprites], [self.visibleSprites, self.interactableSprites], 'stairs down', self.level, tilesGraphics[self.level]['qgates'][int(val)], 1)
                                    else:
                                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], [self.visibleSprites, self.obstacleSprites], 'stairs down', self.level, tilesGraphics[self.level]['qgates'][int(val)], 1)
                                else:
                                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], [self.visibleSprites, self.obstacleSprites], 'interactable', self.level, tilesGraphics[self.level]['qgates'][int(val)], 1)
                            elif style == 'interactions_ceiling':
                                Tile((x, y), [self.visible_sprites], [self.visibleSprites], 'interactable', self.level, tilesGraphics[self.level]['qgates'][int(val)], 20)
                            elif style == 'interactions_passable':
                                interaction = 'none'
                                if col_index == 25 and 12 <= row_index <= 20: interaction = 'X Gate' # X Gate
                                elif col_index in [5, 9] and row_index == 15: interaction = 'Quantum Pressure Plate'# Quantum Pressure Plate
                                elif col_index == 7 and row_index == 15: interaction = 'H Gate'# H Gate
                                elif 6 <= col_index <= 8 and row_index == 22: interaction = 'Quantum Seal'# Quantum Seal
                                Tile((x, y), [self.visible_sprites], [self.visibleSprites, self.interactableSprites], interaction, self.level, tilesGraphics[self.level]['qgates'][int(val)], 1)
                            elif style == 'void_toggle':
                                Tile((x, y), [self.obstacle_sprites], [self.obstacle_sprites, self.interactableSprites], 'void_toggle', self.level, tilesGraphics[self.level]['qgates'][int(val)], 1)
                            elif style == 'player' and val == '0':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.game)
                                # print(f"Player Spawn: {self.player.rect.topleft}")
                            elif style == 'npc' and val == '0':
                                self.cat = Cat((x, y), [self.visible_sprites], self.obstacle_sprites, self.player, self.game)
                    elif self.level == 2:
                        if val != '-1':
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            if style == 'wall_stem':
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], [self.visibleSprites, self.obstacleSprites], 'wall', self.level, tilesGraphics[1]['wall'][int(val)], 2)
                            elif style == 'wall_ceiling':
                                Tile((x, y), [self.visible_sprites], [self.visibleSprites], 'wall',  self.level,tilesGraphics[1]['wall'][int(val)], 21)
                            elif style == 'interactions':
                                interaction = 'none'
                                if col_index == 7 and row_index == 19: interaction = 'H Gate' # H Gate
                                elif col_index == 15 and row_index == 19: interaction = 'bell' # Bell
                                elif col_index == 23 and row_index == 19: interaction = 'Quantum Pressure Plate'
                                elif col_index == 13 and row_index == 14: interaction = 'door 1'
                                elif col_index == 17 and row_index == 14: interaction = 'door 2'
                                elif col_index == 3 and 24 <= row_index <= 25: interaction = 'stairs up'
                                elif 4 <= col_index <=5 and 24 <= row_index <= 25:
                                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], [self.visibleSprites, self.obstacleSprites, self.interactableSprites], 'stairs up', self.level, tilesGraphics[1]['qgates'][int(val)], 1)
                                dummy = Tile((x, y), [self.visible_sprites], [self.visibleSprites, self.interactableSprites], interaction, self.level, tilesGraphics[1]['qgates'][int(val)], 1)  
                                if interaction == 'bell': self.levelProperties[2]["bell"] = dummy 
                            elif style == 'void':
                                Tile((x, y), [], [self.interactableSprites], 'void', self.level, tilesGraphics[1]['qgates'][int(val)], 1, deflate=(-30, -30))
                            elif style == 'player':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.game)
                                print((x, y))
                            elif style == 'npc' and val == '0':
                                self.cat = Cat((x, y), [self.visible_sprites], self.obstacle_sprites, self.player, self.game)
                    elif self.level == 3:
                        if val != '-1':
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            if style == 'wall_stem':
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], [self.visibleSprites, self.obstacleSprites], 'wall', self.level, tilesGraphics[1]['wall'][int(val)], 2)
                            elif style == 'wall_ceiling':
                                Tile((x, y), [self.visible_sprites], [self.visibleSprites], 'wall',  self.level,tilesGraphics[1]['wall'][int(val)], 21)
                            elif style == 'interactions':
                                interaction = 'none'
                                if col_index == 15 and row_index == 3: interaction = 'H Gate' # H Gate
                                elif col_index == 15 and row_index == 10: interaction = 'X Gate' # X Gate
                                elif (col_index == 4 and row_index == 9) or (col_index == 6 and row_index == 11): interaction = 'Quantum Pressure Plate'
                                elif col_index == 13 and row_index == 14: interaction = 'door 1'
                                elif col_index == 17 and row_index == 14: interaction = 'door 2'
                                elif 20 <= col_index <= 23 and 7 <= row_index <= 8: 
                                    interaction = 'toggle bridge'
                                    dummy = Tile((x, y), [self.visible_sprites], [self.visibleSprites, self.interactableSprites], 'stairs down', self.level, tilesGraphics[1]['qgates'][int(val)], 1)
                                    dummy.invisible = True
                                elif col_index == 24 and 6 <= row_index <= 7: interaction = 'stairs down'
                                elif 25 <= col_index <=26 and 6 <= row_index <= 7:
                                    dummy = Tile((x, y), [self.visible_sprites, self.obstacle_sprites], [self.visibleSprites, self.obstacleSprites, self.interactableSprites], 'stairs down', self.level, tilesGraphics[1]['qgates'][int(val)], 1)
                                    if interaction == 'bell': self.levelProperties[2]["bell"] = dummy
                                Tile((x, y), [self.visible_sprites], [self.visibleSprites, self.interactableSprites], interaction, self.level, tilesGraphics[1]['qgates'][int(val)], 1)   
                            elif style == 'void':
                                Tile((x, y), [], [self.interactableSprites], 'void', self.level, tilesGraphics[1]['qgates'][int(val)], 1, deflate=(-30, -30))
                            elif style == 'void_toggle':
                                Tile((x, y), [], [self.interactableSprites], 'void_toggle', self.level, tilesGraphics[1]['qgates'][int(val)], 1)
                            elif style == 'player':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.game)
                                print((x, y))
                            elif style == 'npc' and val == '0':
                                self.cat = Cat((x, y), [self.visible_sprites], self.obstacle_sprites, self.player, self.game)
                    elif self.level == 20:
                        if val != '-1':
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            # print(f"[{row_index}, {col_index}, {val}]")
                            if style == 'interactions_passable' or style == 'interactions_passable2':
                                if 16 <= col_index <= 17 and 10 <= row_index <= 12: # Make H Gate transparent
                                    Tile((x, y), [self.visible_sprites, self.quantumGate_sprites], 'interactable', self.level, tilesGraphics[self.level]['interactions'][int(val)], 20, alpha=128)
                                else:
                                    Tile((x, y), [self.visible_sprites], 'interactable', self.level, tilesGraphics[self.level]['interactions'][int(val)], 1)
                            elif style == 'interactions':
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'interactable', self.level, tilesGraphics[self.level]['interactions'][int(val)], 1)
                            elif style == 'interactions_ceiling':
                                Tile((x, y), [self.visible_sprites], 'interactable', self.level, tilesGraphics[self.level]['interactions'][int(val)], 20)
                            elif style == 'wall_ceiling':
                                Tile((x, y), [self.visible_sprites], 'wall', self.level, tilesGraphics[self.level]['wall'][int(val)], 20)
                            elif style == 'wall_stem':
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], self.level, 'wall', tilesGraphics[self.level]['wall'][int(val)], 1)
                            elif style == 'player' and val == '0':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.game)
                            elif style == 'npc' and val == '0':
                                self.cat = Cat((x, y), [self.visible_sprites], self.obstacle_sprites, self.player, self.game)

        # Init Quantum Computer for Level
        self.qubitNo = self.levelProperties[self.level]["qubit amount"]
        circuit_model = CircuitGridModel(self.qubitNo, 4)

        self.circuitGrid = CircuitGrid(circuit_model, self.game)
        self.stateMarkers = stateUI.StateMarkers(self.qubitNo)
        self.quantumComputer = QuantumComputer(self.stateMarkers, self.circuitGrid)
    def update(self, deltaTime, actions):
        self.visible_sprites.update()
        self.quantumComputer.update()
        self.circuitGrid.handle_input()
        self.circuitGrid.update()
        self.levelLogic()

    def render(self, window):
        self.visible_sprites.custom_draw(self.player, window)
        self.levelUI.customDraw(window)
        self.cat.custom_draw(window)
        if self.game.actions["toggleCircuitGrid"]:
            # self.moving_sprites.draw(window)
            self.circuitGrid.draw(window)
            self.stateMarkers.custom_draw(window)
            self.player.enabled_movement = False
            if self.player.superposition:
                self.player.collapseSuperposition()
                self.player.image.set_alpha(255)
        elif self.game.actions["toggleTutorial"]:
            self.player.enabled_movement = False
        else: 
            self.player.enabled_movement = True
            

    def levelLogic(self):
        if self.level == 0:
            for sprite in self.interactableSprites:
                if sprite.hitbox.colliderect(self.player.hitbox):
                    if sprite.spriteType == 'X Gate' and not self.player.superposition:
                        sprite.kill()
                        self.levelUI.updateCount('X', 1)
                        self.player.quantumSpellBook['X'] += 1
                    elif sprite.spriteType == 'void':
                        if self.player.superposition:
                            for superpositionSprite in self.player.superpositionSprites:
                                if sprite.hitbox.colliderect(superpositionSprite.hitbox):
                                    print("superposed collided")
                                    self.player.respawn(self.levelProperties[self.level]["spawn point"])
                        else: 
                            self.player.respawn(self.levelProperties[self.level]["spawn point"])
                            print("collided")
                    elif sprite.spriteType == 'stairs down' and not self.player.superposition:
                        self.levelUI.resetCount()
                        self.level = 1
                        self.loadLevel()
        elif self.level == 1:
            self.levelProperties[self.level]['progress'] = 1 if self.player.rect.topleft[0] <= 400 else 0
            for sprite in self.interactableSprites:
                if sprite.hitbox.colliderect(self.player.hitbox) and not self.player.superposition:
                    if sprite.spriteType == 'X Gate':
                        sprite.kill()
                        self.levelUI.updateCount('X', 1)
                        self.player.quantumSpellBook['X'] += 1
                    elif sprite.spriteType == 'H Gate':
                        sprite.kill()
                        self.levelUI.updateCount('H', 1)
                        self.player.quantumSpellBook['H'] += 2
                    elif sprite.spriteType == 'stairs down' and self.levelProperties[1]["stairs down unlocked"]:
                        self.levelUI.resetCount()
                        self.level = 3
                        self.loadLevel()
                if self.player.superposition:
                    if sprite.spriteType == 'Quantum Pressure Plate':
                        sprite.properties['pressed'] = False
                        for superpositionSprite in self.player.superpositionSprites:
                            if sprite.hitbox.colliderect(superpositionSprite.hitbox):
                                sprite.properties['pressed'] = True
                                break
                        sprite.image = self.tilesGraphics[self.level]['qgates'][31 if sprite.properties['pressed'] else 30]

                        pressurePlateSprites = [sprite for sprite in self.interactableSprites if sprite.spriteType == 'Quantum Pressure Plate']
                        if pressurePlateSprites[0].properties['pressed'] and pressurePlateSprites[1].properties['pressed']:
                            self.levelProperties[1]["stairs down unlocked"] = True
                            for sprite in self.interactableSprites:
                                if sprite.spriteType == 'Quantum Seal' or sprite.spriteType == 'void_toggle':
                                    sprite.kill()
        elif self.level == 2:
            for sprite in self.interactableSprites:
                if sprite.hitbox.colliderect(self.player.hitbox):
                    if sprite.spriteType == 'H Gate':
                        sprite.kill()
                        self.levelUI.updateCount('H', 1)
                        self.player.quantumSpellBook['H'] += 1
                    elif sprite.spriteType == 'door 1' or sprite.spriteType == 'door 2':
                        print("collided w door")
                        self.level = 3
                        self.levelUI.resetCount()
                        self.loadLevel()
                    elif sprite.spriteType == 'stairs up':
                        pass
                    elif sprite.spriteType == 'void':
                        if self.player.superposition:
                            for superpositionSprite in self.player.superpositionSprites:
                                if sprite.hitbox.colliderect(superpositionSprite.hitbox):
                                    self.player.respawn(self.levelProperties[self.level]["spawn point"])
                        else: self.player.respawn(self.levelProperties[self.level]["spawn point"])
            #     if self.player.superposition:
            #         if sprite.spriteType == 'Quantum Pressure Plate':
            #             sprite.properties['pressed'] = False
            #             for superpositionSprite in self.player.superpositionSprites:
            #                 if sprite.hitbox.colliderect(superpositionSprite.hitbox):
            #                     sprite.properties['pressed'] = True
            #                     break
            #             sprite.image = self.tilesGraphics[1]['qgates'][31 if sprite.properties['pressed'] else 30]
            #             if sprite.properties['pressed'] and not self.levelProperties[self.level]["pressedCooldown"]:
            #                 self.levelProperties[self.level]["pressedCooldown"] = 1
            #                 self.levelProperties[2]["bell state"] = not self.levelProperties[2]["bell state"]
            #             if not sprite.properties['pressed']:
            #                 self.levelProperties[self.level]["pressedCooldown"] = 0
            #             print(self.levelProperties[2]["bell"])
            # if self.levelProperties[2]["bell"] is not None:
            #     print(self.levelProperties[2]["bell"])
            #     if self.levelProperties[2]["bell state"]:
            #         self.levelProperties[2]["bell"].image.set_alpha(self.levelProperties[2]["bell"].wave_value(speed=0.05))
            #     else: self.levelProperties[2]["bell"].image.set_alpha(255)
                if self.player.superposition:
                    for superpositionSprite in self.player.superpositionSprites:
                        if 0 < superpositionSprite.amplitude < 0.9:
                            if sprite.hitbox.colliderect(superpositionSprite.hitbox):
                                if sprite.spriteType == 'bell':
                                    self.player.entangled = True
            if self.levelProperties[2]["bell"] is not None:
                self.levelProperties[2]["bell"].image.set_alpha(self.levelProperties[2]["bell"].wave_value(speed=0.05))
                self.levelProperties[2]["bell state"] = randint(0, 1)
        elif self.level == 3:
            for sprite in self.interactableSprites:
                if sprite.hitbox.colliderect(self.player.hitbox):
                    if sprite.spriteType == 'X Gate':
                        sprite.kill()
                        self.levelUI.updateCount('X', 1)
                        self.player.quantumSpellBook['X'] += 1
                    elif sprite.spriteType == 'H Gate':
                        sprite.kill()
                        self.levelUI.updateCount('H', 1)
                        self.player.quantumSpellBook['H'] += 1
                    elif sprite.spriteType == 'door 1' or sprite.spriteType == 'door 2':
                        print("collided w door")
                        self.levelUI.resetCount()
                        self.level = 2
                        self.loadLevel()
                    elif sprite.spriteType == 'stairs up':
                        pass
                    elif sprite.spriteType == 'void':
                        if self.player.superposition:
                            for superpositionSprite in self.player.superpositionSprites:
                                if sprite.hitbox.colliderect(superpositionSprite.hitbox):
                                    self.player.respawn(self.levelProperties[self.level]["spawn point"])
                        else: self.player.respawn(self.levelProperties[self.level]["spawn point"])

                if self.player.superposition:
                    if sprite.spriteType == 'Quantum Pressure Plate':
                        sprite.properties['pressed'] = False
                        for superpositionSprite in self.player.superpositionSprites:
                            if sprite.hitbox.colliderect(superpositionSprite.hitbox):
                                sprite.properties['pressed'] = True
                                break
                        sprite.image = self.tilesGraphics[1]['qgates'][31 if sprite.properties['pressed'] else 30]

                        pressurePlateSprites = [sprite for sprite in self.interactableSprites if sprite.spriteType == 'Quantum Pressure Plate']
                        if pressurePlateSprites[0].properties['pressed'] and pressurePlateSprites[1].properties['pressed']:
                            self.levelProperties[self.level]["stairs down unlocked"] = True
                            for sprite in self.interactableSprites:
                                if sprite.spriteType == 'toggle bridge':
                                    sprite.invisible = False
                                if sprite.spriteType == 'void_toggle':
                                    sprite.kill()

            


        # Respawn player if out of bounds
        if not (0 < self.player.rect.topleft[0] < 960 and 0 < self.player.rect.topleft[1] < 960):
            self.player.respawn(self.levelProperties[self.level]["spawn point"])
