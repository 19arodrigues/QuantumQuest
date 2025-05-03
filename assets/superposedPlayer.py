import pygame
import copy
from assets.entity import Entity
from assets.resources import importFolder
from assets.settings import TEAM


class SuperposedPlayer(Entity):
    def __init__(self, groups, obstacleSprites, player, offset, quantumState):
        super().__init__(groups)

        self.obstacleSprites = obstacleSprites
        self.player = player
        self.offset = offset
        self.quantumState = quantumState
        self.amplitude = 0

        # Animation Variables
        self.importAssets(TEAM[0])
        # self.animations = copy.deepcopy(self.player.animations)
        self.frame_index = self.player.frame_index
        self.animationSpeed = self.player.animationSpeed
        self.status = self.player.status
        self.enabledMovement = True
        self.speed = self.player.speed
        self.direction = self.player.direction
        self.image = self.animations[self.status][int(self.frame_index)]
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(topleft = pygame.math.Vector2(self.player.rect.x, self.player.rect.y) + offset)
        self.hitbox = self.rect
        # self.ignoreCollisions = False

    def importAssets(self, selected_char: str):
        # Adds the selected character's movement animations to self.animations
        character_path = f'assets/player/{selected_char}/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                        'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': []}
                        #    'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [], }

        for animation in self.animations.keys():
            complete_path = character_path + animation
            self.animations[animation] = importFolder(complete_path)

    def superimposed_animation(self):
        animation = self.animations[self.player.status]
        self.image = animation[int(self.player.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        self.amplitude = self.player.game.stateStack[-1].quantumComputer.probabilities[self.quantumState]
        # print(f"state: {self.quantumState}, speed: {speed}")
        # print(f"SuperposedPlayer: {self.quantumState} {speed}")
        self.image.set_alpha(self.wave_value(speed=self.amplitude*0.05))

    def update(self):
        if self.enabledMovement:
            if self.amplitude:
                # print(self.player.direction)
                # print(f"{self.quantumState}: {self.collided}")
                self.move(self.speed)
                if self.collided:
                    self.player.collapseSuperposition()
                # print(self.hitbox.center)
                # print(self.speed, self.direction)
            self.superimposed_animation()
            # print(f"SuperposedPlayer: {self.hitbox.x}, {self.hitbox.y}, collided?: {self.collided}")
            # if self.amplitude: print(f"State: {self.hitbox.center}, collided?: {self.ignoreCollisions}")
            # if self.collided and self.amplitude: 
            #     print("DEBUG")
                # self.player.collapseSuperposition()
            # if self.amplitude: 
            #     if self.collided:
            #         print(f"{self.quantumState} collided!")
            #     else:
            #         print(f"{self.quantumState} not collided!")
                # print(self.hitbox)
                # print(self.rect.center)
            # for i, sprite in enumerate(self.obstacleSprites):
            #         if i == 369 and self.amplitude:
            #             xdiff = sprite.hitbox.center[0] - self.hitbox.center[0]
            #             ydiff = sprite.hitbox.center[1] - self.hitbox.center[1]
            #             # print(xdiff, ydiff)
            #             print(i, sprite.hitbox.center)
    