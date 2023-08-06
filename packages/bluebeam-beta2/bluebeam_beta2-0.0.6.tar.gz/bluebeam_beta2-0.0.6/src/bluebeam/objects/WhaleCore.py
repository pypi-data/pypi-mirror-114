from bluebeam.objects import Enemy
import pygame
import math
import os

class WhaleCore(Enemy):

    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._hp = 300
        self._contactdmg = 0
        self._anchor = None
        self._anchorpos = pygame.math.Vector2(0, 0)
        self._dmgflash = 0
        self.rect = pygame.rect.Rect(self.pos.x - 75, self.pos.y - 75, 100, 100)
        self.rect.center = self.pos
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images")
        self.spritesheet = pygame.image.load(os.path.join(self.imageDir, 'boss01_core.png')).convert()
        self._glow = []
        self._glowtime = 0
        self.load_sprites()

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, a_):
        self._anchor = a_

    @property
    def anchorpos(self):
        return self._anchorpos

    @anchorpos.setter
    def anchorpos(self, ap_):
        self._anchorpos = ap_

    def load_single(self, vec4):
        rect = pygame.Rect(vec4[0], vec4[1], vec4[2], vec4[3])
        img = pygame.Surface(rect.size).convert()
        img.blit(self.spritesheet, (0, 0), rect)
        img.set_colorkey(img.get_at((0, 0)), pygame.RLEACCEL)
        return img

    def load_sprites(self):
        for image in range(4):
            x = 112 * (image % 2)
            y = 112 * math.floor(image/2)
            img = self.load_single((x,y,112,112))
            self._glow.append(img)

    def update(self):
        super().update()
        self.pos = self._anchor.pos + self._anchorpos
        self.vel = 0
        self._dmgflash = max(0, self._dmgflash - self.g.delta_time)

    def collision_bullet(self):
        col = pygame.sprite.spritecollide(self, self.l.bulletsP, False)
        if len(col) > 0:
            for bul in col:
                self.hp -= bul.dmg
                self.l.uncreate(bul.instid)
                self._dmgflash = 0.35

    def render(self):
        self._glowtime += 6.67 * self.g.delta_time
        if self._glowtime >= 7: self._glowtime = 0
        self.image = self._glow[3 - abs(3 - math.floor(self._glowtime))]
        self.l.s.blit(self.image, self.rect.copy().move(-self.l.view))
