import itertools

import pygame
import math
from bluebeamm.objects import EnemyBullet


class Laser(EnemyBullet):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.owner = 1
        self._emitter = None
        self.emitpoint = self.pos
        self.speed = pygame.math.Vector2(0, 0)
        self.vel = self.speed
        self.warmup = 0.5
        self.lifespan = 2.33
        self._objid = 4
        self._dir = 1
        self.b2speed = 0
        self._width = 16
        self.dmg = 0
        self.times = -1

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, d_):
        self._dir = d_

    @property
    def emitter(self):
        return self._emitter

    @emitter.setter
    def emitter(self, e_):
        self._emitter = e_

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, w_):
        self._width = w_

    def expand(self):
        self.times -= 1
        len = 16
        pow = 6
        wid = (self.warmup <= 0)*(self.width-2) + 2
        self.rect = pygame.rect.Rect(self.emitpoint.x, self.emitpoint.y, 2 + 14 * (self._dir % 2 == 0),
                                     2 + 14 * (self._dir % 2 == 1))
        if abs(self.b2speed) != 0 and self.warmup <= 0:
            self.emitpoint.x += self.b2speed * self.g.delta_time
        self.set_dir()
        while pow >= 0 and len < 1024:
            len += math.pow(4, pow)
            self.rect = self.rect.inflate(math.pow(4, pow) * (self._dir % 2 == 0),
                                          math.pow(4, pow) * (self._dir % 2 == 1))
            self.set_dir()
            if self.collision_surface():
                self.rect = self.rect.inflate(-math.pow(4, pow) * (self._dir % 2 == 0),
                                              -math.pow(4, pow) * (self._dir % 2 == 1))
                self.set_dir()
                len -= math.pow(4, pow)
                pow -= 1
        self.rect = self.rect.inflate((wid - 2) * (self._dir % 2 == 1),
                                      (wid - 2) * (self._dir % 2 == 0))

    def set_dir(self):
        if self._dir == 0:
            self.rect.midleft = self.emitpoint
        elif self._dir == 1:
            self.rect.midtop = self.emitpoint
        elif self._dir == 2:
            self.rect.midright = self.emitpoint
        elif self._dir == 3:
            self.rect.midbottom = self.emitpoint

    def update(self):
        if self.times >= 0:
            self.killproj()
        if  self._emitter is not None:
            self.emitpoint = self._emitter.emitpoint
        if self.times != 0:
            self.expand()
        if self.warmup > 0:
            self.warmup = max(self.warmup - self.g.delta_time, 0)
            if self.warmup == 0:
                self.dmg = 10
        else:
            self.lifespan -= self.g.delta_time
            if self.lifespan <= 0: self.fadeout()

    def fadeout(self):
        self.l.uncreate(self.instid)

    def hit(self):
        pass

    def killproj(self):
        col = itertools.chain(pygame.sprite.spritecollide(self, self.l.bulletsE, False), pygame.sprite.spritecollide(self, self.l.bulletsP, False))
        for bul in col:
            bul.hit()

    def render(self):
        pygame.draw.rect(self.l.s, (64 + 191*(self.times >= 0), 64, 255, 100), self.rect.copy().move(-self.l.view))
