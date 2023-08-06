from bluebeam.objects import Enemy
import pygame


class Target(Enemy):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.rect = pygame.rect.Rect(0, 0, 100, 100)
        self.rect.center = self.pos
        self._mhp = 50
        self.hp = self._mhp
        self.idied = 0

    def update(self):
        super().update()
        if self.hp <= 0:
            self.idied = 1

    def render(self):
        pygame.draw.rect(self.l.s,
                         (128 + 127 * (1 - self.idied), 128, 128 + (127 * self.idied), 100),
                         self.rect.copy().move(-self.l.view))
        pygame.draw.rect(self.l.s,
                         (255, 0, 0, 100),
                         pygame.rect.Rect(self.rect.topleft[0], self.rect.topleft[1] - 24, 100, 16).move(-self.l.view))
        pygame.draw.rect(self.l.s,
                         (0, 255, 0, 100),
                         pygame.rect.Rect(self.rect.topleft[0],
                                          self.rect.topleft[1] - 24,
                                          100 * (self.hp / self._mhp),
                                          16).move(-self.l.view))
