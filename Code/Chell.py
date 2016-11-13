#!/usr/bin/python
# -*- coding: utf-8 -*-
#This is the overall program for my Master's project robot game
#It will be a labyrinth type game with a game screen that has time,score, button (but also take in keyboard)
#As well as have a function to allow camera feed
#V1 --- (10/12/16)- Inital imports done, made skel
#	(10/17/16)- Was sick so not too much done
#	(10/21/16)-Worked on getting window up with map layout. Used some open source code for map creation and editing
#		  -Added a player sprite for the game as well as worked on map
#	          -encountering issue being able to use pi2go library will be needing to work on that!! Need to comment out calls
#                 -able to get sprite to respond to arrow keys
#------(10/23/16) -noticed that ConfigParser is for pyth v2 so it may be a issue later
#		  -added pi2go function call to moving robot in the directional call
#------(11/1/16) - editted some functions, may need to re do movement key as pi2go lib still not being reached
#------(11/3/16) - Re-did entire program as I was running into too many issues dealign with sprite animations and updating. reverting to simplier layout, I
# will try to model it off of paceman as it is more tiled based and now dealing with a static spirte may help. Also I figure to correctly rotate the robot
# I must use the sensors to move the robot then figure when to stop. This allows for better responsiveness to the spirte as well
#These are the imports for the pygame library
#------(11/5/16) - exported player and tile classes to their own file to improve on easibility, as well as create an abstract entity class file
#------(11/10/16) - Got the pi2go library to work! Now figuring out to do movement
import os,sys
#import pi2go
import pygame
from pygame.locals import *
from phell import Phell
from tile import Tiles
from entity import AbstractEntity

#initalize
pygame.init()
width, height = (50,50)
SCREEN_SIZE = (600, 400)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
x,y = (500,200)
x2,y2,width2,height2 = (150,150,150,100)
background = pygame.surface.Surface(SCREEN_SIZE).convert()
background.fill((0,0,0))
direction = 'LEFT'

#creating the objects
chell = Phell((50,50), [500,200])
tile = Tiles((150,150), [150,100])

while True:
    key_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    chell.move()
    #here is where the collide method interact with tile and the goal
    chell.collide(tile)
    if key_pressed[K_UP]:
        y -= 3
        direction = 'UP'
    elif key_pressed[K_DOWN]:
        y += 3
        direction = 'DOWN'
    elif key_pressed[K_LEFT]:
        x -= 3
        direction = 'LEFT'
    elif key_pressed[K_RIGHT]:
        x += 3
        direction = 'RIGHT'

    xycollide = False
    xcollide = axis_overlap(x,width,x2,width2)
    ycollide = axis_overlap(y,height,y2,height2)
    xycollide = xcollide & ycollide
    if xycollide:
        if direction is 'UP':
            y = y2+height2
        elif direction is 'DOWN':
            y = y2-height
        elif direction is 'LEFT':
            x = x2+width2
        elif direction is 'RIGHT':
            x = x2-width

    screen.blit(background, (0,0))
    tile.draw(screen)
    chell.draw(screen)
    pygame.draw.rect(screen, (255,0,0),[x2,y2,width2,height2])
    pygame.draw.rect(screen, (255,255,0),[x,y,width,height])
    pygame.display.update()
