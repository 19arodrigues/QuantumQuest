from state import State
from level import Level
from assets.settings import *
from assets.resources import Font
import pygame
from math import sin

class Title(State):
    def __init__(self, game):
        super().__init__(game, 'title')
        self.font = Font(80)
        self.subFont = Font(40)
    
    def update(self, deltaTime, actions):
        if actions["enter"]:
            newState = Level(self.game)
            newState.enterState()
            print("Entering Level")
        self.game.reset_keys()

    def render(self, window):
        window.fill((255, 255, 255))
        titleSurface = self.font.font.render("QuantumQuest: Prologue", True, RED)
        subTitleSurface = self.subFont.font.render("Press 'Enter' to Start", True, GRAY)
        instructionSurface = self.subFont.font.render("Press 'W', 'A', 'S', and 'D' to move in game", True, GRAY)
        window.blit(titleSurface, (WINDOW_WIDTH/2 - titleSurface.get_width()/2, WINDOW_HEIGHT/2 - titleSurface.get_height()/2))
        subTitleSurface.set_alpha(self.wave_value(speed=0.05))
        window.blit(subTitleSurface, (WINDOW_WIDTH/2 - subTitleSurface.get_width()/2, WINDOW_HEIGHT/2 + titleSurface.get_height()/2 + 20))
        window.blit(instructionSurface, (WINDOW_WIDTH/2 - instructionSurface.get_width()/2, WINDOW_HEIGHT/2 + instructionSurface.get_height()/2 + 140))

    def wave_value(self, offset = 0, speed = 1, baseValue=0):
        return 255*min((sin(speed*pygame.time.get_ticks()/20+offset)**2 + baseValue), 1)
