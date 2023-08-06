import pygame
from bluebeam.objects import Bullet
import os


class PlayerBullet(Bullet):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        # self.owner = 0
        self.speed = pygame.math.Vector2(1000., 0.)
        self.lifespan = 5.
        self.dmg = 10
        self._objid = 4
        self.charged = False
        self.depth = 16
        self.rapid_fire = False
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images")
        self.image = pygame.image.load(os.path.join(self.imageDir, 'ball.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (36, 36))
        self.large_image = pygame.transform.scale(self.image, (64, 64))

        self.collide_terrain = False


    def update(self):
        super().update()
        if(self.charged):
            self.collide_enemy_bullets()

    def collide_enemy_bullets(self):
        col = pygame.sprite.spritecollide(self, self.l.bulletsE, False)
        for bul in col:
            bul.hit()


    def render(self):
        spos = self._pos - self.l.view
        #pygame.draw.rect(self.l.s, (255, 255, 64, 100), self.rect.copy().move(-self.l.view))
        if not self.charged:
            self.l.s.blit(self.image, self.rect.copy().move(-self.l.view))
        else:
            self.l.s.blit(self.large_image, self.rect.copy().move(-self.l.view))

