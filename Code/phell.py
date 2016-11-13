#------(11/5/16) - created file

import pygame
from pygame.locals import *
from entity import AbstractEntity

class Phell(object):
    def __init__(self, dim, pos=[0,0]):
        AbstractEntity.__init__(self, dim, pos)
        self.COLOR = (255,255,0)
        self.direction = 'LEFT'

    def move(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            self.pos[1] -= 3
            self.direction = 'UP'
        elif key_pressed[K_DOWN]:
            self.pos[1] += 3
            self.direction = 'DOWN'
        elif key_pressed[K_LEFT]:
            self.pos[0] -= 3
            self.direction = 'LEFT'
        elif key_pressed[K_RIGHT]:
            self.pos[0] += 3
            self.direction = 'RIGHT'
    #collision detection        
    def collide(self, other):
        xcollide = axis_overlap(self.pos[0], self.dim[0],
                                other.pos[0], other.dim[1])
        ycollide = axis_overlap(self.pos[1], self.dim[1],
                                other.pos[1], other.dim[1])
        if xcollide & ycollide:
            if self.direction is 'UP':
                self.pos[1] = other.pos[1]+other.dim[1]
            elif self.direction is 'DOWN':
                self.pos[1] = other.pos[1]-self.dim[1]
            elif self.direction is 'LEFT':
                self.pos[0] = other.pos[0]+other.dim[0]
            elif self.direction is 'RIGHT':
                self.pos[0] = other.pos[0]-self.dim[0]

    def draw(self, screen):
        values = list(self.pos)+list(self.dim)
        pygame.draw.rect(screen, self.COLOR, values)

def axis_overlap(p1, length1, p2, length2):
        collided = False
        if p1 < p2:
            if p2+length2-p1 < length1+length2:
                collided = True
            elif p1 > p2:
            if p1+length1-p2 < length1+length2:
                collided = True
            elif p1 == p2:
                collided = True
            return collided