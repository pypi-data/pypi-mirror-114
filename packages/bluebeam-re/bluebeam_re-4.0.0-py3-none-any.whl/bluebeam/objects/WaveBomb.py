import pygame, math
from bluebeam.objects import EnemyBullet
from pygame import Vector2 as vec2


class WaveBomb(EnemyBullet):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._initvv = 0
        self.gravity = 35
        self.vel = pygame.math.Vector2(0, self._initvv)
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, 64, 64)
        self.rect.center = self.pos
        self.depth = 16

    @property
    def splits(self):
        return self._splits

    @splits.setter
    def splits(self, s_):
        self._splits = s_

    def update(self):
        self.update_phys()

    def hit(self):
        pass

    def split(self):
        pew = self.l.create("Shockwave", self.rect.midbottom + vec2(0,-1))
        pew.setsize(vec2(32,256))
        pew.setframes(2, 0.03)
        pew.dir = 1
        pew2 = self.l.create("Shockwave", self.rect.midbottom + vec2(0,-1))
        pew2.setsize(vec2(32,256))
        pew2.setframes(2, 0.03)
        pew2.dir = -1
        self.l.uncreate(self.instid)

    def ccheck_h(self):
        cc = self.rect.copy()
        for i in range(1, math.ceil(abs(self.vel.x))):
            self.rect = self.rect.move(math.copysign(1, self.vel.x), 0)
            if self.collision_terrain():
                self.vel = pygame.math.Vector2(-self.vel.x, self.vel.y)
                break
        self.rect = cc

    def ccheck_v(self):
        if (self.pstate == 0): self.pstate = 1
        cc = self.rect.copy()
        for i in range(1, math.ceil(abs(self.vel.y))):
            self.rect = self.rect.move(0, math.copysign(1, self.vel.y))
            if self.collision_terrain(True):
                self.rect = self.rect.move(0, -1)
                self.split()
                break
        self.rect = cc

    def collision_terrain(self, vertical=False):
        col = pygame.sprite.spritecollide(self, self.l.terrain, False)
        if len(col) > 0:
            return 1
        else:
            return 0
