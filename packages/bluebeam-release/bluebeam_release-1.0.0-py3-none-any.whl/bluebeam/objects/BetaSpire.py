import math
from bluebeam.objects import Enemy, Laser, HomingRocket
import pygame
from pygame import Vector2 as vec2
import random
import os


# BOSS 2: Beta Spire
# Phase 1: Attacks using homing rockets, bullet barrage, sweeping the screen
# Phase 2: Attacks using homing rockets+, sweeping the screen, laser barrage
# Phase 3 Attacks using sweeping the screen, laser barrage, Air Man knockoff pattern

# There are only two objects making up the boss: this, and the boss body

class BetaSpire(Enemy):
    phase = 3  # phases count in reverse, starts at 4 for the first frame
    phase_tick = 0  # tickdown for phase changes, for the moving animation...
    body = pygame.sprite.Sprite()

    attacks = {
        0: "self.BulletBarrage()",
        1: "self.HomingRockets()",
        2: "self.ScreenSweep()",
        3: "self.LaserBarrage()",
        4: "self.ThatGuyYouCantBeat()",
    }
    attackbursts = (3, 2, 4, 24, 5)

    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self._hp = 1
        self._mhp = 1
        self._contactdmg = 0
        self.tpos = pos_
        self.rect = pygame.rect.Rect(self.pos.x, self.pos.y, 72, 72)
        self.rect.center = self.pos
        self.image = None
        self.depth = 32

        self.anchorpos = vec2()
        self._arenabounds = [vec2(), vec2()]
        self._popuppts = [vec2(), vec2(), vec2(), vec2(), vec2()]
        self._nextpopup = 0
        self._popupamt = 960
        self.movemode = 0
        self.waitformove = 0

        self._nextattack = 0 #random.randint(0,1)
        self._attacksuntilretreat = 0
        self._attackcooldown = 1.2
        self._attackburst = 0
        self._turretpoints = [vec2(), vec2(), vec2(), vec2(), vec2(), vec2()]
        self._rocketpoints = [vec2(), vec2()]
        self._jetpoints = [vec2(), vec2(), vec2()]
        self._sweep = 0

        self._sprites = []
        self._glow = 0.0
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imagedir = os.path.join(os.path.dirname(self.sourceDir), "images/Boss/BetaSpire")
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss02_core.png')).convert()
        self.load_sprites()
        self.playerdir = 1

        self.phase_change()
        pass

    def load_sprites(self):
        for image in range(4):
            x = 24 * (image % 2)
            y = 24 * math.floor(image / 2)
            img = self.load_single((x, y, 24, 24))
            self._sprites.append(pygame.transform.scale(img, (72, 72)))
        self.image = self._sprites[0]

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp_):
        self._hp = hp_
        if self._hp <= 0 and self.phase > 0:
            self.phase_down()

    def setup(self, arena_lt, arena_rb):
        self.body = self.l.create("SpireBody", self.pos.xy)
        self.body._bosscore = self
        self._anchorpos = (arena_lt + arena_rb) / 2
        self._arenabounds = [arena_lt, arena_rb]
        self._nextpopup = 1
        for i in range(0, 6):
            self._turretpoints[5 - i] = vec2(self.body.rect.width / 2,
                                             128 + (i * (self.body.rect.height - 160) / 5 - self.body.rect.height / 2))
        for i in range(0, 2):
            self._rocketpoints[i] = vec2(self.body.rect.width / 2 + -72 + 72 * i, -156)
        for i in range(0, 3):
            self._jetpoints[i] = (self._turretpoints[2*i] + self._turretpoints[2*i+1])/2
        self.body.movement()
        self.determinepopups()
        self._attackcooldown = 1.2
        self._nextattack = 1
        self.body.activeextents = self._nextattack
        self._attackburst = self.attackbursts[self._nextattack]

    def determinepopups(self):
        h = 2
        space = ((self._arenabounds[1].x - self._arenabounds[0].x) - self.body.rect.width) / (h - 1)
        for i in range(0, h):
            self._popuppts[i] = vec2(self._arenabounds[0].x + self.body.rect.width / 2 + space * i,
                                     self._arenabounds[1].y - 284)

    def movement(self):
        if self.movemode == 0:
            self._popupamt = max(0, self._popupamt - 720 * self.g.delta_time)
        elif self.movemode == 1:
            self._popupamt = min(960, self._popupamt + 720 * self.g.delta_time)
        self.pos = self._popuppts[self._nextpopup] + vec2((self._sweep * self.playerdir), self._popupamt)
        self.rect.center = self.pos
        if self._sweep == 0:
            self.playerdir = math.copysign(1, self.l.player.pos.x - self.pos.x)
        self.body.movement()

    def update(self):
        if self._active:
            if self.phase > 0:
                self.spire_logic()
                self.collision_bullet()
            else:
                self.fadetimer = max(0, self.fadetimer - self.g.delta_time)
                if self.fadetimer < 4.5:
                    self.rect.center = self.pos = self.pos + vec2(0,300) * self.g.delta_time
                    self.body.movement()
                if self.fadetimer == 0:
                    self.death()
        else:
            self.check_active()

    def spire_logic(self):
        if self.waitformove == 0 or self._nextattack == 2:
            self.movement()

        if self.movemode == 0 and self._popupamt == 0 and self.waitformove == 0:
            self.waitformove = 1.2
            self._attackcooldown = 1.2
            self._attackburst = self.attackbursts[self._nextattack]

        elif self.movemode == 1 and self._popupamt == 960 and self.waitformove == 0:
            self.waitformove = 1.2
            self._attackcooldown = 0
            self._nextpopup = random.randint(0, 1)
            self._nextattack = random.randint(0, 2) + (3-self.phase)
            self.body.activeextents = self._nextattack
            self._sweep = 0

        if self._attackcooldown == 0 and self._attackburst == 0 and self.waitformove > 0:
            self.waitformove = max(0, self.waitformove - self.g.delta_time)
            self.body.activeextents = self._nextattack
            self.body.extentoffset = (self.movemode == 0) * max(0.0, self.waitformove - 0.4) / 0.8
            if self.waitformove == 0:
                self.movemode = 1 - self.movemode
                if (self.movemode == 0):
                    self._attackburst = self.attackbursts[self._nextattack]

        elif self.movemode == 0 and self._popupamt == 0:
            self._attackcooldown = max(0, self._attackcooldown - self.g.delta_time)
            if self._attackburst == self.attackbursts[self._nextattack]:
                self.body.extentoffset = 1 - (max(0.0, self._attackcooldown - 0.4) / 0.8)
            if self._attackcooldown == 0 and self._attackburst > 0:
                eval(self.attacks[self._nextattack])

    def death(self):
        if self.deathstate == 1 and self.fadetimer == 0:
            self.l.bossDeathState == 1
            self.l.uncreate(self.instid)

    def phase_down(self):
        self.phase -= 1
        # fallback item
        for eb in self.l.bulletsE:
            if isinstance(eb, Laser):
                eb.fadeout()
            else:
                eb.hit()
        if self.phase <= 0:
            self.body.phasedownexplo = 80
            self.deathstate = 1
            self.fadetimer = 5.5
            pygame.mixer.music.fadeout(1800)
        else:
            self.body.phasedownexplo = 12
            self.waitformove = 0.8
            self._attackburst = 0
            self.phase_change()

    def phase_change(self):
        if self.phase == 3:
            self._mhp = 200
        elif self.phase == 2:
            self._mhp = 250
            pass
        elif self.phase == 1:
            self._mhp = 300
        self._hp = self._mhp

    def attack(self):
        pass

    def BulletBarrage(self):
        if self._attackburst == self.attackbursts[0]:
            las = self.l.create("Laser", vec2(self.body.pos.x + 24 + 2 + 48 * self.playerdir, self.body.pos.y - 160))
            las.width = 48
            las.dir = 1 - self.playerdir
            las.lifespan = 1.75
        patterns = [
            (0, 5),
            (0, 3),
            (0, 1),
            (0, 1, 2),
            (0, 1, 5),
            (0, 1, 4, 5),
            (1, 2),
        ]
        select = random.randint(0, len(patterns) - 1)
        for i in patterns[select]:
            bul = self.l.create("EnemyBullet", self.body.pos + self._turretpoints[i])
            bul.vel = vec2(self.playerdir * 800, 0)
        self._attackburst -= 1
        self._attackcooldown = 0.75
        pass

    def HomingRockets(self):
        for i in range(0, 2):
            hom = self.l.create("HomingRocket", self.body.pos + self._rocketpoints[i])
        self._attackburst -= 1
        self._attackcooldown = 1.6
        pass

    def ScreenSweep(self):
        if (self._attackburst > 1):
            self._attackburst -= 1
            self._attackcooldown = 1 - 0.2*(3-self.phase)
            pass
        else:
            self._sweep += self.g.delta_time * 1350
            self.body.pushforce = 0
            self.body.contactdmg = 20
            if self._sweep > self._arenabounds[1].x - self._arenabounds[0].x:
                self.body.pushforce = 960
                self.body.contactdmg = 10
                self._attackburst = 0
                self._attackcooldown = 0
                self.waitformove = 0.1
            pass
        pass

    def LaserBarrage(self):
        if self._attackburst > 17:
            las = self.l.create("Laser",
                                vec2(self.body.pos.x + (128 + 160 * (24 - self._attackburst)) * self.playerdir,
                                     self.body.pos.y - 512))
            las.width = 48
            las.dir = 1
            las.warmup = 0.67
            las.lifespan = 0.3
            self._attackcooldown = 0.14
        elif 17 >= self._attackburst > 10:
            las = self.l.create("Laser",
                                vec2(self.body.pos.x + (64 + 160*7 - 160 * (17 - self._attackburst)) * self.playerdir,
                                     self.body.pos.y - 512))
            las.width = 48
            las.dir = 1
            las.warmup = 0.67
            las.lifespan = 0.3
            self._attackcooldown = 0.12
        elif 10 >= self._attackburst > 3:
            las = self.l.create("Laser",
                                vec2(self.body.pos.x + (128 + 160 * (10 - self._attackburst)) * self.playerdir,
                                     self.body.pos.y - 512))
            las.width = 48
            las.dir = 1
            las.warmup = 0.6
            las.lifespan = 0.3
            self._attackcooldown = 0.09
        elif self._attackburst > 0:
            alt = (abs(self._attackburst - 1) % 2)
            las = self.l.create("Laser",
                                vec2(self.body.pos.x + (128 + 992 * alt) * self.playerdir,
                                     self.body.pos.y - 512))
            las.width = 96
            las.dir = 1
            las.warmup = 1.0
            las.lifespan = 1.25
            las.b2speed = (450 * self.playerdir * (1 - 2*alt))
            self._attackcooldown = 1.8
        self._attackburst -= 1

    def ThatGuyYouCantBeat(self):
        if self._attackburst == self.attackbursts[0]:
            las = self.l.create("Laser", vec2(self.body.pos.x + 24 + 2 + 48 * self.playerdir, self.body.pos.y - 160))
            las.width = 48
            las.dir = 1 - self.playerdir
            las.lifespan = 2.4
            las.warmup = 0.8
        patterns = [
            (0, 10, 12),
            (5, 6, 9, 13),
            (15, 7, 0),
        ]
        select = random.randint(0, len(patterns) - 1)
        for i in patterns[select]:
            bul = self.l.create("SuperEnemyBullet", self.body.pos + vec2(self._turretpoints[(i%6)].x * self.playerdir, self._turretpoints[(i%6)].y))
            bul.targets = [self.body.pos + vec2((192 + 128*math.floor(i/6))*self.playerdir, 0)+ vec2(0,self._turretpoints[(i%6)].y), self.body.pos + vec2(3072*self.playerdir, 0)+ self._turretpoints[i%6]]
        self._attackburst -= 1
        self._attackcooldown = 0.8
        pass

    def death(self):
        self.l.uncreate(self.body.instid)
        self.l.uncreate(self.instid)
        self.l.bossDeathState = 1

    def render(self):
        if self._active:
            self._glow += 7.5 * self.g.delta_time
            if (self._glow >= 7):
                self._glow -= 7
            self.image = self._sprites[3 - int(abs(3 - self._glow))]
            self.l.s.blit(self.image, self.rect.copy().move(-self.l.view))
            if self.phase > 0 and self._active:
                # Draw boss health bar at bottom of screen
                sz = self.g.screen_size
                mid = sz[0] / 2 - 490
                top = 80
                hel = float(self._hp / self._mhp) * 968
                pygame.draw.rect(self.l.s, (128, 0, 96, 0), pygame.rect.Rect(mid, top, 980, 60))
                pygame.draw.rect(self.l.s, (255, 0, 192, 100), pygame.rect.Rect(mid + 6, top + 6, hel, 48))
