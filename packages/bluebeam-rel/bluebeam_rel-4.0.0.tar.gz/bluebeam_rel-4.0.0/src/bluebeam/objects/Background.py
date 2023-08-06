import pygame


class Background:
    _g = None
    _l = None

    layer_img = []
    layer_spd = []  # speeds for parallax scrolling
    layer_pos = []

    def __init__(self, g_, l_):
        self.layer()
        self._g = g_
        self._l = l_

    def load(self):
        pass

    def layer(self):
        self.layer_img.append(pygame.image.load("images/test_background.png").convert())
        # self.layer_img[0].fill((128, 0, 0, 100), special_flags=pygame.BLEND_ADD)
        self.layer_spd.append(0.)
        self.layer_pos.append(pygame.math.Vector2(-700, -700))

    def update(self):
        # parallax scrolling logic will go here c:
        pass

    def render(self):
        for i in range(0, len(self.layer_img)):
            spos = self.layer_pos[i] - self._l.view
            self._l.s.blit(self.layer_img[i], spos)
