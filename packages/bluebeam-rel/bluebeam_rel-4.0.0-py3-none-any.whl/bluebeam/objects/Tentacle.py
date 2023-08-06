import pygame
import math, os
from bluebeam.objects import EnemyBullet


class Tentacle(EnemyBullet.EnemyBullet):
    def __init__(self, g_, l_, tentacle_num, left, pos_=None):
        self.pull_tentacle_info(tentacle_num, left)
        true_pos = pos_ + self.offset
        super().__init__(g_, l_, true_pos)

        self._dmg = 20
        self.speed = pygame.math.Vector2(0., 0.)
        self.vel = self.speed
        self.lifespan = 300
        self._from_bulky = True


    def pull_tentacle_info(self, tentacle_num, left):
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images/Enemy/BulkyGuy")
        if(tentacle_num == 4):
            self.image = pygame.transform.scale( pygame.image.load(os.path.join(self.imageDir, "ArmsAttack4.png")).convert_alpha() , (194, 166))
            self.rect = pygame.rect.Rect(0,0,194, 166)
            self.offset = pygame.math.Vector2(100,-100)
        elif(tentacle_num == 5):
            self.image = pygame.transform.scale( pygame.image.load(os.path.join(self.imageDir, "ArmsAttack5.png")).convert_alpha() , (160, 112))
            self.rect = pygame.rect.Rect(0,0,160, 112)
            self.offset = pygame.math.Vector2(150,40)
        elif(tentacle_num == 6):
            self.image = pygame.transform.scale( pygame.image.load(os.path.join(self.imageDir, "ArmsAttack6.png")).convert_alpha() , (142, 46))
            self.rect = pygame.rect.Rect(0,0,142, 46)
            self.offset = pygame.math.Vector2(140,100)
            if(not left): self.offset.x += 20
        elif(tentacle_num == 7):
            self.image = pygame.transform.scale( pygame.image.load(os.path.join(self.imageDir, "ArmsAttack7.png")).convert_alpha() , (94, 76))
            self.rect = pygame.rect.Rect(0,0,94, 76)
            self.offset = pygame.math.Vector2(85,35)
            if(not left): self.offset.x += 65
        else:
            self.image = None
            self.offset = pygame.math.Vector2(0,0)

        if(left): 
            self.image = pygame.transform.flip(self.image, True, False)
            self.offset.x = -(self.offset.x + 150)
        else:
            self.offset.x += 55

    def refresh_pos(self, new_pos):
        true_pos = new_pos + self.offset
        self._pos = true_pos

    def render(self):
        spos = self._pos - self.l.view
        self.l.s.blit(self.image, self.rect.copy().move(-self.l.view))

    