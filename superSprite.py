from pygame.sprite import Sprite
from pygame import Surface
from assets.settings import TILESIZE

'''
SuperSprite Class implements a custom generic sprite class for QuantumQuest



groups: list of sprite groups the sprite belongs to
sprite_type: type of sprite
- Entity: sprite that moves
    - Player: player controlled sprite
    - NPC: non-player controlled sprite
    - Mob: enemy sprite
- UI: sprite that is part of the user interface
- Tile: sprite that is part of the tile map
@param 


'''

class SuperSprite(Sprite):
    """
    SuperSprite Class implements a custom generic sprite class for QuantumQuest

                pygame.sprite.Sprite
                        |
                    SuperSprite
            |-----------|------------|
            Entity      UI          Tile
    |-------|-------|
    Player  NPC     Mob

            sprite_type (str): Type of sprite.
                image (Surface): Image of the sprite.
                pos (tuple): Position of the sprite.
                layer (int, optional): Layer of the sprite. Defaults to 0.
    """
    def __init__(self, 
                 spriteGroups=None, 
                 spriteType = 'none', 
                 surface = Surface((TILESIZE, TILESIZE)), 
                 start_pos = (0, 0), 
                 layer = 0, 
                 alpha = 255,
                 SuperSpriteGroups = None):
        """_summary_

        :param spriteGroups: List of pygame sprite groups the sprite belongs to.
        :type spriteGroups: list
        :param spriteType: Entity, UI, or Tile
        :type spriteType: str
        :param surface: visual texture of the sprite, (ie: what is drawn to screen)
        :type surface: Surface, optional
        :param start_pos: position of the sprite, defaults to (0, 0)
        :type start_pos: tuple, optional
        :param layer: layer to be drawn at, defaults to 0
        :type layer: int, optional
        :param alpha: transparency of the sprite, defaults to 255
        :type alpha: int, optional
        """
        if spriteGroups is not None:
            super().__init__(spriteGroups)
        self.spriteType = spriteType
        self.image = surface.convert_alpha()
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect(topleft = start_pos)
        self.hitbox = self.rect
        self._layer = layer
        self.invisible = False
        self.superGroups = []
        self.properties = {}
        if SuperSpriteGroups != None and len(SuperSpriteGroups) != 0:
            for group in SuperSpriteGroups:
                group.add(self)
                self.superGroups.append(group)

    def kill(self):
        """
        Override the kill method to remove the sprite from all groups
        """
        for group in self.superGroups:
            group.remove(self)
        super().kill()
        
            
class SuperSpriteGroup():
    def __init__(self, superSprites=None, name='unnamed'):
        self.name = name
        self.superSprites = []
        if superSprites is not None:
            for superSprite in superSprites:
                self.add(superSprite)
                superSprite.superGroups.append(self)

    def __iter__(self):
        return iter(self.superSprites)
    
    def add(self, superSprite):
        self.superSprites.append(superSprite)

    def remove(self, superSprite):
        self.superSprites.remove(superSprite)

    def empty(self):
        """
        Empties the group of all sprites
        """
        for superSprite in self.superSprites:
            superSprite.kill()
        self.superSprites = []

    def sortByLayer(self):
        """
        Sorts sprites by layer
        Layers >= 20 are always on top
        
        """
        def sprite_sort_key(superSprite):
            if superSprite._layer >= 20:
                return (101 + superSprite._layer%10, 0)  # Always last
            
            if superSprite._layer == -2:
                return (100, superSprite.rect.centery)  # Sort by centery for _layer == -2
            
            return (superSprite._layer, superSprite.rect.centery)
        
        return sorted(self.superSprites(), key=sprite_sort_key)