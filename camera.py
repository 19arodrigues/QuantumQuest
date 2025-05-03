import pygame
from assets.settings import *

class Camera(pygame.sprite.Group):
    def __init__(self, level):
        # General Setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.level = level
        self.current_level = level.level
        # creating the floor [Lowest Layer]
        self.floor_surf = level.floorGrpahics[self.current_level]
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

        # UI Font
        self.font = pygame.font.SysFont(None, 30)

    def custom_draw(self, player, window):
        # Getting the offset 
        self.offset.x = player.rect.centerx - WINDOW_WIDTH // 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT // 2
        # print(player.rect.center)
        
        # Player Coordinates
        # text_surface = self.font.render(f"{player.rect.topleft}", True, WHITE)
        # text_rect = text_surface.get_rect()
        # text_rect.topright = (WINDOW_WIDTH - 10, 10)
        # window.blit(text_surface, text_rect)
        
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text_surface = self.font.render(f"({mouse_x}, {mouse_y})", True, WHITE)
        text_rect = text_surface.get_rect(topleft=(10, WINDOW_HEIGHT - 30))
        window.blit(text_surface, text_rect)

        # Draw the Floor with offset
        if self.current_level != self.level.level:
            self.current_level = self.level.level
            self.floor_surf = self.level.floorGrpahics[self.current_level]
            self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        floor_offset_pos = self.floor_rect.topleft - self.offset
        window.blit(self.floor_surf, floor_offset_pos)


        def sprite_sort_key(sprite):
            if sprite._layer >= 20:
                return (101 + sprite._layer%10, 0)  # Always last
            
            if sprite._layer == -2:
                return (100, sprite.rect.centery)  # Sort by centery for _layer == -2
            
            return (sprite._layer, sprite.rect.centery)  # Default case: sort by layer first, then centery

        for sprite in sorted(self.sprites(), key=sprite_sort_key):
            if sprite in player.superpositionSprites:
                offset_pos = player.rect.topleft - self.offset + sprite.offset
                pass
                # if sprite.amplitude:
                    # print(offset_pos, "=", player.rect.topleft, "-", self.offset, "+", sprite.offset)
                # sprite.rect = sprite.image.get_rect(topleft = offset_pos)
                # sprite.hitbox = sprite.rect
            else:
                offset_pos = sprite.rect.topleft - self.offset
            if not sprite.invisible:
                window.blit(sprite.image, offset_pos)

            # sprite.rect.topleft = offset_pos
            # inside your game loop, after drawing your sprites:
            pygame.draw.rect(window, (255, 0, 0), sprite.rect, 2)  # red outline with thickness 2
