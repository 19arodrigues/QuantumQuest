from superSprite import SuperSprite
from assets.resources import Font
from assets.settings import *
import pygame

class LevelUI():
    def __init__(self, level):
        self.level = level.level
        self.levelObject = level
        self.player = level.player
        self.UIcomponents = []
        self.font = Font(40)
        self.bellStateFont = Font(10)
        # X Gate
        self.textSurface = self.font.font.render("INVENTORY: ", True, WHITE)
        self.textRect = self.textSurface.get_rect()
        self.textRect.topright = (10 + self.textRect.width, 10)
        
        self.UIcomponents.append(UIcomponent('X', level.tilesGraphics[1]['qgates'][int(82)], (self.textRect.topright[0] - 15 , 10)))
        self.UIcomponents.append(UIcomponent('H', level.tilesGraphics[1]['qgates'][int(81)], (self.UIcomponents[0].startPos[0] + self.UIcomponents[0].image.get_width() + 60, 10)))
        self.UIcomponents.append(UIcomponent('lives', level.tilesGraphics[1]['qgates'][int(83)], (WINDOW_WIDTH - 160, 10), count=level.player.lives))

        # playerSurface = level.tilesGraphics[1]['qgates'][int(83)]
        bellSurface = level.tilesGraphics[1]['qgates'][int(80)]
        entangledSurfaces = [level.tilesGraphics[1]['qgates'][int(84)], level.tilesGraphics[1]['qgates'][int(85)]]
        # self.playerSprite = pygame.transform.scale(playerSurface.convert_alpha(), playerSurface, playerSurface.get_height()) 
        self.bellSprite = pygame.transform.scale(bellSurface.convert_alpha(), (bellSurface.get_width(), bellSurface.get_height()))
        self.entagledSprites = [pygame.transform.scale(entangledSurfaces[0].convert_alpha(), (entangledSurfaces[0].get_width()*6, entangledSurfaces[0].get_height()*6)),
                                pygame.transform.scale(entangledSurfaces[1].convert_alpha(), (entangledSurfaces[0].get_width()*6, entangledSurfaces[0].get_height()*6))]
        self.bellStates = {0: [self.bellStateFont.font.render("|0>", True, WHITE), self.bellStateFont.font.render("|1>", True, WHITE)],
                           1: [self.bellStateFont.font.render("|00>", True, WHITE), self.bellStateFont.font.render("|11>", True, WHITE)]}
        
    def customDraw(self, window):
        window.blit(self.textSurface, self.textRect)
        for component in self.UIcomponents:
            component.update(window)
        if self.levelObject.level == 2:
            superPositionSprite = None
            for superpositionSprite in self.player.superpositionSprites:
                if superpositionSprite.amplitude and self.player.entangled:
                    superPositionSprite = superpositionSprite
            self.draw_sprite_pair_with_circle(window, WINDOW_WIDTH - 50, WINDOW_HEIGHT - 130, superPositionSprite, self.bellSprite, self.entagledSprites)

            

    def updateCount(self, type, count):
        for component in self.UIcomponents:
            if component.uiType == type:
                component.count += count
        
    def resetCount(self, resetLives=False):
        for component in self.UIcomponents:
            if resetLives and component.uiType == 'lives':
                component.count = 4
            else:
                component.count = 0

    def draw_sprite_pair_with_circle(self, window, x, y, sprite_a, sprite_b, circleArray):
        # Draw the circle centered around the pair
        circleSprite = circleArray[(pygame.time.get_ticks() // 1000) % 2]
        circle_rect = circleSprite.get_rect(center=(x - 64, y + 16))  # since 64x32 is the bounding box
        window.blit(circleSprite, circle_rect.topleft)

        bellStates = int(sprite_a is not None)
        sprite_b.set_alpha(self.player.wave_value(speed=0.05))
        if bellStates:
            x -= 10
            sprite_a = sprite_a.image
            window.blit(sprite_a, (x, y))
            window.blit(sprite_a, (x - 96, y))
        # Draw the two sprites next to each other inside the circle
        
        window.blit(sprite_b, (x - 32, y))
        window.blit(sprite_b, (x - 128, y))
        window.blit(self.bellStates[bellStates][0], (x - 26 + 13*bellStates, y + 32))
        window.blit(self.bellStates[bellStates][1], (x - 122 + 13*bellStates, y + 32))


class UIcomponent(SuperSprite):
    def __init__(self, uiType, surface, startPos=(0, 0), count=0):
        super().__init__(spriteType='UIcomponent')
        self.count = count
        scaleFactor = 2
        self.image = pygame.transform.scale(surface.convert_alpha(), (surface.get_width()*scaleFactor, surface.get_height()*scaleFactor)) 
        self.rect = self.image.get_rect()
        self.font = Font(40)
        self.uiType = uiType
        self.startPos = startPos

    def update(self, window):
        super().update()
        textSurface = self.font.font.render(f"{self.count}x", True, WHITE)
        window.blit(self.image, (self.startPos[0] + 3, self.startPos[1] - 5))
        window.blit(textSurface, (self.startPos[0] + self.image.get_width(), self.startPos[1]))
