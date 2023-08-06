import pygame
import os
from bluebeam.objects import Bullet



class EnemyBullet(Bullet):
    def __init__(self, g_, l_, pos_=None, left=False, above=False):
        super().__init__(g_, l_, pos_)
        self.owner = 1
        self.speed = pygame.math.Vector2(800., 0.)
        self.vel = self.speed
        self.lifespan = self.l.view_wh.length() / 300
        self._objid = 4
        self.shooty_enemy = False
        self.from_bulky = False

        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images")

        if( not hasattr(self, "image") ):
            self.load_ball_img()

    def load_ball_img(self):
        self.image = pygame.image.load(os.path.join(self.imageDir, 'ball_red.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))



    def load_shooty_image(self):
        self.images = []
        self.index = 0
        #getting paths so it works after pip install
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images/stars")
        for frame in range(1, 4):
            #img = pygame.image.load(f'images/stars/s{frame}.png')
            img = pygame.image.load(os.path.join(self.imageDir, f's{frame}.png'))
            img = pygame.transform.scale(img, (80, 80))
            self.images.append(img)

        self.image = self.images[self.index]
        self.current_position = 0
        self.animation_counter = 0


    def update(self):
        super().update()
        if self.shooty_enemy:
            self.update_animation()

    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter >= 5:
            self.image = self.images[self.index]
            self.index += 1
            self.animation_counter = 0
            if self.index >= 3:
                self.index = 0


        #self.l.s.blit(self.image, self.rect.copy().move(-self.l.view))
        #print("Is this not being called?")

    def render(self):
        spos = self._pos - self.l.view
        if self.shooty_enemy:
            self.l.s.blit(self.image, self.rect.copy().move(-self.l.view))
        elif not self.from_bulky:
            #dpygame.draw.rect(self.l.s, (255, 64, 64, 100), self.rect.copy().move(-self.l.view))
            self.l.s.blit(self.image, self.rect.copy().move(-self.l.view))

