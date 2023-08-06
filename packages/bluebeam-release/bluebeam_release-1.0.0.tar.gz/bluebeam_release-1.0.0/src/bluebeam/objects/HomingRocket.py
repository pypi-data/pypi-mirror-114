from bluebeam.objects import Rocket, Explosion
import pygame, os, math


class HomingRocket(Rocket):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.rect.width = self.rect.height = 48
        self.hp = 30
        self.lifespan = 10.
        self.lockon = 0.3
        self._dir = 270
        self._dirmax = 90
        self.maxvel = 275
        self.traveldir = pygame.math.Vector2(0,-1)

        self.sprites = []
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images/missile")
        self.load_sprites()

    def load_sprites(self):
        imgh = pygame.image.load(os.path.join(self.imageDir, f'missile1.png'))
        imgh = pygame.transform.scale(imgh, (48, 48))
        imgd = pygame.image.load(os.path.join(self.imageDir, f'missile9.png'))
        imgd = pygame.transform.scale(imgd, (80, 80))
        imgv = pygame.image.load(os.path.join(self.imageDir, f'missile18.png'))
        imgv = pygame.transform.scale(imgv, (48, 48))
        self.sprites.append(imgh)
        self.sprites.append(pygame.transform.flip(imgd,False,True))
        self.sprites.append(pygame.transform.flip(imgv,False,True))
        self.sprites.append(pygame.transform.flip(imgd,True,True))
        self.sprites.append(pygame.transform.flip(imgh,True,False))
        self.sprites.append(pygame.transform.flip(imgd,True,False))
        self.sprites.append(imgv)
        self.sprites.append(imgd)

    def update(self):
        self.lockon = max(0, self.lockon - self.g.delta_time)
        if self.lockon <= 0:
            self.aim()
        self.vel = self.traveldir * self.maxvel
        super().update()
        self.collision_bullet()
        pass

    def aim(self):
        ang = pygame.math.Vector2().angle_to(self.l.player.pos - self.pos)
        self._dir = ang
        self.traveldir = pygame.math.Vector2(math.cos(math.radians(self._dir)), math.sin(math.radians(self._dir)))

    def hit(self):
        boom = self.l.create("Explosion", self.pos.xy)
        boom.radius(192)
        self.l.uncreate(self.instid)

    def collision_bullet(self):
        col = pygame.sprite.spritecollide(self, self.l.bulletsP, False)
        if len(col) > 0:
            for bul in col:
                self.lifespan -= bul.dmg/2
                bul.hit()

    def render(self):
        num = int(((self._dir + 720) % 360) / 45) % 8
        self.l.s.blit(self.sprites[num], self.rect.copy().move(-self.l.view))