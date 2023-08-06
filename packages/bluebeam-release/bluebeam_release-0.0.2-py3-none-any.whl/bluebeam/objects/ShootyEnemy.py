from bluebeam.objects import Enemy
import pygame, math
import os

class ShootyEnemy(Enemy):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.rect = pygame.rect.Rect(0, 0, 108, 124)
        self.rect.center = self.pos
        self._mhp = 50
        self.hp = self._mhp
        self.idied = 0

        self.speed = pygame.math.Vector2(400, 800)

        self.shot_speed    = 400
        self.shot_cd       = 2
        self.panic_shot_cd = 0.5

        self.accel = 0.20
        self.gravity = 50
        self._shotcd = 0

        self.panic = False

        # for image/animation
        self.current_position = 0
        self.animation_counter = 0
        self.images_right = []
        self.images_left = []

        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images/Enemy")

        for image in range(1, 9):
            img_left = pygame.image.load(os.path.join(self.imageDir,f'shooter{image}.png'))
            img_left = pygame.transform.scale(img_left, (108, 124))
            img_right = pygame.transform.flip(img_left, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.images_left[self.current_position]

    def update_ai_inputs(self):
        self._rot = pygame.math.Vector2().angle_to(self.l.player.pos - self.pos)
        self.xmove()
        self.check_fire()

    def check_fire(self):
        self._shotcd = max(0, self._shotcd - self.g.delta_time)
        if (self._shotcd <= 0):
            self.fire()

    def xmove(self):
        if(self.l.player.x < self.x): 
            left = True
        else:
            left = False

        xspeed = self.speed.x * self.accel
        ydist = abs(self.l.player.y - self.y)
        xdist = abs(self.l.player.x - self.x)

        if((xdist > 700 or ydist > 700) and self.panic):
            self.panic = False
        elif((xdist <= 250 and ydist < 500) or self.panic):
            if(not left):  self.go_left(xspeed)
            else:     self.go_right(xspeed)

            self.try_jump()
            if(self.panic == False):
                self.panic = True
                self._shotcd = 0.3
        else:
            self.slow_down(xspeed)

        self.update_animation(left)

    def update_animation(self, left):
        # animation_counter = 0
        # if left:
        self.animation_counter += 1
        if self.animation_counter >= 5:
            self.animation_counter = 0
            self.current_position += 1
            if self.current_position >= 4:
                self.current_position = 0

        if left:
            self.image = self.images_left[self.current_position]
            # print(self.current_position)
        else:
            self.image = self.images_right[self.current_position]

    def go_left(self, xspeed):
        targ_xvel = -self.speed.x
        if (self.vel.x > targ_xvel):
            self.vel.x -= xspeed

    def go_right(self, xspeed):
        targ_xvel = self.speed.x
        if (self.vel.x < targ_xvel):
            self.vel.x += xspeed

    def slow_down(self, xspeed):
        if (self.vel.x < 0):
            self.vel.x += xspeed
        elif (self.vel.x > 0):
            self.vel.x -= xspeed

        if (abs(self.vel.x) < xspeed):
            self.vel.x = 0

    def try_jump(self):
        if (self.pstate == 0):
            self.jumping = True
            self._vel.y = -self.speed.y

    # This was Tyler's shooting mechanism for the boss.
    def fire(self):
        #bul = EnemyBullet("EnemyBullet", self.pos.xy)

        inst = self.l.create("EnemyBullet", self.pos.xy)

        inst.load_shooty_image()
        inst.collide_terrain = False
        inst.speed = pygame.math.Vector2(self.shot_speed * math.cos(math.radians(self._rot)),
                                         self.shot_speed * math.sin(math.radians(self._rot)))
        inst.shooty_enemy = True
        if self.l.player.x <= self.pos.x:
            inst.pos.x -= 100
            inst.pos.y -= 40
        else:
            inst.pos.x += 60
            inst.pos.y -= 40

        if (self.panic):
            self._shotcd = self.panic_shot_cd
        else:
            self._shotcd = self.shot_cd

    def update(self):
        super().update()
        if(self._active):
            self.update_ai_inputs()

    def render(self):
        self.l.s.blit(self.image, self.rect.copy().move(-self.l.view))
        pygame.draw.rect(self.l.s,
                         (255, 0, 0, 100),
                         pygame.rect.Rect(self.rect.topleft[0], self.rect.topleft[1] - 24, 100, 16).move(-self.l.view))
        pygame.draw.rect(self.l.s,
                         (0, 255, 0, 100),
                         pygame.rect.Rect(self.rect.topleft[0],
                                          self.rect.topleft[1] - 24,
                                          100 * (self.hp / self._mhp),
                                          16).move(-self.l.view))
