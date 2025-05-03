import pygame
from random import randint
from assets.resources import importFolder

# Skill Class Handles Skill Logic
# SkillEffect Class Handles Skill Sprite and Animations

class Skill:
    def __init__(self, player, spriteGroups):
        self.player = player
        self.character = player.currentCharacter
        self.spriteGroups = spriteGroups

    
    def observe(self):
        # Logic
        
        # Animation
        animations = importFolder(f'assets/player/spells/observe')
        skillEffect = SkillEffect(self.spriteGroups[0], animations, 0.4, self.player.rect.center)
        if self.player.superposition: self.player.collapseSuperposition()

    def castCircuit(self):
        # Logic
        self.player.enterSuperposition()
        # Animation
        

class SkillEffect(pygame.sprite.Sprite):
    def __init__(self, groups, animation, animationSpeed, start_pos, cyclical=False):
        super().__init__(groups)
        # Render Variables
        self._layer = -3

        # Animation Variables
        self.invisible = False
        self.frame_index = 0
        self.animationSpeed = animationSpeed
        self.animation = animation
        self.image = self.animation[0]
        self.rect = self.image.get_rect(center=start_pos)
        self.cyclical = cyclical

        # Movement Variables
        self.direction = pygame.math.Vector2()

    def animate(self):
        self.frame_index += self.animationSpeed
        if self.frame_index >= len(self.animation):
            if self.cyclical: self.frame_index = 0
            else: self.kill()
        else:
            self.image = self.animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.animate()

