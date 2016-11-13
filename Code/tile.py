#------(11/5/16) - created file
import pygame
from entity import AbstractEntity

class Tile(AbstractEntity):
    def __init__(self, dim, pos=[0,0]):
        AbstractEntity.__init__(self, dim, pos)
        self.COLOR = (255,0,0)

    def draw(self, screen):
        values = list(self.pos)+list(self.dim)
        pygame.draw.rect(screen, self.COLOR, values)
