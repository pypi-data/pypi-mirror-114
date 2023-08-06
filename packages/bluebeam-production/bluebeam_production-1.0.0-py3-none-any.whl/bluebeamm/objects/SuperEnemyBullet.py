from bluebeamm.objects import EnemyBullet
import pygame, math


class SuperEnemyBullet(EnemyBullet):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.lifespan = 10.
        self.targets = [pygame.math.Vector2(), pygame.math.Vector2()]
        self.specspeed = 400
        self.vel = pygame.math.Vector2(0,0)
        self.accel = 800
        self.targ = 0
        self.switchtarg = 0.8

    def update(self):
        cur = (self.targets[self.targ] - self.pos)
        if cur.magnitude() != 0 and self.vel != 0:
            self.vel = cur.normalize() * self.specspeed
        else:
            self.vel = pygame.math.Vector2(0)
        if (cur.magnitude() <= (self.vel * self.g.delta_time).magnitude()) and self.targ == 0:
            self.pos = self.targets[self.targ]
            self.vel = pygame.math.Vector2(0)
            self.switchtarg = max(0,self.switchtarg - self.g.delta_time)
            if self.switchtarg == 0:
                self.specspeed = pygame.math.Vector2(400)
                self.targ = 1
        elif self.targ == 1:
            self.specspeed += pygame.math.Vector2(self.accel * self.g.delta_time)
            self.vel = cur.normalize() * self.specspeed.x
        super().update()