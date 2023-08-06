from bluebeam.objects import WhaleTurret
import pygame
import math


class WhaleTurretRocket(WhaleTurret):
    def __init__(self, g_, l_, pos_=None):
        self.style = 2
        super().__init__(g_, l_, pos_)

    def update(self):
        super().update()
        if self._shotcd > 0.07:
            self._rot = pygame.math.Vector2().angle_to(self.l.player.pos - self.pos)

    def fire(self):
        inst = self.l.create("Rocket", self.pos.xy)
        inst.speed = pygame.math.Vector2(500 * math.cos(math.radians(self._rot)),
                                         500 * math.sin(math.radians(self._rot)))
        self._shotcd = 4.33

    def render(self):
        super().render()