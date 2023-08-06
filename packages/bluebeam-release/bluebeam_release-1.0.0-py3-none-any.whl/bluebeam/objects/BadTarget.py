from bluebeam.objects import Target
import pygame


class BadTarget(Target):
    def __init__(self, g_, l_, pos_=None):
        super().__init__(g_, l_, pos_)
        self.shotcd = 1.67

    def update(self):
        super().update()
        if (self.shotcd <= 0):
            inst = self.l.create("EnemyBullet", self.pos.xy)
            inst.speed = pygame.math.Vector2(-300, 0)
            self.shotcd = 1.67
        else:
            self.shotcd -= self.g.delta_time
