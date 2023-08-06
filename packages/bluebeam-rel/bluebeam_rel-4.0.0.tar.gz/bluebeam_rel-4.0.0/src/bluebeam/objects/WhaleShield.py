from bluebeam.objects import WhaleTurret
import pygame


class WhaleShield(WhaleTurret):

    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.hp = 100
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, 160, 32)
        self.rect.center = self.pos

    def render(self):
        pygame.draw.rect(self.l.s, (192, 32, 32, 100), self.rect.copy().move(-self.l.view))
