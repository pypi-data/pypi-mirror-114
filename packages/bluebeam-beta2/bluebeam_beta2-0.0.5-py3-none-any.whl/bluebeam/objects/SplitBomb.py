import pygame, math
from bluebeam.objects import EnemyBullet


class SplitBomb(EnemyBullet):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._splits = 1
        self._initvv = -750
        self.gravity = 35
        self.vel = pygame.math.Vector2(0, self._initvv)
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, 64, 64)
        self.rect.center = self.pos

    @property
    def splits(self):
        return self._splits

    @splits.setter
    def splits(self, s_):
        self._splits = s_

    def update(self):
        self.update_phys()

    def hit(self):
        self.split()

    def split(self):
        boom = self.l.create("Explosion", self.pos)
        boom.radius(48 * self._splits + 128)
        if self._splits > 0:
            for i in range(0, 2):
                item = self.l.create("SplitBomb", self.pos - pygame.math.Vector2(0, self.rect.height / 2))
                item.vel = pygame.math.Vector2((2 * i - 1) * max(0.8 * abs(self.vel.x), 350), self._initvv * 0.95)
                item.splits = self.splits - 1
        self.l.uncreate(self.instid)

    # unique physics for bouncing off walls...

    def ccheck_h(self):
        cc = self.rect.copy()
        for i in range(1, math.ceil(abs(self.vel.x))):
            self.rect = self.rect.move(math.copysign(1, self.vel.x), 0)
            if self.collision_terrain():
                self.vel = pygame.math.Vector2(-self.vel.x, self.vel.y)
                break
        self.rect = cc

    def ccheck_v(self):
        if (self.pstate == 0): self.pstate = 1
        cc = self.rect.copy()
        for i in range(1, math.ceil(abs(self.vel.y))):
            self.rect = self.rect.move(0, math.copysign(1, self.vel.y))
            if self.collision_terrain(True):
                self.rect = self.rect.move(0, -1)
                self.split()
                break
        self.rect = cc

    def collision_terrain(self, vertical=False):
        col = pygame.sprite.spritecollide(self, self.l.terrain, False)
        if len(col) > 0:
            return 1
        else:
            return 0
