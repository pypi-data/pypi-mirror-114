import pygame


class GameObject(pygame.sprite.Sprite):
    g = None

    # Initialize object, call a creation function

    def __init__(self, g_, l_, pos_=None):
        super().__init__()
        self.g = g_  # ref to global vars
        self.l = l_  # ref to level
        self._objid = 0  # CONST!
        self._instid = self.g.getid()  # Gets instance id from global vars
        self.spritesheet = None
        self.depth = 0
        if isinstance(pos_, pygame.math.Vector2):
            self._pos = pos_
        else:
            self._pos = pygame.math.Vector2(0, 0)
        # self.image = pygame.image.load("MaybeWeWontNeedToUseThisButICommentedItHereAny.way")
        # self.rect = self.image.get_rect()
        self.rect = pygame.rect.Rect(0, 0, 0,
                                     0)  # Changing values 0 and 1 here are irrelevant. 2 is width. 3 is height.
        self.rect.center = self.pos
        self.depth = 0
        self._flag = (1, 1, 0)
        self.create()

    @property
    def objid(self):
        return self._objid

    @property
    def instid(self):
        return self._instid

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, n_pos):
        self._pos = n_pos

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, n_flag):
        self._flag = n_flag

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, n_mask):
        self._mask = n_mask

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def load_single(self, vec4):
        rect = pygame.Rect(vec4[0], vec4[1], vec4[2], vec4[3])
        img = pygame.Surface(rect.size).convert()
        img.blit(self.spritesheet, (0, 0), rect)
        img.set_colorkey(img.get_at((0, 0)), pygame.RLEACCEL)
        return img

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    # generic render function
    def render(self):
        # nothing
        pass
