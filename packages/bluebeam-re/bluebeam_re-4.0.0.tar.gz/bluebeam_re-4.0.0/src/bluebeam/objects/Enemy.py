from bluebeam.objects import PhysObject
import pygame


class Enemy(PhysObject):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._objid = 2
        self._hp = 1
        self._contactdmg = 10
        self._active = False
        self._telepath = False
        pass

    def update(self):
        if(self._active):
            self.update_phys()
            self.collision_bullet()
            self.collision_player()
        else:
            self.check_active()


    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp_):
        self._hp = hp_
        if self._hp <= 0:
            self.death()

    @property
    def contactdmg(self):
        return self._contactdmg

    @contactdmg.setter
    def contactdmg(self, contactdmg_):
        self._contactdmg = contactdmg_

    def death(self):
        self.l.uncreate(self.instid)

    def check_active(self):
        diff = self.pos - self.l.player.pos
        squareddist = diff.x**2 + diff.y**2
        if squareddist < 1100000:
            self._active = True

    def collision_bullet(self):
        col = pygame.sprite.spritecollide(self, self.l.bulletsP, False)
        if len(col) > 0:
            for bul in col:
                self.hp -= bul.dmg
                if(bul.charged):
                    self.vel += bul.vel
                bul.hit()

    def collision_player(self):
        col = pygame.sprite.collide_rect(self, self.l.player)
        if col:
            self.l.player.take_damage(self.contactdmg)
