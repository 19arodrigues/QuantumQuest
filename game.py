import subprocess
import sys

try:
    import pygame
except ImportError:
    print("pygame not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame
try:
    import qiskit
except ImportError:
    print("qiskit not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "qiskit"])
    import qiskit

import pygame
import time

from assets.settings import *
from level import Level
from title import Title

class Game:
    def __init__(self):
        # Init PyGame, Window, Clock
        pygame.init()
        pygame.display.set_caption('PHYS495')

        # Get user window's spec
        info = pygame.display.Info()
        # System's window size (desktop resolution)
        screen_width = info.current_w
        screen_height = info.current_h
        self.scaleFactor = 1.3
        self.gameCanvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.window = pygame.display.set_mode((WINDOW_WIDTH*self.scaleFactor, WINDOW_HEIGHT*self.scaleFactor))
        self.clock = pygame.time.Clock()

        # Init Game States
        self.running = True
        self.playing = True
        self.actions = {"left": False, "right": False, "up": False, "down": False, 
                        "action_q": False, "action_e": False, "action_r": False, 
                        "action_x": False, "action_y": False, "action_z": False, 
                        "action_h": False, "action_space": False, "action_c": False, 
                        "action_up": False, "action_down": False, "action_left": False, 
                        "action_right": False, 
                        "enter": False, "toggleCircuitGrid": False, "toggleTutorial": False}
        self.cooldowns = {"toggleCircuitGrid": 0, "circuitGridInput": 0, "toggleTutorial": 0}
        self.stateStack = []
        self.load_states()

        # Init Delta Time for Frame Independence
        self.dt = 0
        self.prev_time = 0

    def run(self):
        # START GAME LOOP
        exit = False
        while self.playing:
            self.gameCanvas.fill((0, 0, 0))
            self.getEvents()
            self.update()
            self.render(self.scaleFactor)
            self.clock.tick(FPS)

    def getEvents(self):
        # print(self.cooldowns["circuitGridInput"])
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.playing = False
                    if event.key == pygame.K_w:
                        self.actions["up"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_a:
                        self.actions["left"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_s:
                        self.actions["down"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_d:
                        self.actions["right"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_q:
                        self.actions["action_q"] = True
                    if event.key == pygame.K_e:
                        self.actions["action_e"] = True
                    if event.key == pygame.K_r:
                        self.actions["action_r"] = True
                    if event.key == pygame.K_x:
                        self.actions["action_x"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_y:
                        self.actions["action_y"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_z:
                        self.actions["action_z"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_h:
                        self.actions["action_h"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_SPACE:
                        self.actions["action_space"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_c:
                        self.actions["action_c"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_UP:
                        self.actions["action_up"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_DOWN:
                        self.actions["action_down"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_LEFT:
                        self.actions["action_left"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_RIGHT:
                        self.actions["action_right"] = True
                        self.cooldowns["circuitGridInput"] = 1
                    if event.key == pygame.K_RETURN:
                        self.actions["enter"] = True
                    if event.key == pygame.K_TAB:
                        if self.cooldowns["toggleCircuitGrid"] == 0:
                            if not self.actions["toggleTutorial"]:
                                self.actions["toggleCircuitGrid"] = not self.actions["toggleCircuitGrid"]
                            self.cooldowns["toggleCircuitGrid"] = 1
                            # self.actions["toggleTutorial"] = False
                    if event.key == pygame.K_f:
                        if self.cooldowns["toggleTutorial"] == 0:
                            if self.stateStack[-1].stateName == 'level':
                                if self.stateStack[-1].cat.catPlayerDistance < 30 and not self.actions["toggleCircuitGrid"]:
                                    self.actions["toggleTutorial"] = not self.actions["toggleTutorial"]
                                    self.cooldowns["toggleTutorial"] = 1
                            # self.actions["toggleCircuitGrid"] = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.actions["up"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_a:
                        self.actions["left"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_s:
                        self.actions["down"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_d:
                        self.actions["right"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_q:
                        self.actions["action_q"] = False
                    if event.key == pygame.K_e:
                        self.actions["action_e"] = False
                    if event.key == pygame.K_r:
                        self.actions["action_r"] = False
                    if event.key == pygame.K_x:
                        self.actions["action_x"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_y:
                        self.actions["action_y"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_z:
                        self.actions["action_z"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_h:
                        self.actions["action_h"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_SPACE:
                        self.actions["action_space"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_c:
                        self.actions["action_c"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_UP:
                        self.actions["action_up"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_DOWN:
                        self.actions["action_down"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_LEFT:
                        self.actions["action_left"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_RIGHT:
                        self.actions["action_right"] = False
                        self.cooldowns["circuitGridInput"] = 0
                    if event.key == pygame.K_RETURN:
                        self.actions["enter"] = False
                    if event.key == pygame.K_TAB:
                        self.cooldowns["toggleCircuitGrid"] = 0
                    if event.key == pygame.K_f:
                        self.cooldowns["toggleTutorial"] = 0

    def update(self):
        # Update using the state at the top of the stack
        self.stateStack[-1].update(self.dt, self.actions)

    def render(self, scaleFactor):
        # Render using the state at the top of the stack
        self.stateStack[-1].render(self.gameCanvas)

        scaled_width = int(WINDOW_WIDTH * scaleFactor)
        scaled_height = int(WINDOW_HEIGHT * scaleFactor)

        self.window.blit(pygame.transform.scale(self.gameCanvas, (scaled_width, scaled_height)), (0, 0))
        pygame.display.flip()

    def load_states(self):
        self.titleScreen = Title(self)
        self.stateStack.append(self.titleScreen)

    def getDeltaTime(self):
        # Calculate Delta Time for Frame Independence
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

if __name__ == "__main__":
    game = Game()
    game.run()