from bluebeam.objects import Enemy
import pygame, math, random, os
from pygame import Vector2 as vec2

class GammaHand(Enemy):
    def __init__(self, g, l, pos):
        super().__init__(g, l, pos)
        self.rect = pygame.rect.Rect(0, 0, 144, 144)
        self.frect = pygame.rect.Rect(0, 0, 192, 192)
        self.body = None
        self.handtype = vec2(1, 1)
        self.sprites = []
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imagedir = os.path.join(os.path.dirname(self.sourceDir), "images/Boss/GammaGenerator")
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss03_hands.png')).convert()
        self.load_sprites()

        self.punchstarts = [vec2(), vec2()]
        self.groundlevel = 0

        self.depth = 11

        self.mode = 0
        self.stateclock = 0
        self.bob = 0
        self.boffset = 0
        self._contactdmg = 0

        self.moveto = vec2()
        self.radiatetarg = vec2()
        self.radiatebursts = 10
        self.radiaterange = [vec2(), 0]

        self.corridorclock = 0

        self.emitpoint = self.pos.xy

    def load_sprites(self):
        for i in range(0,2):
            x = i*48
            img = self.load_single((x,0,48,48))
            self.sprites.append(pygame.transform.scale(img,(192,192)))

    def setup(self, body_, right_, bottom_):
        self.body = body_
        self.handtype = vec2(-1 + 2*right_, -1 + 2*bottom_)
        self.rect.center = self.pos = self.body.pos
        self.groundlevel = self.body.groundlevel
        self.punchstarts[0] = vec2(self.body.bounds[0].x, self.body.bounds[0].y)
        self.punchstarts[1] = vec2(self.body.bounds[1].x, self.body.bounds[0].y + 144)
        if bottom_:
            self.boffset = 90

    def update(self):
        self.process()
        self.collision_player()

    def state(self, mode_):
        self.mode = mode_
        self.stateclock = 0
        if mode_ == 2:
            self.radiatebursts = 0
            self.radiate_reposition()
        if mode_ == 3 or mode_ == 5:
            self.moveto = vec2(self.punchstarts[int(0.5 + self.handtype.x/2)].x, self.punchstarts[0].y)
            self.radiatebursts = 0
        if mode_ == 6:
            self.radiatebursts = 0
            self.corridorclock = 0
            self.moveto = vec2(self.body.pos.x + 140 * self.handtype.x, self.punchstarts[0].y)

    def process(self):
        states = {
            0: self.idle,
            1: self.punch,
            2: self.radiate,
            3: self.laser_A,
            4: self.laser_B,
            5: self.corridor_laser,
            6: self.corridor_bullet,
        }
        states[self.mode]()

    def smooth_move(self, target_, speed):
        mag = (target_ - self.pos).magnitude()
        if mag > 0:
            if (target_ - self.pos).magnitude() < math.pow(mag,0.45):
                self.rect.center = self.pos = target_
            else:
                amt = min(speed*self.g.delta_time, math.pow(mag,0.45))
                self.rect.center = self.pos = self.pos + amt * (target_ - self.pos).normalize()

    def idle(self):
        x = 240 + 60*(self.handtype.y==1)
        y = 120 * self.handtype.y - 60 + math.cos(math.radians(self.body.bob + self.boffset))*48
        self.smooth_move(self.body.pos + vec2(x * self.handtype.x, y), 300)
        pass

    def punch(self):
        x = self.punchstarts[int(0.5 + self.handtype.x)].x
        y = self.punchstarts[int(0.5 + self.handtype.y)].y
        if self.stateclock == 0 and self.pos != vec2(x,y):
            self.stateclock = 0
            self.smooth_move(vec2(x,y), 1600)
        else:
            self.stateclock += self.g.delta_time
            if self.stateclock > 2.0:
                self.state(0)
            elif self.stateclock > 0.8:
                self.swing()

    def swing(self):
        offset = ((self.body.phase<=2) and (self.handtype.y == -1)) * 72
        if self.stateclock < 1:
            self._contactdmg = 10
            div = ((self.stateclock - 0.8) / 0.2)
            x = self.punchstarts[int(0.5+self.handtype.x)].x
            y = self.punchstarts[int(0.5+self.handtype.y)].y
            am = vec2(x,y) - self.body.pos
            targ = vec2(192*self.handtype.x, self.body.bounds[1].y-self.body.pos.y-offset)
            self.rect.center = self.pos = self.body.pos + am.slerp(targ, div)
        elif self.stateclock < 1.2:
            div = ((self.stateclock - 1.0) / 0.2)
            am = vec2(192*self.handtype.x, self.body.bounds[1].y-self.body.pos.y-offset)
            targ = vec2(self.body.bounds[1-int(0.5+self.handtype.x)].x - self.body.pos.x, self.body.bounds[1].y-self.body.pos.y -offset - 96)
            self.rect.center = self.pos = self.body.pos + am.lerp(targ, div)
        elif self.stateclock > 1.5:
            x = 240 + 60 * (self.handtype.y == 1)
            y = 120 * self.handtype.y - 60 - offset
            self.smooth_move(self.body.pos + vec2(x * self.handtype.x, y), 650)
            self._contactdmg = 0
        elif self.stateclock > 2:
            self.state(0)

    def radiate(self):
        if self.pos != self.moveto:
            self.stateclock = 0
            self.smooth_move(self.moveto, 1600)
            self.radiate_genangles(45)
        else:
            self.stateclock += self.g.delta_time
            if self.stateclock >= 0.3 and self.radiatebursts == 0:
                self.radiate_genangles(45)
                self.radiatebursts = 1
            elif self.radiatebursts >= 1 and self.stateclock >= 0.45 - 0.03*(3-self.body.phase):
                self.stateclock = 0
                self.radiate_fire()
                self.radiatebursts += 1
                if (self.radiatebursts % (3+(3-self.body.phase))) == 1:
                    if self.radiatebursts == 10 + 3*(3-self.body.phase):
                        self.state(0)
                    else:
                        self.radiate_reposition()
                        self.radiate_genangles(45)

    def radiate_reposition(self):
        self.rect.center = self.pos
        #self.moveto = self.pos
        self.moveto = vec2(random.randint(self.body.bounds[0].x + 144, self.body.bounds[1].x - 144), random.randint(self.body.bounds[0].y + 144, self.body.bounds[1].y - 288))

    def radiate_genangles(self, spread):
        plrang = (self.l.player.pos - self.pos).normalize()
        self.radiaterange[0] = plrang.rotate(-spread)
        self.radiaterange[1] = spread

    def radiate_fire(self):
        pass
        for i in range(0,3 + int(0.5*(3-self.body.phase))):
             rand = random.random() * (self.radiaterange[1]*2)
             ang = self.radiaterange[0].rotate(round(rand/5)*5)
             bullet = self.l.create("EnemyBullet", vec2(self.pos.x, self.pos.y))
             bullet.speed = ang * 650
             bullet.depth = 24

    def laser_A(self):
        if self.pos != self.moveto and self.radiatebursts % 2 == 0:
            self.smooth_move(self.moveto, 1200)
            self.emitpoint = self.pos
            if self.pos == self.moveto:
                self.radiatebursts += 1
                self.laser_A_fire()
            pass
        else:
            a = (self.body.bounds[1].x - self.body.bounds[0].x) / (450 + 30*(3-self.body.phase))
            self.stateclock += self.g.delta_time
            if self.stateclock > 0.7 + a + 0.4:
                self.state(0)
            elif self.stateclock > 0.7 + a:
                self.pos = vec2(self.body.bounds[int(0.5 - self.handtype.x/2)].x + 192 * self.handtype.x, self.moveto.y)
            elif self.stateclock > 0.7:
                self.pos = self.moveto.lerp(vec2(self.body.bounds[int(0.5 - self.handtype.x/2)].x + 192 * self.handtype.x, self.moveto.y),min(1.0,(self.stateclock-0.7)/a))
            self.emitpoint = self.pos
            self.rect.center = self.pos
        pass

    def laser_A_fire(self):
        las = self.l.create("Laser", self.pos.xy)
        las.warmup = 0.7
        las.width = 96
        las.depth = 16
        las.dir = 1
        las.lifespan = (self.body.bounds[1].x - self.body.bounds[0].x) / (400 + 50*(3-self.body.phase)) + 0.2
        las._emitter = self

    def laser_B(self):
        pass

    def corridor_laser(self):
        if self.radiatebursts == 0 and self.pos != self.moveto:
            self.smooth_move(self.moveto, 750)
            if self.pos == self.moveto:
                self.radiatebursts = 1
                self.corridor_laser_fire()
                pass
        else:
            self.stateclock += self.g.delta_time
            if self.stateclock > 16:
                self.state(0)
            if self.stateclock > 4:
                self.pos = self.rect.center = vec2(self.body.pos.x + 256 * self.handtype.x, self.moveto.y)
            elif self.stateclock > 1:
                self.pos = self.rect.center = self.moveto.lerp(vec2(self.body.pos.x + 256 * self.handtype.x, self.moveto.y), (self.stateclock - 1) / 3)
            self.emitpoint = self.pos
        pass

    def corridor_laser_fire(self):
        las = self.l.create("Laser", self.pos.xy)
        las.warmup = 1
        las.width = 150
        las.dir = 1
        las.depth = 16
        las.lifespan = 13
        las._emitter = self

    def corridor_bullet(self):
        if self.radiatebursts == 0 and self.pos != self.moveto:
            self.smooth_move(self.moveto, 300)
            if self.pos == self.moveto:
                self.radiatebursts = 1
                pass
        else:
            self.stateclock += self.g.delta_time
            self.corridorclock += self.g.delta_time
            if self.stateclock > 13:
                self.state(0)
            elif self.corridorclock > 2.5 and self.radiatebursts == 1:
                self.corridor_bullet_fire()
                self.corridorclock = 0
                self.radiatebursts = 2
            elif self.radiatebursts >= 2 and self.corridorclock > 1.0 - (self.body.phase == 1)*0.05 - min(0.15, (self.radiatebursts - 2)/50):
                self.corridor_bullet_fire()
                self.corridorclock = 0
                self.radiatebursts += 1

    def corridor_bullet_fire(self):
        for i in range(0,3):
            bul = self.l.create("EnemyBullet",self.pos.xy)
            bul.speed = vec2(math.cos(math.radians(90+5*i*self.handtype.x)),math.sin(math.radians(90+5*i*self.handtype.x))) * 750
            bul.depth = 16
        pass

    def death(self):
        boom = self.l.create("Explosion",self.pos.xy)
        boom.radius(480)
        boom.dmg = 0
        boom.depth = 64
        self.l.uncreate(self.instid)

    def render(self):
        type=0
        self.frect.center = self.rect.center
        if self.body.explo > 0 or self.mode == 2 or self.mode == 3 or self.mode == 5 or self.mode == 6:
            type=1
        img = self.sprites[type]
        if self.handtype.x==1:
            img = pygame.transform.flip(img,True,False)
        self.l.s.blit(img,self.frect.copy().move(-self.l.view))