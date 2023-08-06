from bluebeamm.objects import Enemy
import pygame, os
from pygame import Vector2 as vec2


class GammaCore(Enemy):

    def __init__(self, g_, l_, pos_):
        super().__init__(g_, l_, pos_)
        self.body = None
        self.exposed = 0
        self.door = None
        self.heart = []
        self.drect = pygame.rect.Rect(0,0,124,116)
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imagedir = os.path.join(os.path.dirname(self.sourceDir), "images/Boss/GammaGenerator")
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss03_core_open.png')).convert()
        self.load_sprites()
        self.hp = 1
        self.rect = pygame.rect.Rect(0,0,192,44)
        self.pos = self.rect.center = pos_
        self.depth = 9
        self.flash = 0

    def load_sprites(self):
        for i in range(0,4):
            x = i*48
            img = self.load_single((x,0,48,26))
            self.heart.append(pygame.transform.scale(img,(192,104)))
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss03_core_shut.png')).convert()
        self.door = pygame.transform.scale(self.load_single((0,0,31,29)),(124,116))

    def setup(self, body_):
        self.body = body_

    def update(self):
        self.flash = (self.flash + (7 + 5.25*(3-self.body.phase)) * self.g.delta_time) % 7
        if self.exposed > 0:
             self.exposed = max(0, self.exposed - self.g.delta_time)
        self.pos = self.rect.center = self.body.pos + vec2(0, 112)
        if self.exposed > 0:
            self.collision_bullet()
        pass

    def collision_bullet(self):
        col = pygame.sprite.spritecollide(self, self.l.bulletsP, False)
        if len(col) > 0:
            for bul in col:
                self.body.hp -= bul.dmg
                bul.hit()

    def render(self):
        item = 3-abs(int(self.flash)-3)
        if self.exposed == 0:
            self.drect.center = self.pos + vec2(-62,0)
            self.l.s.blit(self.door, self.drect.copy().move(-self.l.view))
            self.drect.center = self.pos + vec2(62,0)
            self.l.s.blit(pygame.transform.flip(self.door,True,False), self.drect.copy().move(-self.l.view))
        else:
            self.l.s.blit(self.heart[item], self.rect.copy().move(-self.l.view - vec2(0,30)))
            self.drect.center = self.pos + vec2(-(62 + min(96., 96.*(6.5-self.exposed))),0)
            self.l.s.blit(self.door, self.drect.copy().move(-self.l.view))
            self.drect.center = self.pos + vec2((62 + min(96., 96.*(6.5-self.exposed))),0)
            self.l.s.blit(pygame.transform.flip(self.door,True,False), self.drect.copy().move(-self.l.view))
        pass
