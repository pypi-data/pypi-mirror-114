from bluebeamm.objects import Enemy
from bluebeamm.objects import Tentacle
import pygame
import os


class BulkyEnemy(Enemy):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.rect = pygame.rect.Rect(0, 0, 150, 245)
        self.rect.center
        self._mhp = 150
        self.hp = self._mhp
        self.idied = 0

        self.speed = pygame.math.Vector2(550, 1100)
        self.accel = 0.05
        self.gravity = 80
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images/Enemy/BulkyGuy")

        self.max_attack_cd = 1
        self.attack_cd = self.max_attack_cd
        self.tentacle = None

        self.left = True

        #for image/animation
        self.attacking = False
        self.current_position = 0
        self.animation_counter = 0
        self.walk_right = []
        self.walk_left = []
        for image in range(1,4):
            img_right = pygame.image.load(os.path.join(self.imageDir,f'BulkWalk{image}.png')).convert_alpha()
            img_right = pygame.transform.scale(img_right, (326, 258))
            img_left = pygame.transform.flip(img_right, True, False)
            self.walk_right.append(img_right)
            self.walk_left.append(img_left)

        self.attack_right = []
        self.attack_left = []

        for image in range(1,8):
            img_right = pygame.image.load(os.path.join(self.imageDir,f'BulkAttack{image}.png')).convert_alpha()
            img_right = pygame.transform.scale(img_right, (326, 258))
            img_left = pygame.transform.flip(img_right, True, False)
            self.attack_right.append(img_right)
            self.attack_left.append(img_left)



        self.image = self.walk_left[self.current_position]


    def update_ai_inputs(self):
        if( self.attacking == False): 
            self.try_attack()
        self.xmove()

    def try_attack(self):
        if(self.attack_cd <= 0):
            above = self.l.player.y < self.y - 100
            xdist = abs(self.l.player.x - (self.x + self.vel.x * self.g.delta_time))
            if(xdist <= 400):
                if(above):
                    self.try_jump(cd=1)
                else:
                    self.attacking = True
                    self.animation_counter = 0
                    self.current_position = 0
            elif(above):
                self.try_jump(cd=0.3)
            elif(xdist >= 600 and self.l.player.y < self.y - 50):
                self.try_jump(cd=0)
        else:
            self.attack_cd -= self.g.delta_time

    def xmove(self):
        # Should I go left or right?
        if(self.attacking == False or self.current_position < 2):
            if (self.l.player.x < self.x - 80):
                targ_xvel = -self.speed.x
                if (self.vel.x > targ_xvel):
                    self.vel.x -= self.speed.x * self.accel

            elif (self.l.player.x > self.x + 80):
                targ_xvel = self.speed.x
                if (self.vel.x < targ_xvel):
                    self.vel.x += self.speed.x * self.accel
                    #left = False
            if (self.l.player.x < self.x):
                self.left = True
            else:
                self.left = False
        else:
            self.slow_down(self.speed.x * .01)
        self.update_animation(self.left)
    
    def try_jump(self, cd=0.3):
        if (self.pstate == 0):
            if(self.attack_cd <= 0):
                self.jumping=True
                self._vel.y = -self.speed.y
                self.attack_cd = cd

    def slow_down(self, xspeed):
        if (self.vel.x < 0):
            self.vel.x += xspeed
        elif (self.vel.x > 0):
            self.vel.x -= xspeed

        if (abs(self.vel.x) < xspeed):
            self.vel.x = 0

    def update_animation(self, left):
        attack_delays = [15,25,20,3,3,20,5]
        #attack_delays = [50,50,50,50,50,50,50]
        #animation_counter = 0
        #if left:
        self.animation_counter += 1
        if self.attacking:
            if self.animation_counter >= attack_delays[self.current_position]:
                if(self.tentacle):
                    self.l.uncreate(self.tentacle.instid)
                    self.tentacle = None
                self.animation_counter = 0
                self.current_position += 1
                tentacle_num = self.current_position + 1
                if (4 <= tentacle_num and tentacle_num <= 7):
                    self.tentacle = Tentacle.Tentacle(self.g, self.l, tentacle_num, self.left, self._pos)
                    self.tentacle._from_bulky = True
                    self.l.bulletsE.add(self.tentacle)
                if self.current_position >= 7:
                    self.current_position = 0
                    self.attacking = False
                    self.attack_cd = self.max_attack_cd
            
        else:
            if self.animation_counter >= 10:
                self.animation_counter = 0
                self.current_position += 1
                if self.current_position >= 3:
                    self.current_position = 0

        if self.attacking:
            if left: self.image = self.attack_left[self.current_position]
            else: self.image = self.attack_right[self.current_position]
        else:
            if left: self.image = self.walk_left[self.current_position]
            else: self.image = self.walk_right[self.current_position]

    def death(self):
        if(self.tentacle):
            self.l.uncreate(self.tentacle.instid)
        self.l.uncreate(self.instid)

    def update(self):
        super().update()
        if(self._active):
            self.update_ai_inputs()
        if(self.tentacle):
            self.tentacle.refresh_pos(self._pos + self._vel*self.g.delta_time)

    def render(self):
        # pygame.draw.rect(self.l.s,
        #                  (128 + 127 * (1 - self.idied), 128, 128 + (127 * self.idied), 100),
        #                  self.rect.copy().move(-self.l.view))
        
        if(self.left):
            self.l.s.blit(self.image, self.rect.copy().move(-self.l.view - (150,0)))
        else:
            self.l.s.blit(self.image, self.rect.copy().move(-self.l.view - (0,0)))
        pygame.draw.rect(self.l.s,
                         (255, 0, 0, 100),
                         pygame.rect.Rect(self.rect.topleft[0], self.rect.topleft[1] - 24, 100, 16).move(-self.l.view))
        pygame.draw.rect(self.l.s,
                         (0, 255, 0, 100),
                         pygame.rect.Rect(self.rect.topleft[0],
                                          self.rect.topleft[1] - 24,
                                          100 * (self.hp / self._mhp),
                                          16).move(-self.l.view))