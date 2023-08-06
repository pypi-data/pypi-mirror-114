from bluebeam.objects import EnemyBullet, Explosion
import pygame


class Rocket(EnemyBullet):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.lifespan = 10.
        self.sprite = pygame.sprite.Sprite()

    def rotinplace(self, image, angle):
        core = image.get_rect().center
        ret = pygame.transform.rotate(image, angle)
        rec = ret.get_rect(center=ret.get_rect(center=(core[0], core[1])).center)
        return ret, rec

    def hit(self):
        boom = self.l.create("Explosion", self.pos.xy)
        boom.radius(192)
        self.l.uncreate(self.instid)
