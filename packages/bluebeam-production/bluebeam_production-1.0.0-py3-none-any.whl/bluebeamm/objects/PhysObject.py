from bluebeamm.objects import GameObject
import pygame
import math


# PHYSICS OBJECTS
# Physics objects are game objects with physics.
# Physics objects have the following attributes:
## Velocity (Vec2, objects should move by this much per tick as long as they aren't blocked)
## Gravity (float, added to velocity per tick when in air and not hovering)
## Physics State (int)
### 0: Ground State (Object is on ground)
### 1: Air State (Object is not on ground)
### 2: Hover State (Object ignores gravity entirely)

# I'm going to need assistance with handling collisions - specifically, actually detecting them. 
# Once I've figured out how to do that or someone else has gotten to it, then I can implement the physics update function.
# If anyone else wants to do that, make sure to check for horizontal collisions before vertical ones.

class PhysObject(GameObject):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._objid = 1
        self._vel = pygame.math.Vector2(0, 0)
        self._gravity = 0
        self._pstate = 0
        self._speed = pygame.math.Vector2(200,200)
        self._collide_terrain = True

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, vel_):
        if isinstance(vel_, pygame.math.Vector2): self._vel = vel_

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed_):
        self._speed = speed_

    @property
    def gravity(self):
        return self._gravity

    @gravity.setter
    def gravity(self, gravity_):
        self._gravity = gravity_

    @property
    def pstate(self):
        return self._pstate

    @pstate.setter
    def pstate(self, pstate_):
        self._pstate = pstate_

    @property
    def collide_terrain(self):
        return self._collide_terrain

    @collide_terrain.setter
    def collide_terrain(self, col):
        self._collide_terrain = col

    def update_phys(self, gravity_mod=1):
        if (self.pstate == 1):
            self.vel.y += self.gravity * gravity_mod
        ovel = pygame.math.Vector2(self.vel.x, self.vel.y)
        self.vel *= self.g.delta_time

        # Physics calculations go here.

        # Collision checks: start with horizontal velocity
        xv_bounce = self.ccheck_h()
        self.pos.x += self.vel.x - math.modf(self.vel.x)[0]
        self.rect.center = self.pos

        # Next, vertical velocity
        yv_reset = self.ccheck_v()
        self.pos.y += self.vel.y - math.modf(self.vel.y)[0]
        self.rect.center = self.pos

        self.vel = ovel
        if (yv_reset): self.vel.y = 0
        if (xv_bounce): self.vel.x = 0

    def update(self):
        self.update_phys()

    # Horizontal movement collision checking
    def ccheck_h(self):
        if(self.collide_terrain==False): return False
        
        xv_bounce = False
        cc = self.rect.copy()
        for i in range(1, math.ceil(abs(self.vel.x))):
            self.rect = self.rect.move(math.copysign(1, self.vel.x), 0)
            if self.collision_terrain():
                xv_bounce = True
                self.vel = pygame.math.Vector2(math.copysign(i - 1, self.vel.x), self.vel.y)
                break
        self.rect = cc
        return xv_bounce

    # Vertical movement collision checking
    def ccheck_v(self):
        if(self.collide_terrain==False): return False

        yv_reset = False
        if (self.pstate == 0): self.pstate = 1
        cc = self.rect.copy()
        for i in range(1, math.ceil(abs(self.vel.y))):
            self.rect = self.rect.move(0, math.copysign(1, self.vel.y))
            if self.collision_terrain(True):
                yv_reset = True
                self.vel = pygame.math.Vector2(self.vel.x, math.copysign(i - 1, self.vel.y))
                break
        self.rect = cc
        return yv_reset

    def collision_terrain(self, vertical=False):
        col = pygame.sprite.spritecollide(self, self.l.terrain, False)
        if len(col) > 0:
            # Update pstate to determine if the PhysObject is grounded
            if (vertical): self.check_grounded(col)
            return 1
        else:
            return 0

    def check_grounded(self, col):
        if (self.pstate == 1):
            for c in col:
                if ( self.rect.bottom - 1 <= c.rect.top ):
                    # Player is grounded
                    self.pstate = 0
                    
                elif( self.rect.top < c.rect.top ):
                    # If we are here, we are partially stuck in the ground
                    # As such, we'll correctively increase our y position by 1 until we aren't stuck
                    self.pos.y -= 1
