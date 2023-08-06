from bluebeam.objects import WhaleTurret
import pygame
import math


class WhaleTurretSide(WhaleTurret):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._turretpoint = self.pos
        self._extenddelay = 4.5
        self._extend = 0

    def update(self):
        self.style = 1
        super().update()
        self._turretpoint = self.pos
        self.pos = self._turretpoint + pygame.math.Vector2(0, self._extend)
        self._extenddelay -= self.g.delta_time
        if self._shotcd > 0.8 and self._extenddelay <= 0:
            value = self.l.player.pos.y - (self._turretpoint.y + self._extend)
            self._extend += math.copysign(min(abs(value), 175 * self.g.delta_time), value)

    def fire(self):
        inst = self.l.create("EnemyBullet", self._turretpoint + pygame.math.Vector2(0, self._extend))
        inst.speed = pygame.math.Vector2(400 * math.cos(math.radians(self._rot)),
                                         400 * math.sin(math.radians(self._rot)))
        self._shotcd = 4.33

    def render(self):
        super().render()
