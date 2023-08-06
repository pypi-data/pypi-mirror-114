from bluebeam.objects import Enemy
import pygame
import os


class SliderEnemy(Enemy):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.rect = pygame.rect.Rect(0, 0, 100, 100)
        self.rect.center = self.pos
        self._mhp = 50
        self.hp = self._mhp
        self.idied = 0

        self.speed = pygame.math.Vector2(900, 300)
        self.accel = 0.02
        self.gravity = 0
        self.collide_terrain = False
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images/Enemy")

        #for image/animation
        self.current_position = 0
        self.animation_counter = 0
        self.images_right = []
        self.images_left = []
        for image in range(1,5):
            img_right = pygame.image.load(os.path.join(self.imageDir,f'fish-big{image}.png')).convert_alpha()
            img_right = pygame.transform.scale(img_right, (120, 90))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.images_right[self.current_position]


    def update_ai_inputs(self):
        self.xmove()
        self.ymove()

    def xmove(self):
        # Should I go left or right?
        left = False
        if (self.l.player.x < self.x - 80):
            targ_xvel = -self.speed.x
            if (self.vel.x > targ_xvel):
                self.vel.x -= self.speed.x * self.accel

        elif (self.l.player.x > self.x + 80):
            targ_xvel = self.speed.x
            if (self.vel.x < targ_xvel):
                self.vel.x += self.speed.x * self.accel
                #left = False

        if (self.l.player.x < self.x):
           left = True
        else:
            left = False
        self.update_animation(left)

    def ymove(self):
        # Should I go up or down?
        if (self.l.player.y < self.y - 80):
            targ_yvel = -self.speed.y
            if (self.vel.y > targ_yvel):
                self.vel.y -= self.speed.y * self.accel

        if (self.l.player.y > self.y + 80):
            targ_yvel = self.speed.y
            if (self.vel.y < targ_yvel):
                self.vel.y += self.speed.y * self.accel

    def update_animation(self, left):
        #animation_counter = 0
        #if left:
        self.animation_counter += 1
        if self.animation_counter >= 5:
            self.animation_counter = 0
            self.current_position += 1
            if self.current_position >= 4:
                self.current_position = 0

        if left:
            self.image = self.images_left[self.current_position]
            #print(self.current_position)
        else:
            self.image = self.images_right[self.current_position]


    def update(self):
        super().update()
        if(self._active):
            self.update_ai_inputs()

    def render(self):
        # pygame.draw.rect(self.l.s,
        #                  (128 + 127 * (1 - self.idied), 128, 128 + (127 * self.idied), 100),
        #                  self.rect.copy().move(-self.l.view))

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
