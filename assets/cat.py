import pygame
from assets.entity import Entity
from assets.resources import importFolder, loadImages
from assets.resources import Font
# import assets.resources
from random import randint
from assets.settings import *

class Cat(Entity):
    direction = pygame.math.Vector2()
    def __init__(self, start_pos, groups, obstacleSprites, player, game):
        super().__init__(groups)

        self.spriteType = 'cat'
        self.catPlayerDistance = 1000

        #Animation Variables
        self.importAssets()
        self.frame_index = 0
        self.animationSpeed = 0.05
        self.status = "idle"
        self.movementStatus = False
        self.moveProbability = 0
        self.speed = 1
        self.direction = Cat.direction
        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(topleft=start_pos)
        self.enabledMovement = True
        
        # Tutorial Varaibles
        self.timeSinceLastHelp = 0
        self.game = game
        

        # Help UI Varaibles
        self.font = Font(10)
        self.catTutorialsImages = loadImages('assets/cat/tutorials', 'catTutorials')
        # Movement Variables
        self.obstacleSprites = obstacleSprites
        self.player = player
        self.ignoreCollisions = True
        # self.hitbox = self.rect.inflate(-10, -20)
        self.hitbox = self.rect

    def importAssets(self):
        # Adds the selected character's movement animations to self.animations
        character_path = f'assets/cat/'
        self.animations = {'walk': [], 'idle': [], 'jump': [], 'interact': [],
                        'idle_animation': [], 'attack': [], 'danger_sense': []}

        for animation in self.animations.keys():
            complete_path = character_path + animation
            self.animations[animation] = importFolder(complete_path)

    def catLogic(self):
        self.catPlayerDistance = (pygame.math.Vector2(self.player.hitbox.center) - pygame.math.Vector2(self.hitbox.center)).magnitude()
        # MOVEMENT LOGIC
        # Change the cat's chance to move every few seconds unless it is far enough from a palyer
        if self.catPlayerDistance > 150:
            self.moveProbability = 100
            Cat.direction = (pygame.math.Vector2(self.player.hitbox.center) - pygame.math.Vector2(self.hitbox.center)).normalize()
            # print(Cat.direction)
        elif self.catPlayerDistance < 50:
            self.moveProbability = 0
        elif(pygame.time.get_ticks() % 10000  == 3000): # Every 3s update move probability
            # print("Updating move probability")
            self.moveProbability = randint(1, 99)
            Cat.direction = (randint(-1, 1), randint(-1, 1))
        if self.moveProbability > 95:
            self.direction = Cat.direction
            self.move(self.speed)
            # print("Cat:", self.direction)
            self.status = "walk"
            # print(f"Cat is moving {self.moveProbability} in direction {Cat.direction}, cat is at pos {self.hitbox.x}, { self.hitbox.y} ")
        else:
            self.status = "idle"

        # INTERACTION LOGIC
        
        # if self.catPlayerDistance + self.timeSinceLastHelp/10 > 300:
        #     print("lemme help")
        # self.timeSinceLastHelp += 1

    def cat_animation(self):
        animation = self.animations[self.status]

        # Iterate through the animation list each method call
        self.frame_index += self.animationSpeed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image.set_alpha(self.wave_value(speed=0.01, baseValue=0.5))
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # # Handle Alpha Value
        # if self.superposition:
        #     self.image.set_alpha(0)
        # elif self.immune:
        #     alpha = self.wave_value()
        #     self.image.set_alpha(alpha)
        # else:
        #     self.image.set_alpha(255)

    def update(self):
        if self.enabledMovement:
            self.catLogic()
            self.cat_animation()
    
    def custom_draw(self, window):
        if self.catPlayerDistance < 30 and not self.player.superposition:
            self.draw_help_box(window, WINDOW_WIDTH/2 + 20, WINDOW_HEIGHT/2 - 50)
            if self.game.actions["toggleTutorial"]:
                level = self.game.stateStack[-1].level
                scaleFactor = 1.3 #level.scaleFactor
                if level == 0:
                    catSurface = self.animations[self.status][int(self.frame_index)]
                    window.blit(pygame.transform.scale(catSurface.convert_alpha(), (catSurface.get_width()*14, catSurface.get_height()*14)), (-70, -85))
                    images = self.catTutorialsImages['catTutorials'][level]
                    for img_name, surface in images.items():
                        if img_name == '1.png':
                            window.blit(pygame.transform.scale(surface, (surface.get_width()*0.32, surface.get_height()*0.32)), (15/scaleFactor, 15/scaleFactor))
                        elif img_name == '2.png':
                            window.blit(pygame.transform.scale(surface, (surface.get_width()*0.37, surface.get_height()*0.37)), (15/scaleFactor, 460/scaleFactor))
                        elif img_name == '3.png':
                            window.blit(pygame.transform.scale(surface, (surface.get_width()*0.15, surface.get_height()*0.15)), (1390/scaleFactor, 475/scaleFactor))
                            window.blit(pygame.transform.flip(pygame.transform.scale(catSurface.convert_alpha(), (catSurface.get_width()*7, catSurface.get_height()*7)), True, False), ((1400-90)/scaleFactor, (720-190)/scaleFactor))
                        elif img_name == '4.png':
                            window.blit(surface, (30, 80))
                            # window.blit(surface, (x, y))
                            # x += surface.get_width() + 10
                elif level == 1:
                    progress = self.game.stateStack[-1].levelProperties[level]['progress']
                    if progress == 0:
                        catSurface = self.animations[self.status][int(self.frame_index)]
                        window.blit(pygame.transform.scale(catSurface.convert_alpha(), (catSurface.get_width()*23, catSurface.get_height()*23)), (650, -70))
                        images = self.catTutorialsImages['catTutorials'][level]
                        for img_name, surface in images.items():
                            if img_name == '1.png':
                                window.blit(pygame.transform.scale(surface, (surface.get_width()*0.4, surface.get_height()*0.4)), (70, 220))
                            elif img_name == '2.png':
                                window.blit(pygame.transform.scale(surface, (surface.get_width()*0.4, surface.get_height()*0.4)), (70, 70))
                    elif progress == 1:
                        catSurface = self.animations[self.status][int(self.frame_index)]
                        window.blit(pygame.transform.flip(pygame.transform.scale(catSurface.convert_alpha(), (catSurface.get_width()*21, catSurface.get_height()*21)), True, False), (490, 10))
                        images = self.catTutorialsImages['catTutorials'][level]
                        for img_name, surface in images.items():
                            if img_name == '3.png':
                                window.blit(pygame.transform.scale(surface, (surface.get_width()*0.235, surface.get_height()*0.235)), (15, 70))
                            elif img_name == '4.png':
                                window.blit(pygame.transform.scale(surface, (surface.get_width()*0.34, surface.get_height()*0.34)), (610, 70))



    def respawn(self, respawnPos):
        self.teleport(respawnPos)

    def teleport(self, teleportPos):
        self.rect.topleft = teleportPos
        self.hitbox.topleft = teleportPos

    def draw_help_box(self, window, x, y):
        # Text rendering
        text_surface = self.font.font.render("I need help!", True, WHITE)
        text_rect = text_surface.get_rect()
        text_surface_extra = self.font.font.render("Press 'F'", True, GRAY)
        text_extra_rect = text_surface_extra.get_rect()

        # Padding around the text
        padding = 10
        rect_width = text_rect.width + 2 * padding + text_extra_rect.width
        rect_height = text_rect.height + 2 * padding

        # Rectangle position
        rect = pygame.Rect(x, y, rect_width, rect_height)

        # Triangle "tail" for speech bubble
        triangle_height = 10
        triangle_width = 12
        triangle = [
            (rect.left, rect.bottom - 10),                # base point at bottom-right
            (rect.left + 5, rect.bottom),# point sticking out right
            (rect.left - 5, rect.bottom + 5)                      # lower base point
        ]
        pygame.draw.polygon(window, BLACK, triangle)
        pygame.draw.polygon(window, WHITE, triangle, 2)

        # Draw white box with black border
        pygame.draw.rect(window, BLACK, rect)
        pygame.draw.rect(window, WHITE, rect, 2)

        # Draw to handle overalp - mirage of one shape
        rect_overlap = pygame.Rect(x, y + 22, 7, 6)
        pygame.draw.rect(window, BLACK, rect_overlap)

        # Blit text centered in the box
        text_pos = (x + padding, y + padding)
        window.blit(text_surface, text_pos)
        window.blit(text_surface_extra, (text_pos[0] + 5 + text_rect.width, text_pos[1]))

    