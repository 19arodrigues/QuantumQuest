import pygame
from superSprite import SuperSprite
from math import sin

class Entity(SuperSprite):
    def __init__(self, groups):
        super().__init__(groups)
        self._layer = -2
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.ignoreCollisions = False
        self.collided = False

        # Quantum Properties
        self.quantumState = None

        # Movement Variables
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        direction = pygame.math.Vector2(self.direction)
        
        if direction.magnitude() != 0:
            direction = direction.normalize()

        self.collided = False
        self.hitbox.x += direction.x * speed
        horizontalCollision = self.collision("horizontal")
        self.hitbox.y += direction.y * speed
        verticalCollision = self.collision("vertical")
        self.rect.center = self.hitbox.center
        self.collided = horizontalCollision or verticalCollision
        # print(f"Entity: {self.hitbox.x}, {self.hitbox.y}, collided?: {self.collided}")


    def collision(self, direction):
        if not self.ignoreCollisions and self.obstacleSprites is not None:
            if direction == "horizontal":
                for sprite in self.obstacleSprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        # print(sprite._layer)
                        if self.direction.x > 0:  # Moving Right | Collision on Right : Keep Left
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # Moving Left | Collision on Left : Keep Right
                            self.hitbox.left = sprite.hitbox.right
                        return True
            elif direction == "vertical":
                for sprite in self.obstacleSprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        # print(sprite._layer)
                        if self.direction.y > 0:  # Moving Down | Collision on bottom : Move Up
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # Moving Up | Collision on Top : Move Down
                            self.hitbox.top = sprite.hitbox.bottom
                        return True
            
    def wave_value(self, offset = 0, speed = 1, baseValue=0):
        return 255*min((sin(speed*pygame.time.get_ticks()/20+offset)**2 + baseValue), 1)
