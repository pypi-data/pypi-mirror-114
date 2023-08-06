from bluebeam.objects import Enemy
import pygame
import math
import os

# Base class for whale boss turrets


class WhaleTurret(Enemy):

    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._hp = 50
        self._contactdmg = 0
        self._anchor = None
        self._anchorpos = pygame.math.Vector2(0, 0)
        self._dmgflash = 0
        self._shotcd = 0.01
        self._rot = 0
        self.rect = pygame.rect.Rect(self.pos.x - 25, self.pos.y - 25, 80, 80)
        self.rect.center = self.pos
        self.osc = 0
        self.bases = []
        self.guns = []
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images")
        self.spritesheet = pygame.image.load(os.path.join(self.imageDir, 'boss01_turrets.png')).convert()
        if not hasattr(self, "style"): self.style = 0
        self.load_sprites()

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, a_):
        self._anchor = a_

    @property
    def anchorpos(self):
        return self._anchorpos

    @anchorpos.setter
    def anchorpos(self, ap_):
        self._anchorpos = ap_

    @property
    def shotcd(self):
        return self._shotcd

    @shotcd.setter
    def shotcd(self, sc_):
        self._shotcd = sc_

    @property
    def rot(self):
        return self._rot

    @rot.setter
    def rot(self, r_):
        self._rot = r_

    def load_single(self, vec4):
        rect = pygame.Rect(vec4[0], vec4[1], vec4[2], vec4[3])
        img = pygame.Surface(rect.size).convert()
        img.blit(self.spritesheet, (0, 0), rect)
        img.set_colorkey(img.get_at((0, 0)), pygame.RLEACCEL)
        return img

    def load_sprites(self):
        for image in range(4):
            x = 88 * (image % 4)
            self.bases.append(self.load_single((x,0,88,88)))
            self.guns.append(self.load_single((x,88,88,88)))
        self.image = self.bases[self.style]

    def update(self):
        super().update()
        self.pos = self._anchor.pos + self._anchorpos
        self.vel = 0
        self._dmgflash = max(0, self._dmgflash - self.g.delta_time)
        self._shotcd = max(0, self._shotcd - self.g.delta_time)
        if self._shotcd <= 0:
            self.fire()
        self.image = self.bases[self.style]

    def fire(self):
        self._shotcd = 2.5

    def collision_bullet(self):
        col = pygame.sprite.spritecollide(self, self.l.bulletsP, False)
        if len(col) > 0:
            for bul in col:
                self.hp -= bul.dmg
                self.l.uncreate(bul.instid)
                self._dmgflash = 0.35

    def rotinplace(self, image, angle):
        core = image.get_rect().center
        ret = pygame.transform.rotate(image, angle)
        rec = ret.get_rect(center = ret.get_rect(center = (core[0],core[1])).center)
        return ret, rec

    def render(self):
        # Draw base
        self.l.s.blit(self.image, self.rect.copy().move(-self.l.view))
        # Draw gun
        gun = self.guns[self.style]
        rgun = self.rotinplace(gun, 90 + -self.rot)
        self.l.s.blit(rgun[0], rgun[1].copy().move(-self.l.view + self.pos - pygame.math.Vector2(self.rect.width/2,self.rect.height/2)))