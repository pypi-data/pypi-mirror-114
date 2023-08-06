from bluebeam.objects import WhaleTurret
import pygame


class WhaleTurretLaser(WhaleTurret):
    def __init__(self, g_, l_, pos_=None):
        self.style = 3
        super().__init__(g_, l_, pos_)
        self._hp = 150
        self._endpoints = [-100, 100]
        self._railx = 0
        self.dir = 1
        self._emitpoint = pygame.math.Vector2(self.pos.x, (self.pos.y + self.rect.midbottom[1]) / 2)
        self._shotcd = 4.67
        self._rot = 1

    @property
    def endpoints(self):
        return self._endpoints

    @endpoints.setter
    def endpoints(self, e_):
        self._endpoints = e_

    @property
    def emitpoint(self):
        return self._emitpoint

    @emitpoint.setter
    def emitpoint(self, e_):
        self._emitpoint = e_

    def update(self):
        super().update()
        self._railx += self.dir * 160 * self.g.delta_time
        if self.dir * self._railx > self.dir * self.endpoints[int(0.5 - 0.5 * self.dir)]:
            self._railx = self.endpoints[int(0.5 - 0.5 * self.dir)]
            self.dir = -self.dir
        self.rect.center = self.pos = self._anchor.pos + self._anchorpos + pygame.math.Vector2(self._railx, 0)
        self._emitpoint = pygame.math.Vector2(self.pos.x, (self.pos.y + self.rect.midbottom[1]) / 2)

    def fire(self):
        inst = self.l.create("Laser", self.pos.xy)
        inst.emitter = self
        inst.dir = self._rot
        inst.width = 36
        self._shotcd = 4.67

    def render(self):
        self.rot = self.rot * 90
        super().render()
        self.rot = self.rot / 90
