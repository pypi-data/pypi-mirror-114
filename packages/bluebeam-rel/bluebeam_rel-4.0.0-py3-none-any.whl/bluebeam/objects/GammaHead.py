from bluebeam.objects import Enemy
import pygame, math, random, os
from pygame import Vector2 as vec2

class GammaHead(Enemy):
    def __init__(self, g, l, pos):
        super().__init__(g, l, pos)
        self.rect = pygame.rect.Rect(0, 0, 832, 288)
        self.body = None
        self.handtype = vec2(1, 1)
        self.sprite = None

        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imagedir = os.path.join(os.path.dirname(self.sourceDir), "images/Boss/GammaGenerator")
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss03_head.png')).convert()
        self.load_sprites()

        self.neckpoint = vec2()

        self.depth = 10

        self.mode = 0
        self.stateclock = 0
        self.bob = 0

        self.moveto = vec2()
        self.waveburst = 0

    def load_sprites(self):
        img = self.load_single((0,0,208,72))
        self.sprite = pygame.transform.scale(img, (832,288))

    def setup(self, body_):
        self.body = body_
        self.neckpoint = self.pos

    def state(self, mode_):
        self.mode = mode_
        self.stateclock = 0
        if mode_ == 1:
            self.waveburst = 0
            self.wave_reposition()

    def update(self):
        self.process()

    def process(self):
        pass
        states = {
            0: self.idle,
            1: self.wave
        }
        states[self.mode]()

    def smooth_move(self, target_, speed):
        mag = (target_ - self.pos).magnitude()
        if mag > 0:
            if (target_ - self.pos).magnitude() < math.pow(mag, 0.45):
                self.rect.center = self.pos = target_
            else:
                amt = min(speed*self.g.delta_time, math.pow(mag, 0.45))
                self.rect.center = self.pos = self.pos + amt * (target_ - self.pos).normalize()

    def idle(self):
        self.bob = (self.bob + self.g.delta_time * 180) % 360
        self.smooth_move(self.body.pos + vec2(0, -128), 300)

    def wave(self):
        if self.pos != self.moveto:
            self.smooth_move(self.moveto, 600)
            self.stateclock = 0
        else:
            self.stateclock += self.g.delta_time
            if self.stateclock > 0.5 - 0.1*(3-self.body.phase):
                self.l.create("WaveBomb", self.pos.xy)
                self.waveburst += 1
                if self.waveburst >= 3 + (3-self.body.phase):
                    self.state(0)
                else:
                    self.wave_reposition()

    def wave_reposition(self):
        self.rect.center = self.pos
        self.moveto = vec2(random.randint(self.body.bounds[0].x + 144, self.body.bounds[1].x - 144), self.body.pos.y - 160)

    def wave_spit(self):
        self.l.create("WaveBomb", self.pos.xy)

    def death(self):
        pass

    def render(self):
        self.l.s.blit(self.sprite,self.rect.copy().move(-self.l.view))