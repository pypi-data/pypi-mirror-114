import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, global_vars, level, block_position, block_width=64, block_height=64):
        super().__init__()
        self._global_vars = global_vars
        self._level = level
        self._block_position = block_position
        self.rect = pygame.rect.Rect(block_position[0], block_position[1], block_width, block_height)
        self.block_width = block_width

    def render(self):
        spos = self._block_position - self._level.view
        pygame.draw.rect(self._level.s, (255, 255, 255, 100), self.rect.copy().move(-self._level.view))
