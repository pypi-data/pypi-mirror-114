#GAMMAGENERATOR - final boss
from bluebeam.objects import Enemy
import pygame, os, random
from pygame import Vector2 as vec2


class GammaGenerator(Enemy):
    def __init__(self, g, l, pos):
        super().__init__(g, l, pos)
        self.rect = pygame.rect.Rect(0, 0, 832, 768)
        self.phase = 3
        self.hp = 1
        self._mhp = 1

        self.depth = 8
        self.bob = 0

        self.bounds = [vec2(), vec2()]
        self.groundlevel = 0
        self.hands = []
        self.head = None
        self.rocketpoints = [vec2(), vec2(), vec2(), vec2()]
        self.core = None

        self.body = None
        self.rocket = None
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imagedir = os.path.join(os.path.dirname(self.sourceDir), "images/Boss/GammaGenerator")
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss03_body.png')).convert()
        self.load_sprites()

        self.orders = 3
        self.ordertimer = 0
        self.supermove = 0

        self.attackid = 0
        self.attackamt = 0
        self.attacktimer = 0

        self.explo = 0
        self.explo_time = 0

        self.deathstate = 0
        self.risetimer = 3
        self.fadetimer = 0

    def load_sprites(self):
        img = self.load_single((0,0,208,192))
        self.body = pygame.transform.scale(img, (832,768))
        self.spritesheet = pygame.image.load(os.path.join(self.imagedir, 'boss03_rockets.png')).convert()
        img = self.load_single((0,0,42,69))
        self.rocket = pygame.transform.scale(img, (168,276))

    def setup(self, bounds_):
        self.bounds = bounds_
        self.rect.center = self.pos = vec2((self.bounds[0].x + self.bounds[1].x) / 2, self.bounds[1].y + 560)
        tpos = vec2((self.bounds[0].x + self.bounds[1].x) / 2, self.bounds[1].y - 360)
        self.groundlevel = self.bounds[1].y
        for i in range(0,4):
            x = self.pos.x + (2*(i%2)-1)*(self.rect.width/2)
            y = self.pos.y - 64 + (i>=2)*64
            hand = self.l.create("GammaHand",vec2(x,y))
            hand.setup(self, i % 2, i >= 2)
            self.hands.append(hand)
            x = tpos.x + 240 - 480*(i%2) + (40 - 80*(i%2)) * int(i/2)
            y = tpos.y + 160 * int(i/2)
            self.rocketpoints[i] = vec2(x,y)
        self.head = self.l.create("GammaHead", vec2(self.pos.x, self.pos.y - 256))
        self.head.setup(self)
        self.core = self.l.create("GammaCore", self.pos.xy)
        self.core.setup(self)
        self.depth = 9
        self.ordertimer = 3
        self.attackamt = 0
        self.phase_change()

    def update(self):
        if self.explo > 0:
            self.phase_explo()
        if self.deathstate == 0:
            if self.risetimer > 0:
                s = vec2((self.bounds[0].x + self.bounds[1].x) / 2, self.bounds[1].y + 560)
                c = vec2((self.bounds[0].x + self.bounds[1].x) / 2, self.bounds[1].y - 360)
                self.risetimer = max(0,self.risetimer-self.g.delta_time)
                self.pos = self.rect.center = c.lerp(s, self.risetimer/3)
                self.ordertimer = 1.75
            self.bob = (self.bob + self.g.delta_time * 180) % 360
            if self.attacktimer > 0:
                self.attacktimer = max(self.attacktimer - self.g.delta_time, 0)
            elif self.ordertimer > 0 and self.attackamt <= 0:
                self.ordertimer = max(self.ordertimer - self.g.delta_time, 0)
            if self.ordertimer <= 0 and self.attackamt <= 0 and self.attacktimer <= 0:
                if self.supermove == 1:
                    self.superorder()
                else:
                    self.order()
            elif self.attackamt > 0 and self.attacktimer <= 0:
                self.attack()
            if self.hp <= 0:
                self.phase_down()
        elif self.deathstate == 1:
            self.fadetimer = max(self.fadetimer - self.g.delta_time,0)
            if self.fadetimer < 4.5:
                self.pos += vec2(0,200) * self.g.delta_time
                self.rect.center = self.pos
            if self.fadetimer == 0:
                self.finaldeath()

    def order(self):
        if self.orders > 0:
            neworder = random.randint(0, 4)
            self.ordertimer = 1
            if neworder==0:
                # attack 0 - fist swing
                self.attackid = 0
                self.attackamt = 4
                self.attack()
                pass
            elif neworder==1:
                # attack 1 - radial barrage
                self.attackid = 1
                self.attackamt = 1
                self.attack()
                pass
            elif neworder==2:
                self.attackid = 2
                self.attackamt = 1
                self.attack()
                # attack 2 - shockwave bombs
                pass
            elif neworder==3:
                # attack 3 - background missiles
                self.attackid = 3
                self.attackamt = 4 + 2*(3-self.phase)
                self.attack()
                pass
            elif neworder==4:
                # attack 4 - rapid lasers
                self.attackid = 4
                self.attackamt = 2 + (3-self.phase)
                self.attack()
                pass
            else: self.superorder()
        else:
            self.orders = 3 + (3-self.phase)  # 3 orders on phase 1 + an order for each later phase
            self.core.exposed = 6.5
            self.ordertimer = self.core.exposed + 3
        pass

    def attack(self):
        if self.attackid == 0:
            if self.phase==3:
                self.hands[self.attackamt % 2].state(1)
            else:
                self.hands[self.attackamt % 2].state(1)
                self.hands[2 + self.attackamt % 2].state(1)
            self.attacktimer = 1 + (self.attackamt%2 == 1)*1
            self.attackamt -= 1
            pass
        elif self.attackid == 1:
            for i in range(0,2):
                self.hands[i].state(2)
            self.attacktimer = 5.25 + 1.3*(3-self.phase)
            self.attackamt -= 1
            pass
        elif self.attackid == 2:
            self.head.state(1)
            self.attacktimer = 5.25
            self.attackamt -= 1
            pass
        elif self.attackid == 3:
            i = (4 - self.attackamt) % 4
            rock = self.l.create("GammaBGRocket", self.l.player.pos.xy)
            rock.setup(self.rocketpoints[i])
            self.attackamt -= 1
            self.attacktimer = 0.85 - 0.12*(3-self.phase)
            pass
        elif self.attackid == 4:
            i = (2 - self.attackamt) % 2
            self.hands[2+i].state(3)
            self.attackamt -= 1
            self.attacktimer = (self.bounds[1].x - self.bounds[0].x) / (400 + 30*(3-self.phase)) + 0.7
            pass
        else:
            self.superattack()
        if self.attackamt <= 0:
            self.ordertimer = 2.5
            self.orders -= 1

    def superattack(self):
        for i in range(0,4):
            self.hands[i].state(5 + int(i/2))
            self.hands[3].corridorclock = 0.5
            self.attacktimer = 15
            self.attackamt -= 1
            self.ordertimer = 3
            self.supermove = 0

    def superorder(self):
        # superorders - used when phase 2 and 3 start
        self.attackid = 666
        self.attackamt = 1
        self.superattack()
        # corridor attack

    def spawnhealth(self):
        l = (self.bounds[1].x - self.bounds[0].x) / 4
        for i in range(0, 4):
            x = self.bounds[0].x + l*(i+0.5)
            y = self.bounds[1].y - 96
            node = self.l.create("RedPower",vec2(x,y))
            node.depth = 9

    def phase_down(self):
        self.spawnhealth()
        self.phase -= 1

        if self.phase <= 0:
            self.deathstate = 1
            self.fadetimer = 5.5
            for i in range(0,4):
                self.hands[i].death()
            pygame.mixer.music.fadeout(1800)
            self.explo = 80
        else:
            for i in range(0, 3):
                self.hands[i].state(0)
            self.phase_change()
            self.core.exposed = 0
            self.ordertimer = 5
            self.supermove = 1
            self.explo = 16

    def phase_explo(self):
        self.explo_time -= self.g.delta_time
        if self.explo_time <= 0:
            self.explo -= 1
            self.explo_time = 0.1
            boom = self.l.create("Explosion", self.pos.xy + vec2(random.randint(-300,300), random.randint(-300,300)))
            boom.dmg = 0
            boom.radius(160)
            boom.depth = 64
        pass

    def phase_change(self):
        if self.phase == 3:
            self._mhp = 100
        elif self.phase == 2:
            self._mhp = 110
        elif self.phase == 1:
            self._mhp = 120
        self.hp = self._mhp

    def death(self):
        pass

    def finaldeath(self):
        self.l.bossDeathState = 1
        bigboom = self.l.create("Explosion",self.pos.xy)
        bigboom.dmg = 0
        bigboom.radius(2048)
        bigboom.depth = 64
        self.l.uncreate(self.instid)

    def render(self):
        self.l.s.blit(self.body,self.rect.copy().move(-self.l.view))
        self.l.s.blit(self.rocket, self.rect.copy().move(-self.l.view + vec2(60,300)))
        self.l.s.blit(pygame.transform.flip(self.rocket,True,False), self.rect.copy().move(-self.l.view + vec2(612,300)))
        if self.phase > 0:
            # Draw boss health bar at bottom of screen
            sz = self.g.screen_size
            mid = sz[0] / 2 - 490
            top = 80
            hel = float(self._hp / self._mhp) * 968
            pygame.draw.rect(self.l.s, (128, 0, 96, 0), pygame.rect.Rect(mid, top, 980, 60))
            pygame.draw.rect(self.l.s, (255, 0, 192, 100), pygame.rect.Rect(mid + 6, top + 6, hel, 48))