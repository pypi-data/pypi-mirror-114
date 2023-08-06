from bluebeam.objects import WhaleTurret
import pygame
import math


class WhaleTurretFlex(WhaleTurret):
    def __init__(self, g_, l_, pos_=None):
        self.style = 0
        super().__init__(g_, l_, pos_)

    def update(self):
        super().update()
        self._rot = pygame.math.Vector2().angle_to(self.l.player.pos - self.pos)

    def fire(self):
        inst = self.l.create("EnemyBullet", self.pos.xy)
        inst.speed = pygame.math.Vector2(300 * math.cos(math.radians(self._rot)),
                                         300 * math.sin(math.radians(self._rot)))
        self._shotcd = 2.67

    def render(self):
        super().render()
