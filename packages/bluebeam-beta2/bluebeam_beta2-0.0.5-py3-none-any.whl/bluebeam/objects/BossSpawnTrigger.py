import math
import os

from bluebeam.objects import GameObject
import pygame

class BossSpawnTrigger(GameObject):

    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._activated = 0
        self.rect = pygame.rect.Rect(self.pos.x,self.pos.y,1024,256)
        self.rect.midtop = self.pos
        self.stand = []
        self.jump = []
        self.laugh = []
        self.clutch = []
        #paths so it works
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images")
        self.soundDir = os.path.join(os.path.dirname(self.sourceDir), "Sounds")
        #self.spritesheet = pygame.image.load(f'images/boss01_commander.png').convert()
        self.spritesheet = pygame.image.load(os.path.join(self.imageDir, "boss01_commander.png")).convert()
        self.load_sprites()
        self.commanderrp = pygame.math.Vector2(512, 0)
        self.waittospawn = 2.25
        self.waittojump = 0
        self.jumping = 0

    @property
    def activated(self):
        return self._activated

    @activated.setter
    def activated(self, a_):
        self._activated = a_

    def load_sprites(self):
        self.laugh.append(pygame.transform.scale(self.load_single((0, 0, 48, 48)), (144, 144)))
        self.laugh.append(pygame.transform.scale(self.load_single((48, 0, 48, 48)), (144, 144)))
        self.stand.append(pygame.transform.scale(self.load_single((0, 48, 48, 48)), (144, 144)))
        self.jump.append(pygame.transform.scale(self.load_single((48, 48, 48, 48)), (144, 144)))
        self.clutch.append(pygame.transform.scale(self.load_single((0, 96, 48, 48)), (144, 144)))
        self.image = self.stand[0]

    def firstframe(self):
        self.activated = 1
        self.l.view_target = self.pos + pygame.math.Vector2(-self.l.view_wh.x,-128 - self.l.view_wh.y)
        print(self.l.view)
        print(self.l.view_target)
        self.l.camstate = 1
        pygame.mixer.music.fadeout(1800)

    def update(self):
        self.image = self.stand[0]
        if self._activated == 1:
            if self.waittospawn > 0 and self.waittojump == 0:
                self.waittospawn = max(self.waittospawn - self.g.delta_time, 0)
                self.image = self.laugh[int(self.waittospawn * 7.5) % 2]
                if self.waittospawn <= 0:
                    whale = self.l.create("AlphaWhale",self.pos - pygame.math.Vector2(0,256))
                    self.waittojump = 0.8 + 1.2
                    pygame.mixer.music.load(os.path.join(self.soundDir, 'trainer5.mod'))
                    pygame.mixer.music.play(-1,0,200)
            elif self.waittojump > 0:
                self.waittojump = max(self.waittojump - self.g.delta_time, 0)
                self.image = self.stand[0]
            else:
                self.jumping += self.g.delta_time
                self.image = self.jump[0]
                self.commanderrp.y = -480 * min(1.,math.pow(self.jumping/0.8,0.67))
                if self.jumping > 0.8:
                    self.image = self.clutch[0]
                    self.commanderrp.x += 600 * self.g.delta_time
                if self.jumping > 3:
                    self.l.uncreate(self.instid)
                pass
            pass

    def render(self):
        self.l.s.blit(self.image, self.rect.copy().move(-self.l.view + self.commanderrp + pygame.math.Vector2(0,self.rect.height-144)))