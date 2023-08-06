from bluebeam.objects import PhysObject
import pygame


class Bullet(PhysObject):
    def __init__(self, g_, l_, pos_):
        super().__init__(g_, l_, pos_)
        self._objid = 3
        self.speed = pygame.math.Vector2(500, 500)
        self.vel = self.speed
        self.size = 32
        self.owner = 0  # Constant value (unless we add reflecting enemy/player shots.) 0 = player bullet, 1 = enemy bullet.
        self.knf = 0  # Kill Next Frame
        self._lifespan = 3.
        self._dmg = 10
        self._collide_terrain = True
        pass

    def update(self):
        if self.knf == 1:
            self.hit()
        else:
            self.update_phys()
            self.lifespan -= self.g.delta_time
            if self.lifespan <= 0:
                self.hit()
            if ((self.l.view + self.l.view_wh) - self.pos).length() > self.l.view_wh.length() * 1.75:
                self.hit()

    def render(self):
        pass
    
    @property
    def collide_terrain(self):
        return self._collide_terrain

    @collide_terrain.setter
    def collide_terrain(self, col):
        self._collide_terrain = col

    @property
    def lifespan(self):
        return self._lifespan

    @lifespan.setter
    def lifespan(self, lifespan_):
        self._lifespan = lifespan_

    @property
    def dmg(self):
        return self._dmg

    @dmg.setter
    def dmg(self, dmg_):
        self._dmg = dmg_

    @property
    def speed(self):
        return self._speed

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size_):
        self._size = size_
        self.rect = pygame.rect.Rect(0, 0, self._size, self._size)
        self.rect.center = self.pos

    @speed.setter
    def speed(self, speed_):
        self._speed = speed_
        self._vel = self._speed

    def collision_target(self):
        if self.owner == 0:
            col = pygame.sprite.spritecollide(self, self.l.enemies, False)
        else:
            col = pygame.sprite.collide_rect(self, self.l.player)
        if col:
            return 1
        else:
            return 0

    def collision_surface(self):
        col = pygame.sprite.spritecollide(self, self.l.terrain, False)
        if len(col) > 0:
            return 1
        else:
            return 0

    def collision_terrain(self, vertical=None):
        if self.collision_target() or self.collision_surface():
            if(self._collide_terrain): self.knf = 1
            return 0
        else:
            return 0

    def hit(self):
        self.l.uncreate(self.instid)
