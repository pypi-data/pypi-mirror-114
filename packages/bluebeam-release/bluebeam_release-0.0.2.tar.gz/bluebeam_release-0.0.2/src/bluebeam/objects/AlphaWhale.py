import math
from bluebeam.objects import Enemy, Laser
import time
import pygame, os
from pygame import Vector2 as vec2
from bluebeam.GlobalVars import GlobalVars

# BOSS 1: Alpha "Whale
# phase 1: 6 turrets + 1 core
## 4 flex turrets: shoot directly at the player
## 2 side turrets: extend downward and fire close to the ground
# phase 2: Y turrets + 2 cores
## 2 flex turrets
## 1 side turret
## 2 cannon turrets: shoot explosive projectiles at the character
## 1 laser turret: travels horizontally and periodically fires a beam
# phase 3: Z turrets + 2 cores + 2 metal shields + commander
## 2 metal shields: destructible parts that protect cores from below
## commander is functionally an invincible turret with more complex attacks

spawns = [[], [], []]

# phase 1 spawning targets
spawns[0] = [["WhaleCore", vec2(0, 0)],
             ["WhaleTurretFlex", vec2(-320, -50), 0],
             ["WhaleTurretFlex", vec2(-80, -100), 1.33],
             ["WhaleTurretFlex", vec2(80, -100), 1.33],
             ["WhaleTurretFlex", vec2(320, -50), 0],
             ["WhaleTurretSide", vec2(-400, -50), 2.165, 0],
             ["WhaleTurretSide", vec2(400, -50), 0, 180]]

# phase 2 spawning targets
spawns[1] = [["WhaleCore", vec2(-320, 32)],
             ["WhaleCore", vec2(320, -32)],
             ["WhaleTurretRocket", vec2(-225, -75), 0],
             ["WhaleTurretFlex", vec2(-75, 0), 0],
             ["WhaleTurretFlex", vec2(75, 0), 1.33],
             ["WhaleTurretRocket", vec2(225, -75), 2.17],
             ["WhaleTurretLaser", vec2(0, 75), 1.33]]

# phase 3 spawning targets
spawns[2] = [["WhaleCore", vec2(-320, 0)],
             ["WhaleCore", vec2(-200, -100)],
             ["WhaleTurretFlex", vec2(100, -100), 1.33],
             ["WhaleTurretFlex", vec2(50, 100), 0],
             ["WhaleCommander", vec2(320, -48)], ]


class AlphaWhale(Enemy):
    phase = 4  # phases count in reverse, starts at 4 for the first frame
    phase_tick = 0  # tickdown for phase changes, for the moving animation...
    cores = pygame.sprite.Group()  # contains only "WhaleCore enemies
    turrets = pygame.sprite.Group()

    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._objid = 2
        self._hp = 1
        self._mhp = 1
        self._contactdmg = 0
        self.tpos = pos_
        self.floattick = 0
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, 0, 0)
        self.rect.center = self.pos
        self.frect = pygame.rect.Rect(self.pos.x, self.pos.y, 960, 360)
        self.frect.center = self.pos
        self.floatoffset = -4000
        self.deathstate = 0
        self.deathoffset = pygame.math.Vector2()
        self.fadetimer = 0

        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images/boss/AlphaWhale")
        self.spritesheet = pygame.image.load(os.path.join(self.imageDir, 'boss01_body.png')).convert()
        self.load_sprites()

        pass

    def load_sprites(self):
        img = self.load_single((0,0,320,48))
        self.image = pygame.transform.scale(img, (3200,480))

    def update(self):
        if(self._active):
            self.pos = vec2(self.floatoffset,0) + self.deathoffset + self.tpos + vec2(18*math.cos(self.floattick * 4.5), 8*math.sin(self.floattick*2.25))
            self.rect.center = self.frect.center = self.pos
            self.floattick += self.g.delta_time
            self._hp = 0
            if abs(self.floatoffset) > 0:
                sub = self.g.delta_time * 600
                self.floatoffset = math.copysign(max(abs(self.floatoffset) - sub, 0),self.floatoffset)
            for core in self.cores:
                self._hp += core.hp
            if self._hp <= 0 and self.phase_tick <= 0 and self.deathstate == 0:
                self.phase_down()
            if self.deathstate == 1:
                self.fadetimer -= self.g.delta_time
                self.deathoffset += vec2(600 * self.g.delta_time, 200 * self.g.delta_time)
                if self.fadetimer <= 0:
                    self.death()
        else:
            self.check_active()

    def phase_down(self):
        self.phase -= 1
        # fallback item
        for core in self.cores:
            core.death()
        for turret in self.turrets:
            turret.death()
        for eb in self.l.bulletsE:
            if isinstance(eb, Laser):
                eb.fadeout()
            else:
                eb.hit()
        if self.phase <= 0:
            self.deathstate = 1
            self.fadetimer = 5.5
            pygame.mixer.music.fadeout(1800)
        else:
            if self.phase!=3: self.floatoffset = 1000
            self.phase_change()

    def phase_change(self):
        for spawn in spawns[3 - self.phase]:
            item = self.l.create(spawn[0], self.pos)
            item.anchorpos = spawn[1]
            item.anchor = self
            if spawn[0] == "WhaleCore":
                self.cores.add(item)
            else:
                self.turrets.add(item)
                if spawn[0] == "WhaleTurretFlex" or spawn[0] == "WhaleTurretRocket":
                    item.shotcd = 5.5 + spawn[2]
                elif spawn[0] == "WhaleTurretSide":
                    item.shotcd = 5.5 + spawn[2]
                    item.rot = spawn[3]
                elif spawn[0] == "WhaleTurretLaser":
                    item.endpoints[0] = 420
                    item.endpoints[1] = -420
        if self.phase == 3:
            self._mhp = 250
        elif self.phase == 2:
            self._mhp = 500
            pass
        elif self.phase == 1:
            self._mhp = 500
            pass

    def death(self):
        self.l.bossDeathState = 1
        self.l.uncreate(self.instid)

    def render(self):
        if self.phase>0 and self._active:
            # Draw boss health bar at bottom of screen
            sz = self.g.screen_size
            mid = sz[0] / 2 - 490
            top = 80
            hel = float(self._hp / self._mhp) * 968
            pygame.draw.rect(self.l.s, (128,0,96,0)   , pygame.rect.Rect(mid  ,top  ,980,60))
            pygame.draw.rect(self.l.s, (255,0,192,100), pygame.rect.Rect(mid+6,top+6,hel,48))

        self.l.s.blit(self.image, pygame.rect.Rect(self.pos.x - 500 - 1000 * min(3-self.phase,2), self.pos.y - 292, 3000, 424).move(-self.l.view))