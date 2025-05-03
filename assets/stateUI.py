# Credit for outline func to : https://github.com/lordmauve/pgzero/tree/main

import pygame.sprite

from assets.resources import Font
from assets.settings import *
from math import pi, sin, cos

FIELD_HEIGHT = round(WINDOW_HEIGHT * 0.7)
FIELD_WIDTH = WINDOW_WIDTH
WIDTH_UNIT = round(WINDOW_WIDTH/100)

class StateMarker(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, state=0, qubitAmt=2):
        super().__init__()
        self.font = Font(60)
        self.text = BASIS_STATES[qubitAmt-1][state]
        self.image = self.font.font.render(self.text, 1, (255, 255, 255)) # .convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        super().update()
        self.image.set_alpha(self.image.get_alpha())

    def updateColour(self, colour):
        oldAlpha = self.image.get_alpha()
        self.image = self.font.font.render(self.text, True, colour)
        self.image.set_alpha(oldAlpha)

class StateMarkers():
    def __init__(self, qubitAmt=2):
        self.markers  = []
        noOfStates = 2 ** qubitAmt
        self.qubitAmt = qubitAmt
        font = Font()
        self.radius = 200
        self.textWidth = 0
        self.circle_cache = {}
        for i in range(noOfStates):
            text = font.font.render(BASIS_STATES[qubitAmt-1][i], 1, (255, 255, 255))
            x = WINDOW_WIDTH/2 + self.radius*sin(i * (2*pi) / noOfStates) - text.get_width()/2 + 15
            y = (WINDOW_HEIGHT/3 + 7*WINDOW_HEIGHT/100) -self.radius*cos(i * (2*pi) / noOfStates) + text.get_height()/2
            self.markers.append(StateMarker(x, y, i, self.qubitAmt))
            self.textWidth = max(text.get_width(), self.textWidth)

    def custom_draw(self, window):
        self.draw_state_circle_arcs(window)
        for marker in self.markers:
            # background = pygame.Surface((marker.rect.width, marker.rect.height), pygame.SRCALPHA)
            # background.fill((0, 0, 0, 128))
            # window.blit(background, marker.rect.topleft)

            radius = self.textWidth // 2 + 5 # Padding
            circle_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            circle_pos = (marker.rect.centerx - radius, marker.rect.centery - radius + 5)
            colour = min((155*marker.image.get_alpha()/255) + 100, 255)
            pygame.draw.circle(circle_surf, (colour, colour, colour, 200), (radius, radius), radius)
            window.blit(circle_surf, circle_pos)

            # padding = 15
            # border_radius = 20
            # rect = marker.rect.inflate(padding, padding)
            # background = pygame.Surface(rect.size, pygame.SRCALPHA)
            # colour = max(marker.image.get_alpha(), 200)
            # color_with_alpha = (colour, colour, colour, 200)
            # pygame.draw.rect(background, color_with_alpha, background.get_rect(), border_radius=border_radius)
            # window.blit(background, (rect.topleft[0]+5, rect.topleft[1]+8))

            window.blit(self.outlineText(marker), marker.rect)
            # window.blit(marker.image, marker.rect)
            if marker.image.get_alpha() > 50:
                rotated_marker = pygame.transform.rotate(marker.image, 90)
                window.blit(rotated_marker, (15, WINDOW_HEIGHT - rotated_marker.get_height() - 45))


    def draw_state_circle_arcs(self, window, color=WHITE):
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2 
        num_points = 120
        pixel_size = 20
        circleRadius = 220

        arc_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        # pixel = pygame.Surface((pixel_size, pixel_size), pygame.SRCALPHA)
        for i in range(num_points):
            angle = 2 * pi * i / num_points
            subAngle = self.radToDeg(angle) % ((360) / (2**self.qubitAmt))
            # print(f"{subAngle} = {self.radToDeg(angle)} % {((360) / (2**3))}")
            # print(f"angle: {self.degToRad(subAngle)} > subAngle: {self.textWidth/self.radius}")
            if self.degToRad(subAngle) > (self.textWidth*1.4)/self.radius:
                angle = angle - (self.textWidth*1.4)/(2*self.radius)
                x = center_x + circleRadius * sin(angle)
                y = center_y - circleRadius * cos(angle) # 10 is padding
                alpha = 100
                pygame.draw.rect(arc_surface,(*color[:3], alpha), pygame.Rect(round(x), round(y), pixel_size, pixel_size))
            # pygame.draw.rect(window, WHITE, pygame.Rect(round(x), round(y), pixel_size, pixel_size))
            # pixel.fill((255, 255, 255, 100))
            # window.blit(pixel, (round(x), round(y)))
        window.blit(arc_surface, (0, 0))

    def radToDeg(self, rad, integer=True):
        if integer:
            return int(rad * 180 / pi)
        else:
            return rad * 180 / pi
    
    def degToRad(self, deg):
        return deg * pi / 180

    def circlepoints(self, r):
        r = int(round(r))
        if r in self.circle_cache:
            return self.circle_cache[r]
        x, y, e = r, 0, 1 - r
        self.circle_cache[r] = points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points
    
    def outlineText(self, marker, colour=BLACK, outlineWidth=5):
        textsurface = marker.image
        w = textsurface.get_width() + 2 * outlineWidth
        h = textsurface.get_height()

        osurf = pygame.Surface((w, h + 2 * outlineWidth)).convert_alpha()
        osurf.fill((0, 0, 0, 0))

        surf = osurf.copy()

        osurf.blit(marker.font.font.render(marker.text, True, colour).convert_alpha(), (0, 0))

        for dx, dy in self.circlepoints(outlineWidth):
            surf.blit(osurf, (dx + outlineWidth, dy + outlineWidth))

        surf.blit(textsurface, (outlineWidth, outlineWidth))
        return surf
        
