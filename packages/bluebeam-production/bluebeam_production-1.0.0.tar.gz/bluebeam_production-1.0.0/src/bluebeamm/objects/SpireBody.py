import math
from bluebeamm.objects import Enemy
import pygame
from pygame import Vector2 as vec2
import os
import random

class SpireBody(Enemy):
    phase = 4  # phases count in reverse, starts at 4 for the first frame
    body = pygame.sprite.Sprite()

    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._bosscore = None
        self._sprites = []
        self._glass = []
        self._streams = []
        self._commander = []
        self._extensions = []
        self._jets = []
        self.depth = 16
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, 162, 480)
        self.rect.center = self.pos
        self.image = None
        self.contactdmg = 10
        self.pushforce = 960
        self._anims = 0
        self.plrtookdmg = 0
        self.plrlasthp = self.l.player.hp

        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imagedir = os.path.join(os.path.dirname(self.sourceDir), "images/Boss/BetaSpire")
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss02_body.png')).convert()
        self.load_sprites()

        self.activeextents = 1
        self.extentoffset = 0
        self.phasedownexplotime = 0.1
        self.phasedownexplo = 0
        pass

    def load_sprites(self):
        # Body
        for image in range(3):
            x = 72 * (image % 3)
            y = 0
            img = self.load_single((x,y,72,160))
            self._sprites.append(pygame.transform.scale(img, (216,480)))
        self.image = self._sprites[0]
        # Streams
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss02_streams.png'))
        for image in range(4):
            x = 48 * (image % 4)
            y = 0
            img = self.load_single((x,y,48,124))
            self._streams.append(pygame.transform.scale(img, (144,372)))
        # Commander Pilot
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss02_commander.png'))
        for image in range(4):
            x = 36 * (image % 2)
            y = 20 * int(image/2)
            img = self.load_single((x,y,36,20))
            self._commander.append(pygame.transform.scale(img, (108,60)))
        # Glass
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss02_glass.png'))
        for image in range(3):
            x = 0
            y = 27 * image
            img = self.load_single((x,y,48,27))
            self._glass.append(pygame.transform.scale(img, (144,81)))
        # Extensions
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss02_extents.png'))
        # Turret
        img = self.load_single((0, 0, 16, 16))
        self._extensions.append(pygame.transform.scale(img, (48, 48)))
        # Rocket Battery
        img = self.load_single((16, 0, 24, 16))
        self._extensions.append(pygame.transform.scale(img, (72, 48)))
        # BulletBarrage Anti-Cheese Laser
        img = self.load_single((0, 16, 24, 24))
        self._extensions.append(pygame.transform.scale(img, (72, 72)))
        # Jets
        img = self.load_single((24, 16, 16, 24))
        self._extensions.append(pygame.transform.scale(img, (48, 72)))
        # Laser Cannon
        img = self.load_single((0, 40, 40, 24))
        self._extensions.append(pygame.transform.scale(img, (120, 72)))
        # Flames
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss02_jets.png'))
        for i in range(0,3):
            img = self.load_single((12*i, 0, 12, 16))
            self._jets.append(pygame.transform.scale(img, (36, 48)))
            img = self.load_single((24*i, 16, 24, 28))
            self._jets.append(pygame.transform.scale(img, (72, 84)))
            if i == 1:
                self._jets.append(self._jets[0])
                self._jets.append(self._jets[1])

    def movement(self):
        self.pos = self._bosscore.pos + vec2(0,45)
        self.rect.center = self.pos

    def update(self):
        if self._active:
            self.plrtookdmg = max(0, self.plrtookdmg - self.g.delta_time)
            if self.plrlasthp != self.l.player.hp:
                self.plrtookdmg = 0.8
            self.plrlasthp = self.l.player.hp
            if self.rect.colliderect(self.l.player.rect):
                self.hit()
            if self.phasedownexplo > 6:
                self.image = self._sprites[min(max(0,4-self._bosscore.phase), 2)]
            else:
                self.image = self._sprites[min(max(0, 3 - self._bosscore.phase), 2)]
            if self.phasedownexplo > 0:
                self.phasedownexplotime = max(0,self.phasedownexplotime - self.g.delta_time)
                if self.phasedownexplotime <= 0:
                    for i in range(0,3):
                        boom = self.l.create("Explosion", self.pos + pygame.math.Vector2(random.randint(-96,96),random.randint(-128,256)))
                        boom.dmg = 0
                        boom.radius(96)
                        boom.depth = 64
                    self.phasedownexplo -= 1
                    self.phasedownexplotime = 0.1
        else:
            self.check_active()

    def hit(self):
        if (self.contactdmg > 0):
            self.l.player.take_damage(self.contactdmg)
        furthest = 0
        if (abs(self.l.player.pos.x - self._bosscore._popuppts[0].x) < abs(self._bosscore._popuppts[1].x - self.l.player.pos.x)):
            furthest = 1
        else: furthest = -1
        self.l.player.pos += pygame.math.Vector2(self.pushforce * self.g.delta_time * furthest, -self.pushforce/3 * self.g.delta_time)


    def render(self):
        if self._active:
            self._anims = (self._anims + self.g.delta_time / 0.0625) % 8
            # Draw commander
            x = 27
            y = 33
            mode = 0
            if self.phasedownexplo > 0:
                mode = 3
            elif self.plrtookdmg > 0:
                mode = 1 + int(self._anims/2) % 2
            self.l.s.blit(self._commander[mode], self.rect.copy().move(-self.l.view + pygame.math.Vector2(x, y)))
            # Draw glass
            x = 9
            y = 9
            self.l.s.blit(self._glass[min(3-self._bosscore.phase, 2)], self.rect.copy().move(-self.l.view + pygame.math.Vector2(x, y)))
            if self.extentoffset != 0:
                if self.activeextents == 0 or self.activeextents == 4:

                    # Draw turrets
                    x = self.rect.width/2 + (self.rect.width/2 - 18 - 48*(1 - self.extentoffset)) * self._bosscore.playerdir + (-48*(self._bosscore.playerdir==-1))
                    for i in range(0,6):
                        y = self._bosscore._turretpoints[i].y + 212
                        img = self._extensions[0]
                        if self._bosscore.playerdir == 1:
                            img = pygame.transform.flip(img,True,False)
                        self.l.s.blit(img, self.rect.copy().move(-self.l.view + pygame.math.Vector2(x,y)))

                    # Draw laser emitter
                    x = self.rect.width/2 + (self.rect.width/2 - 36 - 24*(1-self.extentoffset)) * self._bosscore.playerdir
                    y = 36 + 72*(1-self.extentoffset)
                    img = self._extensions[2]
                    if self._bosscore.playerdir == -1:
                        img = pygame.transform.flip(img, True, False)
                    self.l.s.blit(img, self.rect.copy().move(-self.l.view + pygame.math.Vector2(x,y)))
                elif self.activeextents == 1:
                    # Draw rocket turrets
                    for i in range(0,2):
                        x = self._bosscore._rocketpoints[i].x
                        y = self._bosscore._rocketpoints[i].y + 212 + 72 * (1 - self.extentoffset)
                        img = self._extensions[1]
                        if i == 0:
                            img = pygame.transform.flip(img, True, False)
                        self.l.s.blit(img, self.rect.copy().move(-self.l.view + pygame.math.Vector2(x, y)))
                elif self.activeextents == 2:
                    # Draw sweep jets and flames
                    x = self.rect.width/2 - 12 + (self.rect.width/2 - 48*(1 - self.extentoffset)) * -self._bosscore.playerdir + (-24*(self._bosscore.playerdir==1))
                    for i in range(0,3):
                        y = self._bosscore._jetpoints[i].y + 212
                        offset = pygame.math.Vector2(
                            0 - 36*(self._bosscore._sweep > 0) + 33*(self._bosscore._sweep > 0 and self._bosscore.playerdir==-1),
                            12 - 18*(self._bosscore._sweep > 0)
                        )
                        img = self._extensions[3]
                        if self._bosscore.playerdir == -1:
                            img = pygame.transform.flip(img,True,False)
                        self.l.s.blit(img, self.rect.copy().move(-self.l.view + pygame.math.Vector2(x, y)))
                        if 4-i > self._bosscore._attackburst:
                            img = self._jets[2*int(math.floor(self._anims) % 4) + (self._bosscore._sweep > 0)]
                            if self._bosscore.playerdir == -1:
                                img = pygame.transform.flip(img, True, False)
                            self.l.s.blit(img, self.rect.copy().move(-self.l.view + offset + pygame.math.Vector2(x - (-9*(self._bosscore.playerdir==1) + 36*self._bosscore.playerdir), y)))
            self.l.s.blit(self.image, self.rect.copy().move(-self.l.view - pygame.math.Vector2(27,0)))
            self.l.s.blit(self._streams[int(self._anims/2) % 4], self.rect.copy().move(-self.l.view + pygame.math.Vector2(9, 99)))
