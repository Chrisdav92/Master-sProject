#!/usr/bin/python
# -*- coding: utf-8 -*-
#This is the overall program for my Master's project robot game
#It will be a labyrinth type game with a game screen that has time,score, button (but also take in keyboard)
#As well as have a function to allow camera feed
#V1 --- (10/12/16)- Inital imports done, made skel
#       (10/17/16)- Was sick so not too much done
#       (10/21/16)-Worked on getting window up with map layout. Used some open source code for map creation and editing
#                 -Added a player sprite for the game as well as worked on map
#                 -encountering issue being able to use pi2go library will be needing to work on that!! Need to comment out calls
#                 -able to get sprite to respond to arrow keys
#------(10/23/16) -noticed that ConfigParser is for pyth v2 so it may be a issue later
#                 -added pi2go function call to moving robot in the directional call
#------(11/1/16) - editted some functions, may need to re do movement key as pi2go lib still not being reached
#------(11/3/16) - Re-did entire program as I was running into too many issues dealign with sprite animations and updating. reverting to simplier layout, I
# will try to model it off of paceman as it is more tiled based and now dealing with a static spirte may help. Also I figure to correctly rotate the robot
# I must use the sensors to move the robot then figure when to stop. This allows for better responsiveness to the spirte as well
#------(11/5/16) - exported player and tile classes to their own file to improve on easibility, as well as create an abstract entity class file
#------(11/10/16) - Got the pi2go library to work! Now figuring out to do movement
#------(11/12/16) -- Introduced maze generation for the maze, based on size of screen. Also will check to see if it blocks anyother ones.
#------(11/14/16) -- Got the maze to work, added player position and goal.
#------(11/15/16) -- Included motor movement but having issue with quitting game correctly after goal has been reached.

#These are the imports for the library
import os.path,sys
#import pi2go
import pygame

sys.setrecursionlimit(10000) 
from pygame.locals import *
pygame.init()
fpsClock = pygame.time.Clock()

# =================VARIABLES================================================
# Constants
mazeWidth = 21
mazeHeight = 20
u = pixelUnit = 30
windowWidth = mazeWidth * pixelUnit
windowHeight = mazeHeight * pixelUnit
walk_cooldown = 0
WALK_DELAY = 1
# Maze is a 2D array of integers
maze = {}

# Maze variables - used for generation
primes = [37,73,43,47,2,83,7,89,41,17,67,71,101,97,3,19,61,5,11,23,53,59,29,13,79,31,103]
numbers = [3755,8187,7883,9111,2503,5838,9544,1001,2246,1840,1160,1069,9369,9540,3213]
level = 1
seed = 0
seedPlus = 0

# Corner variables - gameplay
checks = [0,0,0]
checksc = [(1, mazeHeight-2),(mazeWidth-2, 1),(mazeWidth-2, mazeHeight-2)]

# Player variables
playerx, playery = 1,1
minutes = 0
seconds = 0
frames = 0
fps = 14
playerName = 'P1'

windowSurfaceObj = pygame.display.set_mode((windowWidth,windowHeight))
updateRect = pygame.Rect(0,0,u,u)

greyColor= pygame.Color(160,160,160)
blackColor = pygame.Color(0,0,0)
redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0,240,0)

def minit():
        global minutes, seconds
        minutes = seconds  = 0
        global frames
        frames = 0

# =================Drawing the maze=======================================

# Draw a square with color c at (x,y) in our grid of squares with u width
def drawSquare(x,y,c):
        global u
        pygame.draw.rect(windowSurfaceObj, c, (x*u, y*u, u, u))

# Draw maze walls without player or objectives
def drawMaze():
        for x in range(0, mazeWidth):
                for y in range(0, mazeHeight):
                        if maze[x,y] == 1:
                                drawSquare(x,y,blackColor)

def updateText():
        global minutes, seconds, frames
        timemsg = ' - Time:'+str(minutes)+'m'+str(seconds)+'s'
        if( frames < 10 ):
                timemsg = timemsg+'0'
        msg = 'PyMaze - '+playerName
        pygame.display.set_caption(msg)

# Draw maze, objectives and player. Update score display
def drawScene():
        global minutes, seconds, frames
        frames += 1
        if(frames >= fps):
                seconds += 1
                frames = 0
        if(seconds >= 60):
                minutes += 1
                seconds = 0
        updateText()
        windowSurfaceObj.fill(greyColor)
        drawSquare(playerx,playery,greenColor)
        drawMaze()
        for i in range(0,1):
                if checks[i] == 0:
                        drawSquare(*checksc[i], c=redColor)
        pygame.display.update()
                        
def isOutside(x,y):
        if x<0 or y<0 or x>=mazeWidth or y>=mazeHeight:
                return True
        return False
   
def isBorder(x,y):
        if x == 0 and (y>=0 and y < mazeHeight):
                return True
        if x == (mazeWidth-1) and (y>=0 and y < mazeHeight):
                return True
        if y == 0 and (x>=0 and x < mazeWidth):
                return True
        if y == mazeHeight-1 and (x>=0 and x < mazeWidth):
                return True
        return False

def isBlocked(x,y):
        if( x<0 or y<0 or x>=mazeWidth or y>= mazeHeight ):
                return True
        if(maze[x,y] == 1):
                return True
        return False

def recursiveSearch(x,y):
        if isBlocked(x,y):
                return
        if maze[x,y] == 10:
                return
        if not isBlocked(x,y):
                maze[x,y] = 10
                recursiveSearch(x-1,y)
                recursiveSearch(x+1,y)
                recursiveSearch(x,y-1)
                recursiveSearch(x,y+1)


def recursiveSearchStart(x,y):
        recursiveSearch(x,y)
        rval = True                                     # rval == true means the search visited everything
        for x in range(1, mazeWidth-1):                 # ignore first and last row and column
                for y in range(1, mazeHeight-1):        # they are always walls
                        if( maze[x,y] == 0):
                                rval = False            # We found something the search didn't visit
                        if( maze[x,y] == 10 ):
                                maze[x,y] = 0
        return rval


def tryPlace(x,y):
        if(isBlocked(x,y)):
                return False
        maze[x,y] = 1
        if recursiveSearchStart(1,1):
                return True
        maze[x,y] = 0
        return False

def cellGen(x,y):
        # Don't create 2x2 squares:
        if isBlocked(x-1,y) and isBlocked(x-1,y-1) and isBlocked(x,y-1):
                return
        if isBlocked(x+1,y) and isBlocked(x+1,y-1) and isBlocked(x,y-1):
                return
        if isBlocked(x-1,y) and isBlocked(x-1,y+1) and isBlocked(x,y+1):
                return
        if isBlocked(x+1,y) and isBlocked(x+1,y+1) and isBlocked(x,y+1):
                return
        # Don't cut off parts of the maze - tryPlace ensures this
        drawCheck = tryPlace(x,y)
        if drawCheck:
                drawSquare(x,y,blackColor)
                pygame.display.update()
        return

# resets player position and the level
def resetPlayer():
        global checks, playerx, playery, secondsLevel
        playerx = playery = 1
        secondsLevel = 0
        checks = [0,0,0]        
        global kUp, kLeft, kDown, kRight
        global kW, kA, kS, kD
        kUp = kLeft = kDown = kRight = False

# Generate a maze based on seed and level
def generate():
        resetPlayer()
        for x in range(0, mazeWidth):
                for y in range(0, mazeHeight):
                        maze[x,y] = 0
                        if isBorder(x,y):
                                maze[x,y] = 1
        drawScene()
        i = x = y = 0
        global seed, level, seedPlus
        seed = 111 + 3*(level-1) + level/3 + level/5 + seedPlus
        n = seed%15
        rand = {}
        for i in range(0,256):
                if(n>14):
                        n=0
                rand[i] = seed * numbers[n] + i
                for p in range(0, 27):
                        rand[i] += i/primes[p]
        
        i = 0
        while i<255:
                num = rand[i]
                x = num%mazeWidth
                i += 1
                num = rand[i]
                y = num%mazeHeight
                i += 1
                cellGen(x,y);
        for x in range(1, mazeWidth-1):
                for y in range(1, mazeHeight-1):
                        cellGen(x,y)
                        x2 = mazeWidth-1-x
                        y2 = mazeHeight-1-y
                        cellGen(x2, y2)
                        cellGen(x2/2, y2/2)
                        space = 2+level%4
                        if(x > 3 and (x+(4*y/3))%space == 0):
                                for y3 in range(y, y+mazeHeight/3):
                                        cellGen(x, y3)

# =================Player Methods======================

# Moves player by (x*unit, y*unit)
# All game logic is done through this function
# since nothing happens when standing still
def playerMove(x,y):
        global playerx, playery, score
        global level, secondsLevel, minutes, seconds
        global checks, checksc
        playerx += x
        playery += y
        if(isBlocked(playerx,playery)):
                playerx -= x
                playery -= y
                return
        c = (playerx,playery)
        for i in range(0,1):
                if(checksc[i] == c and checks[i] == 0):
                        checks[i] = 1
                        if(checks[0] == 1):
                            pygame.quit()       
                        return
                        
# Move player based on keyboard input
def movement():
        if kUp:
                playerMove(0,-1)
        if kLeft:
                playerMove(-1,0)
        if kDown:
                playerMove(0,1)
        if kRight:
                playerMove(1,0)

# =================Exiting Game=========================

def exitPyMaze():
        pygame.quit()
        sys.exit()
        
        
def pad(s, n):
        while(len(s) < n):
                s = s + ' '
        return s

# =================Player name method====================

def setName():
        global playerName
        doneTyping = False
        tempName = ''
        while(doneTyping == False):
                events = 0
                for event in pygame.event.get():
                        events += 1
                        if event.type == QUIT:
                                exitPyMaze()
                        elif event.type == KEYDOWN:
                                if event.key == K_RETURN:
                                        doneTyping = True
                                elif event.key == K_ESCAPE:
                                        pygame.event.post(pygame.event.Event(QUIT))
                                else:
                                        tempName = tempName + event.unicode
                
                msg = 'Enter name: ' + tempName
                pygame.display.set_caption(msg)
                fpsClock.tick(fps)
        
        playerName = tempName

# =================Main==================================

minit()
generate()
pi2go.init()
if(level == 1):
        setName()
while True:
        #Handle events:
        delta = fpsClock.tick() / 1000.0
        walk_cooldown -= delta
        events = 0
        for event in pygame.event.get():
                events += 1
                if event.type == QUIT:
                        exitPyMaze()
                
                elif event.type == KEYDOWN:
                        if event.key == K_UP:
                                kUp = True
                                movement()
                                walk_cooldown = WALK_DELAY
                                pi2go.forward(15)
                                pi2go.stop
                        if event.key == K_LEFT:
                                kLeft = True
                                movement()
                                walk_cooldown = WALK_DELAY
                                pi2go.spinLeft(15)
                                pi2go.stop
                        if event.key == K_DOWN:
                                kDown = True
                                movement()
                                walk_cooldown = WALK_DELAY
                                pi2go.reverse(15)
                                pi2go.stop
                        if event.key == K_RIGHT:
                                kRight = True
                                movement()
                                walk_cooldown = WALK_DELAY
                                pi2go.spinRight(15)
                                pi2go.stop
                        if event.key == K_ESCAPE:
                                pygame.event.post(pygame.event.Event(QUIT))
                elif event.type == KEYUP:
                        if event.key == K_UP:
                                kUp = False
                        if event.key == K_LEFT:
                                kLeft = False
                        if event.key == K_DOWN:
                                kDown = False
                        if event.key == K_RIGHT:
                                kRight = False
        #Drawing scene and updating window:
        if(events == 0):
                movement()              
        drawScene()
        fpsClock.tick(fps)
