import math
import os

import pygame, itertools

from bluebeam.objects import *
from bluebeam.TileMap import TileMap


class Level:
    g = None  # global vars reference
    s = None  # screen reference
    # major objects
    view = pygame.math.Vector2()
    view_target = pygame.math.Vector2()
    player = pygame.sprite.Sprite()
    bg = None
    objtimer = 1
    camstate = 0
    # groups

    booster = pygame.sprite.Sprite()

    enemies = pygame.sprite.Group()
    pickups = pygame.sprite.Group()
    bulletsE = pygame.sprite.Group()  # it says "bullets" but melee attacks can just be wide, unmoving bullets :)
    bulletsP = pygame.sprite.Group()
    others = pygame.sprite.Group()
    powerUps = pygame.sprite.Group()
    triggers = pygame.sprite.Group()


    def __init__(self, g_, s_, cam_offset, FILENAME):
        self.view_wh = cam_offset
        self.g = g_
        self.s = s_
        self.terrain = pygame.sprite.Group()
        self.bossDeathState = 0
        self.load(FILENAME)
        self.player_around_lg = False

        pass

    def delete(self):
        objects = itertools.chain(self.bulletsP, self.bulletsE, self.enemies, self.powerUps, self.others, self.pickups, self.triggers)
        for thing in objects:
            thing.kill()
    
    def uncreate(self, id):
        temp = filter(lambda item: (item.instid == id),
                      itertools.chain(self.bulletsP, self.bulletsE, self.enemies, self.powerUps, self.triggers))
        for target in temp:
            target.kill()

    def load(self, FILENAME):
        # Background stuff
        self.TileMap = TileMap(self.g, self, filename=FILENAME)

        # Always load a player
        player_pos = self.TileMap.load_player_pos()
        self.player = Player(self.g, self, player_pos)

        # Enemies
        self.spawn_tilemap_enemies()
        self.spawn_tilemap_pickups()
        #self.create("AlphaWhale",pygame.math.Vector2(1000,300))
        #self.create("SliderEnemy",pygame.math.Vector2(3500,200))
        #self.create("LittleGrey", pygame.math.Vector2(100,2300))
        #self.enemies.add(self.create("LittleGrey", pygame.math.Vector2(100,2300)))

        #self.create("SliderEnemy",pygame.math.Vector2(1500,570))
        pygame.mixer.music.stop()

        sourceDir = os.path.dirname(os.path.abspath(__file__))
        soundDir = os.path.join(sourceDir, "Sounds")

        if FILENAME == "MapLevel2.tmx":
            pygame.mixer.music.load(os.path.join(soundDir, 'moskito.xm'))
        elif FILENAME == "MapLevel3.tmx":
            pygame.mixer.music.load(os.path.join(soundDir, 'heidi7.xm'))
        else:
            pygame.mixer.music.load(os.path.join(soundDir, 'flc_pamp.mod'))
        pygame.mixer.music.play(-1,0,0)
        pass

    def spawn_tilemap_pickups(self):
        pickups = self.TileMap.load_pickup_info()
        for picktype, pos in pickups:
            self.create(picktype, pos)

    def spawn_tilemap_enemies(self):
        enemy_list = self.TileMap.load_enemy_info()
        for enemy_type, enemy_pos in enemy_list:
            self.create(enemy_type, enemy_pos)

    def create(self, it, pos):
        item = eval(it)(self.g, self, pos)
        self.append(item)
        return item


    def append(self, item):
        if isinstance(item, Enemy):
            self.enemies.add(item)
        if isinstance(item, Bullet):
            if item.owner == 0:
                self.bulletsP.add(item)
            else:
                self.bulletsE.add(item)
        if isinstance(item, Block):
            self.terrain.add(item)

        if isinstance(item, BossSpawnTrigger) or isinstance(item, BetaBossSpawnTrigger) or isinstance(item, GammaBossSpawnTrigger):
            self.triggers.add(item)

        if isinstance(item, YellowPower):
             self.powerUps.add(item)

        if isinstance(item, BluePower):
            self.powerUps.add(item)
        if isinstance(item, RedPower):
            self.powerUps.add(item)

    def update(self):
        for bullet in itertools.chain(self.bulletsP, self.bulletsE):
            bullet.update()

        self.player.update()

        for enemy in self.enemies:
            enemy.update()

        for powerUp in self.powerUps:
            powerUp.update()

        for trigger in self.triggers:
            trigger.update()

        self.check_grey()

        self.update_view()
        # bg.update()
        self.objtimer -= self.g.delta_time
        if self.objtimer <= 0:
            self.objtimer = 1.
            num = len(self.bulletsE) + len(self.bulletsP) + len(self.enemies) + len(self.pickups) + len(
                self.others) + len(self.powerUps)
        pass

    def update_view(self):
        if self.camstate == 0:
            self.view = self.player.pos - self.view_wh
        elif self.camstate == 1:
            dist = (self.view_target - self.view).length()
            if dist > 0:
                ang = (self.view_target - self.view).normalize()
                self.view += ang * min(dist, 600 * self.g.delta_time)
        # print("self.player.pos: ", self.player.pos)

    def check_grey(self):
        found_grey = False
        for enemy in self.enemies:
            if enemy._telepath:
                self.player.around_lg = True
                self.player.confuse_cd = 1.5
                found_grey = True
        if(not found_grey):
            if(self.player.confuse_cd > 0):
                self.player.confuse_cd -= self.g.delta_time
            if(self.player.confuse_cd <= 0):
                self.player.around_lg = False
        

    def render(self):
        self.s.fill((0, 0, 255))
        self.TileMap.render(self.s, self.view)
        self.renderpipeline = pygame.sprite.Group(sorted(itertools.chain(self.enemies, self.bulletsE, self.bulletsP, self.triggers, self.powerUps), key=lambda d: d.depth))
        for item in self.renderpipeline:
            item.render()
        #for enemy in self.enemies:
        #    enemy.render()
        #for bullet in itertools.chain(self.bulletsE, self.bulletsP):
        #    bullet.render()
        self.player.render()
        #for power_up in self.powerUps:
        #    power_up.render()
        #for trigger in self.triggers:
        #    trigger.render()
        # for pickup in pickups:
        #     pickup.render()
        # for misc in others:
        #   misc.render()
        pass
