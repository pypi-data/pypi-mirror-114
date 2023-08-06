from bluebeam.objects import WhaleTurret
import os
import pygame
import math
import random


# Commander has 3 attacks
## Split Bomb - Throws bombs that split into two, the last bombs splitting twice
## Direct Burst - Fires a few bullets directly at the player in a few bursts
## Laser Wave - Creates laser waves that travel along the ground of varying max heights
# Attacks are determined randomly via a weighted RNG call
## Later, I'll implement a system where the commander tends to use attacks that have hit the player before
# Commander is also invincible - only stops attacking when the boss is destroyed

class WhaleCommander(WhaleTurret):

    def __init__(self, g_, l_, pos_=None):
        self._hanging = []
        self._gun = []
        super().__init__(g_, l_, pos_)
        self._hanging.clear()
        self._gun.clear()

        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images")
        self.spritesheet = pygame.image.load(os.path.join(self.imageDir, 'boss01_commander.png')).convert()

        #self.spritesheet = pygame.image.load(f'images/boss01_commander.png').convert()
        self.load_sprites()
        self.hp = -1
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, 0, 0)
        self._weights = [1, 1.1, 0]
        self.nextattack = 0
        self.trackplr = 1
        self.plrpos = self.l.player.pos
        self.aimpos = pygame.math.Vector2()
        self.burst = 0
        self._shotcd = 3.75
        self.determinenext()
        self.image = self._hanging[0]

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, weights_):
        self._weights = weights_

    def load_sprites(self):
        self._hanging.append(pygame.transform.scale(self.load_single((48, 96, 48, 48)), (144, 144)))

        #tempsheet = pygame.image.load(f'images/commander_gun.png').convert()
        tempsheet = pygame.image.load(os.path.join(self.imageDir, 'commander_gun.png')).convert()
        rect = pygame.Rect(0, 0, 40, 30)
        img = pygame.Surface(rect.size).convert()
        img.blit(tempsheet, (0, 0), rect)
        img.set_colorkey(img.get_at((0, 0)), pygame.RLEACCEL)
        self._gun.append(pygame.transform.scale(img, (120,90)))


    def update(self):
        self.pos = self._anchor.pos + self._anchorpos
        self.vel = 0
        if self.trackplr == 1 and self.nextattack == 1 and self._shotcd < 1.2:
            self.plrpos = self.l.player.pos
            dist = max(abs(self.plrpos.length() - self.aimpos.length()), 0.01)
            self.aimpos = self.aimpos.lerp(self.plrpos, min(self.g.delta_time * (1000 / dist), 1))
        elif self.nextattack != 1 and self._shotcd < 1.2:
            dist = max(abs(self.plrpos.length() - self.aimpos.length()), 0.01)
            self.aimpos = self.aimpos.lerp(self.plrpos, min(self.g.delta_time * (1000 / dist), 1))
        else:
            dist = abs(pygame.math.Vector2(self.pos.x - 800, self.pos.y).length() - self.pos.length())
            self.aimpos = self.aimpos.lerp(pygame.math.Vector2(self.pos.x - 800, self.pos.y),
                                           min(self.g.delta_time * (1000 / dist), 1))

        self._shotcd = max(0, self._shotcd - self.g.delta_time)
        if self._shotcd <= 0:
            self.fire()

    def fire(self):
        if self.nextattack == 0:
            self._shotcd = 0.8
            inst = self.l.create("SplitBomb", self.pos.xy)
            inst.vel = (self.aimpos - self.pos.xy).normalize()
            inst.vel.x = inst.vel.x * 500
            inst.vel.y = inst.vel.y * 750
            inst.splits = math.floor(1 + self.burst / 2)
            angle = math.radians(random.random() * 60 + 210)
            self.plrpos = pygame.math.Vector2(self.pos.x + 800 * math.cos(angle),
                                              self.pos.y - 400 + 500 * math.sin(angle))
            self.burst += 1
            if self.burst >= 3:
                self.burst = 0
                self.determinenext()
                self._shotcd = 3.75
        elif self.nextattack == 1:
            trackplr = 0
            angle = pygame.math.Vector2().angle_to(self.aimpos - self.pos)
            inst = self.l.create("EnemyBullet", self.pos.xy)
            inst.vel = pygame.math.Vector2(400 * math.cos(math.radians(angle)), 400 * math.sin(math.radians(angle)))
            self._shotcd = 0.05
            self.burst += 1
            if self.burst % 4 == 0:
                trackplr = 1
                self._shotcd = 0.475
            if self.burst >= 12:
                trackplr = 1
                self.burst = 0
                self.determinenext()
                self._shotcd = 3.75
        else:
            self._shotcd = 0.95
            self.burst += 1
            if self.burst >= 3:
                self.burst = 0
                self.determinenext()
                self._shotcd = 3.75

    def determinenext(self):
        r = random.random() * (self.weights[0] + self.weights[1] + self.weights[2])
        if r < self.weights[0]:
            self.trackplr = 0
            self.nextattack = 0
        elif r < self.weights[0] + self.weights[1]:
            self.trackplr = 1
            self.nextattack = 1
        else:
            self.trackplr = 0
            self.nextattack = 2
        if self.nextattack == 0:
            angle = math.radians(random.random() * 30 + 240)
            self.plrpos = pygame.math.Vector2(self.pos.x + 800 * math.cos(angle),
                                              self.pos.y - 400 + 500 * math.sin(angle))

    def rotinplace(self, image, angle):
        core = image.get_rect().center
        ret = pygame.transform.rotate(image, angle)
        rec = ret.get_rect(center = ret.get_rect(center = (core[0],core[1])).center)
        return ret, rec

    def render(self):
        pygame.draw.line(self.l.s, (255, 0, 0, 100), self.pos - self.l.view, self.aimpos - self.l.view)
        self.l.s.blit(self.image, pygame.rect.Rect(self.pos.x - self.l.view.x - 72, self.pos.y - self.l.view.y - 72, 144,144))
        ang = (self.aimpos - self.pos).as_polar()[1]
        rgun = self.rotinplace(self._gun[0], 180 - ang)
        self.l.s.blit(rgun[0], rgun[1].copy().move(self.pos - self.l.view + pygame.math.Vector2(-27, -72 + 7)))