from objects import Enemy
import pygame
import os

class LittleGrey(Enemy):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.rect = pygame.rect.Rect(0, 0, 108, 124)
        self.rect.center = self.pos
        self._mhp = 50
        self.hp = self._mhp
        self.idied = 0

        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images/Enemy")
        self.image = pygame.image.load(os.path.join(self.imageDir, 'littlegrey.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 120))

        # self.gravity = 50
        # self._shotcd = 0


    def inproximity(self):
        diff = self.pos - self.l.player.pos
        squareddist = diff.x ** 2 + diff.y ** 2
        if squareddist < 10000 and (self._hp > 0):
            self._telepath = True
        else:
            self._telepath = False
        if self._hp <= 0:
            self.l.player.around_lg = False


    # def move(self):
    #     #just using the slidy enemy's xmove for the time being while experimenting with other ways littlegrey can
    #     #attack. Will adjust.
    #     left = False
    #     if (self.l.player.x < self.x - 80):
    #         targ_xvel = -self.speed.x
    #         if (self.vel.x > targ_xvel):
    #             self.vel.x -= self.speed.x * self.accel
    #
    #     elif (self.l.player.x > self.x + 80):
    #         targ_xvel = self.speed.x
    #         if (self.vel.x < targ_xvel):
    #             self.vel.x += self.speed.x * self.accel
    #             # left = False
    #
    #     if (self.l.player.x < self.x):
    #         left = True
    #     else:
    #         left = False

    def update(self):
        super().update()
        #self.move()
        self.inproximity()
        # if (self._active):
        #     self.update_ai_inputs()


    def render(self):
        # pygame.draw.rect(self.l.s,
        #                   (128 + 127 * (1 - self.idied), 128, 128 + (127 * self.idied), 100),
        #                   self.rect.copy().move(-self.l.view))
        self.l.s.blit(self.image, self.rect.copy().move(-self.l.view))
        pygame.draw.rect(self.l.s,
                         (255, 0, 0, 100),
                         pygame.rect.Rect(self.rect.topleft[0], self.rect.topleft[1] - 24, 100, 16).move(-self.l.view))
        pygame.draw.rect(self.l.s,
                         (0, 255, 0, 100),
                         pygame.rect.Rect(self.rect.topleft[0],
                                          self.rect.topleft[1] - 24,
                                          100 * (self.hp / self._mhp),
                                          16).move(-self.l.view))

