from bluebeam.objects import EnemyBullet
import pygame
import os


class Explosion(EnemyBullet):

    def __init__(self, g_, l_, pos_):
        super().__init__(g_, l_, pos_)
        self.lifespan = 15
        self.dmg = 20

        self.images = []
        self.index = 0
        self.animation_counter = 0
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images/Explosion")
        for frame in range(1, 5):
            img = pygame.image.load(os.path.join(self.imageDir, f'explosion{frame}.png')).convert_alpha()
            img = pygame.transform.scale(img, (210, 210))
            self.images.append(img)

        self.image = self.images[self.index]

        pass

    def radius(self, radi):
        self.rect = pygame.rect.Rect(self.pos.x - radi / 2, self.pos.y - radi / 2, radi, radi)
        self.rect.center = self.pos

    def hit(self):
        pass

    def animate(self):
        self.animation_counter += 1
        self.lifespan -= 1
        if self.animation_counter >= 3:
            self.image = self.images[self.index]
            self.index += 1
            self.animation_counter = 0
            if self.index >= 4:
                self.lifespan - 0
                self.l.uncreate(self.instid)

    def update(self):
        self.animate()
        '''
        if self.lifespan <= 0:
            self.l.uncreate(self.instid)
        else:
            self.lifespan -= 1
        '''

    def render(self):
        #pygame.draw.circle(self.l.s, (255, 255, 128, 100), self.rect.center - self.l.view, self.rect.width / 1.71)
        self.l.s.blit(self.image, self.rect.copy().move(-self.l.view))
