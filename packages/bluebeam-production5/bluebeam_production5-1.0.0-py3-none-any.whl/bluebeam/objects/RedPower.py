import pygame
import os

class RedPower(pygame.sprite.Sprite):
    def __init__(self, global_vars, level, pup_position, pup_width=32, pup_height=32):
        super().__init__()
        self.depth = 0
        self.instid = 4
        self.objid = 5
        self._global_vars = global_vars
        self._level = level
        self._pup_position = pup_position
        self.index = 0
        self.animation_counter = 0
        self.images = []
        self.sourceDir = os.path.dirname(os.path.abspath(__file__))
        self.imageDir = os.path.join(os.path.dirname(self.sourceDir), "images/Red")
        for frame in range(1,7):
            img = pygame.image.load(os.path.join(self.imageDir, f'frame {frame}.png')).convert_alpha()
            img = pygame.transform.scale(img, (48, 48))
            self.images.append(img)

        self.image = self.images[self.index]
        #self.rect = self.image.get_rect()
        self.rect = pygame.rect.Rect(pup_position[0], pup_position[1], pup_width, pup_height)
        #self.rect.center = self._pos
        self.player_acquired = False
        self._pup_width = pup_width


    def acquired(self):
        self.player_acquired = True
        return 3

    def update(self):
        self.animation_counter += 1
        if not self.player_acquired and self.animation_counter >= 10:
            self.image = self.images[self.index]
            self.index += 1
            self.animation_counter = 0
            if self.index >= 5:
                self.index = 0

    def render(self):
        spos = self._pup_position - self._level.view
        if not self.player_acquired:
            #pygame.draw.rect(self._level.s, (255, 215, 0, 100), self.rect.copy().move(-self._level.view))
            self._level.s.blit(self.image, self.rect.copy().move(-self._level.view))
