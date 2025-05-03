# magick Stone\ Ground.png  +gravity -crop 32x32 stone_ground_%d.png

# cd aseprite
# mkdir build
# cd build
# cmake \
#   -DCMAKE_BUILD_TYPE=RelWithDebInfo \
#   -DCMAKE_OSX_ARCHITECTURES=arm64 \
#   -DCMAKE_OSX_DEPLOYMENT_TARGET=11.0 \
#   -DCMAKE_OSX_SYSROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk \
#   -DLAF_BACKEND=skia \
#   -DSKIA_DIR=$HOME/deps/skia \
#   -DSKIA_LIBRARY_DIR=$HOME/deps/skia/out/Release-arm64 \
#   -DSKIA_LIBRARY=$HOME/deps/skia/out/Release-arm64/libskia.a \
#   -DPNG_ARM_NEON:STRING=on \
#   -G Ninja \
#   ..
# ninja aseprite

import pygame
from superSprite import SuperSprite
from assets.settings import *
from math import sin


# Tile Types: struct, shadow, tree, plant, prop
class Tile(SuperSprite):
    def __init__(self, pos, oldgroups, groups, spriteType, level, surface = pygame.Surface((TILESIZE, TILESIZE)), layer=-1, alpha=255, deflate=(0, 0)):
        super().__init__(oldgroups, SuperSpriteGroups=groups)
        self.level = level
        self.spriteType = spriteType
        if layer > -1:
            self._layer = layer
        self.image = surface.convert_alpha()  # by default is a black screen of size TILESIZE x TILESIZE
        self.image.set_alpha(alpha)
        if self.spriteType == 'object':  # off set image position for abnormal sized images
            self.rect = self.image.get_rect(topleft=(pos[0],pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(deflate[0], deflate[1])

    def wave_value(self, offset = 0, speed = 1, baseValue=0):
        return 255*min((sin(speed*pygame.time.get_ticks()/20+offset)**2 + baseValue), 1)