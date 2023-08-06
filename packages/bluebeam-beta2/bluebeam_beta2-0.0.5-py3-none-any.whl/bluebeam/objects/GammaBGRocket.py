import pygame
from bluebeam.objects import EnemyBullet

#boy, you can just SMELL the iji final boss rip-off-ing from miles away

class GammaBGRocket(EnemyBullet):

    def __init__(self,g_, l_, pos_):
        super().__init__(g_, l_, pos_)
        print("BGrocket spawned")
        self.spawnpos = pygame.math.Vector2()
        self.fakepos = pygame.math.Vector2()
        self.plr = self.l.player
        self.rect = pygame.rect.Rect(self.pos.x,self.pos.y,0,0)
        self.distance = 2.2
        self.depth = 16

    def setup(self, pos_):
        self.spawnpos = self.fakepos = pos_

    def update(self):
        self.distance -= self.g.delta_time
        self.fakepos = pygame.math.Vector2.lerp(self.spawnpos, self.pos, pow(self.clamp01((1.2-self.distance) / 1.2),3))
        if self.distance <= 0:
            self.boom()

    def clamp01(self, _c):
        if _c > 1: return 1
        elif _c < 0: return 0
        else: return _c

    def boom(self):
        boom = self.l.create("Explosion",self.pos.xy)
        boom.radius(256)
        boom.depth = 12
        self.l.uncreate(self.instid)
        pass

    def render(self):
        if self.distance < 1.2:
            p = pow(self.clamp01((1.2-self.distance) / 1.2),4)
            pygame.draw.circle(surface=self.l.s, color=(160*pow(p,0.33), 0, 0, 255), center=(self.fakepos - self.l.view), radius=32 + 64*p)
        pygame.draw.circle(surface=self.l.s, color=(255, 0, 0, 255), center=(self.pos - self.l.view), radius=128, width=24)