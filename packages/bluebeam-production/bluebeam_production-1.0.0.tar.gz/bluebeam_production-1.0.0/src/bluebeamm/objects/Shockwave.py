from bluebeamm.objects import EnemyBullet
import pygame


class Shockwave(EnemyBullet):

    def __init__(self, g_, l_, pos_):
        super().__init__(g_, l_, pos_)
        self._frames = 10
        self._frame = 10
        self._spawnat = self._frames - 1
        self._timeperframe = 0.02
        self._width = 16
        self._height = 256
        self.depth = 16
        self._rheight = self._height * (1 - (1 + abs(self._frame - self._frames / 2)) / (1 + self._frames / 2))
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, self._width, self._rheight)
        self.rect.midbottom = self.pos
        self.lifespan = self._timeperframe
        self.dir = 1
        self.dmg = 10

    def setsize(self, v2_):
        self._width = v2_.x
        self._height = v2_.y
        self._rheight = self._height * (1 - (1 + abs(self._frame - self._frames / 2)) / (1 + self._frames / 2))
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, v2_.x, self._rheight)
        self.rect.midbottom = self.pos

    def update(self):
        self._rheight = self._height * (1 - (abs(self._frame - self._frames / 2)) / (1 + self._frames / 2))
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, self._width, self._rheight)
        self.rect.midbottom = self.pos
        self._lifespan = max(0, self._lifespan - self.g.delta_time)
        if self._lifespan <= 0:
            if self._frame == -1:
                self.fadeout()
            else:
                self._lifespan = self._timeperframe
                self._frame -= 1
                if self._frame == self._spawnat:
                    if not self.check(self._width * self.dir):
                        nextwave = self.l.create("Shockwave", self.pos + pygame.math.Vector2(self._width * self.dir, 0))
                        nextwave.setsize(pygame.math.Vector2(self._width, self._height))
                        nextwave.dir = self.dir
                        nextwave.setframes(self._frames, self._timeperframe)

    def fadeout(self):
        self.l.uncreate(self.instid)

    def hit(self):
        pass

    def setframes(self, f_, t_=None):
        if t_ is not None:
            self._timeperframe = t_
        self._frames = f_
        self._frame = f_
        self._spawnat = f_ - 1

    def check(self, offset):
        print(self.rect.height)
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, self._width, self._rheight)
        self.rect.midbottom = self.pos
        col = pygame.sprite.spritecollide(self, self.l.terrain, False)
        if len(col) > 0:
            return 1
        else:
            return 0
