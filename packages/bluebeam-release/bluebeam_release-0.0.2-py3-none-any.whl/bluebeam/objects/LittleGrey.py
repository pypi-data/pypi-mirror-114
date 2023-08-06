from bluebeam.objects import Enemy
import pygame
import os

class LittleGrey(Enemy):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.rect = pygame.rect.Rect(0, 0, 78, 78)
        self.rect.center = self.pos
        self._mhp = 30
        self.hp = self._mhp
        self.idied = 0

        self.speed = pygame.math.Vector2(150, 150)
        self.accel = 0.02

        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images/Enemy/LittleGrey")
        
        self.images_left = []
        self.images_right = []
        for i in range(3):
            img_right = pygame.image.load(os.path.join(self.imageDir, f'LittleGrey{i}.png')).convert_alpha()
            img_right = pygame.transform.scale(img_right, (78,78))
            img_left  = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.images_left[1]

        self.gravity = 0
        self.collide_terrain = False
        self.jump_cd = 0

        self.current_position = 1
        self.animation_counter = 1
        # self._shotcd = 0



    def update(self):
        super().update()
        if (self._active):
            self.inproximity()
            self.update_ai_inputs()

    def inproximity(self):
        diff = self.pos - self.l.player.pos
        squareddist = diff.x ** 2 + diff.y ** 2
        if squareddist < 80000 and (self._hp > 0):
            self._telepath = True
        else:
            self._telepath = False
        if self._hp <= 0:
            self.l.player.around_lg = False

    def update_ai_inputs(self):
        if(self.l.player.around_lg):
            self.image = self.images_left[0]
        else:
            self.xmove()
            self.ymove()

    def xmove(self):
        # Should I go left or right?
        left = False
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
           left = True
        else:
            left = False
        self.update_animation(left)

    def ymove(self):
        # Should I go up or down?
        if (self.l.player.y < self.y - 80):
            targ_yvel = -self.speed.y
            if (self.vel.y > targ_yvel):
                self.vel.y -= self.speed.y * self.accel

        if (self.l.player.y > self.y + 80):
            targ_yvel = self.speed.y
            if (self.vel.y < targ_yvel):
                self.vel.y += self.speed.y * self.accel

    def update_animation(self, left):
        #animation_counter = 0
        #if left:
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.animation_counter = 0
            self.current_position += 1
            if self.current_position >= 3:
                self.current_position = 1
        if self._telepath:
            self.image = self.images_left[0]
        if left:
            self.image = self.images_left[self.current_position]
            #print(self.current_position)
        else:
            self.image = self.images_right[self.current_position]

    def collision_bullet(self):
        col = pygame.sprite.spritecollide(self, self.l.bulletsP, False)
        if len(col) > 0:
            for bul in col:
                self.hp -= bul.dmg
                self.vel += bul.vel / 2
                bul.hit()


    def render(self):
        # pygame.draw.rect(self.l.s,
        #                   (128 + 127 * (1 - self.idied), 128, 128 + (127 * self.idied), 100),
        #                   self.rect.copy().move(-self.l.view))
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

