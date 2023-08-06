import math

from bluebeam.objects import PhysObject, PlayerBullet, YellowPower, BossSpawnTrigger
import pygame
import os


class Player(PhysObject):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._hp = 100
        self.recently_damaged = False
        self.speed = pygame.math.Vector2(500, 1000)
        # self.rect = pygame.rect.Rect(0, 0, 100, 100) ORIGINAL
        self.rect = pygame.rect.Rect(0, 0, 24, 64)
        self.rect.center = self.pos
        self.shotcd = 0
        self.confuse_cd = 0
        self.invuln = 1.2
        self.gravity = 50
        self.jumping = False
        self.charge_unlocked = False
        self.jump_gravity_mod = 0.3  # Gravity is only x% effective while holding space!

        # for left right movement
        self.running_left = []

        self.stand_pos = 0
        # Load sprite sheet
        self.idle = []
        self.jump = []
        self.falling = []
        self.running_right = []
        self.arm = []
        self.activearm = None
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images")
        self.soundDir = os.path.join(os.path.dirname(self.sourceDir), "Sounds")
        self.spritesheet = pygame.image.load(os.path.join(self.imageDir, 'sigma.png')).convert()
        self.chroma = -1
        self.load_sprites()

        self.image = self.running_right[self.stand_pos]
        self.confusion_img = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir,"Confusion.png")).convert_alpha(), (44,32))
        #self.rect = self.image.get_rect()
        #self.width = self.image.get_width()
        #self.height = self.image.get_height()
        self.animation_counter = 0
        self.direction = 1
        self.aimdirection = pygame.math.Vector2(0, 0)

        # power-ups changes bullet. Default will be zero
        # will decide soon if the power-ups will come from items found or
        # how far in the level player has traversed/enemies killed/score?
        self.current_power = ""
        self.power_up = 0
        self.power_changed = False
        self.charged = False
        self.charged_counter = 0

        #loading some sounds
        self.powup_sound = pygame.mixer.Sound(os.path.join(self.soundDir, 'up.wav'))
        self.powup_sound.set_volume(0.5 * (self.g.get_music_vol() / 100))
        self.charging_sound = pygame.mixer.Sound(os.path.join(self.soundDir, 'charge.wav'))
        self.charging_sound.set_volume(0.5 * (self.g.get_music_vol() / 100))
        self.shoot_sound = pygame.mixer.Sound(os.path.join(self.soundDir, 'shot.wav'))
        self.shoot_sound.set_volume(0.5 * (self.g.get_music_vol() / 100))
        self.charged_sound = pygame.mixer.Sound(os.path.join(self.soundDir, "charged.wav"))
        self.charged_sound.set_volume(0.5 * (self.g.get_music_vol() / 100))
        self.cshot_sound = self.shoot_sound
        self.cshot_sound.set_volume(0.5 * (self.g.get_music_vol() / 100))
        self.damaged_sound = pygame.mixer.Sound(os.path.join(self.soundDir, 'damaged.wav'))
        self.damaged_sound.set_volume(0.5 * (self.g.get_music_vol() / 100))

        #for littlegrey default attack is telepath (inverts player controls)
        self.around_lg = False

        self.power_yellow = 0
        self.power_blue = 0
        self.continuous_shot = False
        self.shooting = False
    def is_player_out_of_bounds(self):
        if self.pos.y > 2528:
            self._hp = 0

    def turn_player_red(self):
        self.idle.clear()
        self.jump.clear()
        self.falling.clear()
        self.running_right.clear()
        self.running_left.clear()
        self.arm.clear()
        self.spritesheet = pygame.image.load(os.path.join(self.imageDir, 'sigmaRed.png')).convert()
        self.load_sprites("red")

    def turn_player_green(self):
        self.idle.clear()
        self.jump.clear()
        self.falling.clear()
        self.running_right.clear()
        self.running_left.clear()
        self.arm.clear()
        current_arm = self.activearm
        self.spritesheet = pygame.image.load(os.path.join(self.imageDir, 'sigma.png')).convert()
        self.load_sprites("green")
        self.activearm = current_arm

    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, amount):
        self._hp = amount

    def load_sprites(self, arm_color="green"):
        # Standing sprite
        self.idle.append(self.load_single((0,0,64,64)))

        # Jumping sprite
        self.jump.append(self.load_single((64, 0, 64, 64)))

        # Running sprites
        for image in range(10):
            x = 64 * (image % 5)
            y = 64 + 64 * math.floor(image/5)
            img = self.load_single((x,y,64,64))
            imgflip = pygame.transform.flip(img, True, False)
            self.running_right.append(img)
            self.running_left.append(imgflip)

        # Load arms
        if arm_color == "green":
            tempsheet = pygame.image.load(os.path.join(self.imageDir, "arm.png")).convert()
        elif arm_color == "red":
            tempsheet = pygame.image.load(os.path.join(self.imageDir, "armRed.png")).convert()
        #tempsheet = pygame.image.load(f'images/arm.png').convert()
        rect = pygame.Rect(80, 16, 40, 11)
        img = pygame.Surface(rect.size).convert()
        img.blit(tempsheet, (0, 0), rect)
        img.set_colorkey(img.get_at((0, 0)), pygame.RLEACCEL)
        self.arm.append(img)
        rect = pygame.Rect(80, 16, 40, 11)
        img = pygame.Surface(rect.size).convert()
        img.blit(tempsheet, (0, 0), rect)
        img.set_colorkey(img.get_at((0, 0)), pygame.RLEACCEL)
        self.arm.append(img)
        self.activearm = self.arm[1]

    # Returns how much the player's shot is charged up, as a percentage
    def get_charge_level(self):
        if(self.charged): return 1.0
        else:
            return float(self.charged_counter) / 50.
    
    def get_powerup_level(self):
        return self.power_up
            
    def update(self):
        self.check_inputs()
        self.update_sprite()
        self.power_sprites()

        gravity_mod = 1
        if (self.jumping):
            gravity_mod = self.jump_gravity_mod

        self.update_phys(gravity_mod)
        self.collision_bullet()
        self.collision_trigger()
        self.shotcd = max(self.shotcd - self.g.delta_time, 0)
        if(self.invuln > 0):
            self.invuln = max(self.invuln - self.g.delta_time, 0)
            if(self.invuln <= 0):
                self.turn_player_green()

        self.shoot_sound.set_volume(0.5 * (self.g.get_FX_vol() / 100))

    # Read and manage all the inputs for player
    def check_inputs(self):
        keys = pygame.key.get_pressed()
        #if not self.l.check_grey():
        if not self.around_lg:
            self._vel.x = (keys[pygame.K_d] - keys[pygame.K_a]) * self._speed.x
        else:
            self._vel.x = -(keys[pygame.K_d] - keys[pygame.K_a]) * self._speed.x

        # Jumping
        if (keys[pygame.K_SPACE]):
            if (self.pstate == 0):
                self.jumping = True
                self._vel.y = -self.speed.y
        elif (self.jumping == True):
            self.jumping = False



        # Charging
        if keys[pygame.K_RSHIFT] and not self.charged and self.charge_unlocked:
            self.charged_counter += 1
            #place charging sound here
            #self.charging_sound.play()

            # print(self.charged_counter)
        if self.charged_counter >= 50:
            self.charged_sound.play()
            self.charged = True
            self.charged_counter = 0


        # Shooting
        if not self.around_lg:
            self.aimdirection = pygame.math.Vector2(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])
        else:
            self.aimdirection = -1 * pygame.math.Vector2(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])

        if self.aimdirection.length() > 0:
            if self.power_yellow > 0:
                self.shoot(self.aimdirection.x, self.aimdirection.y)

            elif self.power_yellow == 0 and not self.shooting:
                self.shoot(self.aimdirection.x, self.aimdirection.y)
                self.shooting = True
        else:
            self.shooting = False

        # elif self.aimdirection.length() > 0 and self.power_yellow == 0 and self.shooting:
        #     self.shooting = False
        #     #print("does this print")

    def power_sprites(self):
    # obtaining powerUp(s)
        keys = pygame.key.get_pressed()
        power = pygame.sprite.spritecollide(self, self.l.powerUps, False)
        if len(power) > 0:
            for booster in power:
                #old_power = self.power_up
                boost_type = booster.acquired()
                self.powup_sound.play()
                booster.kill()

                if  (boost_type == 1):
                    self.current_power = "blue"
                    self.charge_unlocked = True
                    self.power_blue += 1
                elif(boost_type == 2):
                    self.current_power = "yellow"
                    self.power_up += 1
                    self.power_yellow += 1
                elif(boost_type == 3):
                    self.current_power = "red"
                    self.hp += 10
                    if self.hp > 100:
                        self.hp = 100

    # Update the Player's Animation
    def update_sprite(self):
        self.is_player_out_of_bounds()

        if self._vel.x != 0: self.direction = math.copysign(1, self._vel.x)

        self.truedir = self.direction
        if (self.aimdirection.x != self.direction) and self.aimdirection.x != 0:
            self.truedir = self.aimdirection.x

        if self._vel.x < 0:
            self.animation_counter += 18 * self.g.delta_time

            if self.animation_counter >= 10:
                self.animation_counter = 0
        elif self._vel.x > 0:
            self.animation_counter += 18 * self.g.delta_time

            if self.animation_counter >= 10:
                self.animation_counter = 0
        else:
            self.animation_counter = 0

        if abs(self._vel.y) > self.gravity:
            self.image = self.jump[0]
        elif self._vel.x != 0:
            self.image = self.running_right[math.floor(self.animation_counter)]
        else:
            self.image = self.idle[0]

        self.activearm = self.arm[1]

        if (self.truedir == -1):
            self.image = pygame.transform.flip(self.image, True, False)
            self.activearm = pygame.transform.flip(self.activearm, True, False)

    def shoot(self, lr, ud):
        if self.shotcd <= 0:
            inst = self.l.create("PlayerBullet", self.pos.xy)
            inst.speed = pygame.math.Vector2(lr * 800, ud * 800)
            if (self.aimdirection.x == 1 and self.aimdirection.y == 0 and not self.charged):
                inst.pos.x += 18
                inst.pos.y -= 10
            elif (self.aimdirection.x == -1 and self.aimdirection.y == 0 and not self.charged):
                inst.pos.x -= 18
                inst.pos.y -= 10
            elif (self.aimdirection.x == 1 and self.aimdirection.y == 0 and self.charged):
                inst.pos.x += 30
                inst.pos.y -= 10
            elif (self.aimdirection.x == -1 and self.aimdirection.y == 0 and self.charged):
                inst.pos.x -= 30
                inst.pos.y -= 10
            elif (self.aimdirection.x == 0 and self.aimdirection.y == -1 and not self.charged):
                inst.pos.y -= 30
            elif (self.aimdirection.x == 0 and self.aimdirection.y == -1 and self.charged):
                inst.pos.y -= 40
            elif (self.aimdirection.x == 1 and self.aimdirection.y == -1 and not self.charged):
                inst.pos.x += 15
                inst.pos.y -= 22
            elif (self.aimdirection.x == 1 and self.aimdirection.y == -1 and self.charged):
                inst.pos.x += 30
                inst.pos.y -= 22

            elif (self.aimdirection.x == -1 and self.aimdirection.y == -1 and not self.charged):
                inst.pos.x -= 12
                inst.pos.y -= 22
            elif (self.aimdirection.x == -1 and self.aimdirection.y == -1 and self.charged):
                inst.pos.x -= 30
                inst.pos.y -= 35

            if self.charged:
                self.cshot_sound.play()
                inst.dmg *= 1.5 * self.power_blue
                inst.size = 64
                self.charged = False
                inst.charged = True

            if self.power_yellow >= 1:
                self.shotcd = .4 - self.power_yellow * .05
                self.shoot_sound.play()
            else:
                self.shotcd = .4
                self.shoot_sound.play()

    def rotinplace(self, image, angle):
        core = image.get_rect().center
        ret = pygame.transform.rotate(image, angle)
        rec = ret.get_rect(center = ret.get_rect(center = (core[0],core[1])).center)
        return ret, rec

    def render(self):
        # Draw arm
        if self.aimdirection == 0 and self._vel.length() == 0:
            self.l.s.blit(self.activearm, self.rect.copy().move(-self.l.view).move(pygame.math.Vector2(12 + 3*self.direction,15)))
        else:
            inv = (self.truedir == -1 and self.aimdirection.x != 0)
            ang = 180*(self.truedir==-1 and self.aimdirection.x != 0) + pygame.math.Vector2(self.aimdirection.x,-self.aimdirection.y).as_polar()[1]
            rarm = self.rotinplace(self.activearm, ang)
            self.l.s.blit(rarm[0], rarm[1].copy().move(-self.l.view + self.pos - pygame.math.Vector2(30)).move(pygame.math.Vector2(10,15)))
        # Draw player
        #pygame.draw.rect(self.l.s, (255,255,0,100),self.rect.copy().move(-self.l.view))
        self.l.s.blit(self.image, self.rect.copy().move(-self.l.view - pygame.math.Vector2(20,0)))
        if(self.around_lg):
            self.l.s.blit(self.confusion_img, self.rect.copy().move(-self.l.view - pygame.math.Vector2(10,50)))


    def collision_bullet(self):
        col = pygame.sprite.spritecollide(self, self.l.bulletsE, False)
        if len(col) > 0:
            for bul in col:
                self.take_damage(bul.dmg)
                bul.hit()

    def collision_trigger(self):
        col = pygame.sprite.spritecollide(self, self.l.triggers, False)
        if len(col) > 0:
            for bul in col:
                if bul.activated != 1:
                    bul.firstframe()


    def take_damage(self, damage):
        if self.invuln <= 0 and damage > 0:
            self._hp -= damage
            self.invuln = 0.5
            self.damaged_sound.play()
            self.turn_player_red()
