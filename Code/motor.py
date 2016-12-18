# Pi2Go basic motor sketch 

import pi2go, time

# Reading a button press from your keyboard, don't worry about this too much!
import sys
import tty
import termios

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

def readchar():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
        finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ch == '0x03':
                raise KeyboardInterrupt
        return ch

def readkey(getchar_fn=None):
        getchar = getchar_fn or readchar
        c1 = getchar()
        if ord(c1) != 0x1b:
                return c1
        c2 = getchar()
        if ord(c2) != 0x5b:
                return c1
        c3 = getchar()
        return ord(c3) - 65  # 0=Up, 1=Down, 2=Right, 3=Left arrows

speed = 40
leftM = 33
rightM = 25

#FORWARD IS FACING EAST
def east():
 eastBool = True;
 while(eastBool):
   keyp = readkey()
   if keyp == 'd' or keyp == RIGHT and eastBool:
                        pi2go.go(leftM,speed)
                        print 'East Forward', speed
                        time.sleep(1.5)
                        pi2go.stop()

   if keyp == 's' or keyp == DOWN and eastBool:
                        pi2go.spinRight(speed)
                        print 'TURING south RIGHT', speed
                        time.sleep(1.8)
                        pi2go.forward(speed)
                        print 'Forward to SOUTH', speed
                        time.sleep(1.5)
                        pi2go.stop()
                        eastBool = False;
                        south()
                        
   if keyp == 'w' or keyp == UP and eastBool:
                        pi2go.spinLeft(speed)
                        print 'TURING north LEFT', speed
                        time.sleep(1.5)
                        pi2go.forward(speed)
                        print 'Forward to NORTH', speed
                        time.sleep(1.5)
                        pi2go.stop()
                        eastBool = False;
                        north()         

   if keyp == 'a' or keyp == LEFT and eastBool:
                        pi2go.reverse(speed)
                        print 'Backward west', speed
                        time.sleep(1.5)
                        pi2go.stop()
   if keyp == '/':
                        print 'Exiting.....'
                        exit()

#FORWARD IS FACING WEST
def west():
  westBool = True;
  while(westBool):
   keyp = readkey()
   if keyp == 'd' or keyp == RIGHT and westBool:
                        pi2go.reverse(speed)
                        print 'Backward east', speed
                        time.sleep(1.5)
                        pi2go.stop()

   if keyp == 's' or keyp == DOWN and westBool:
                        pi2go.spinLeft(speed)
                        print 'TURING south LEFT', speed
                        time.sleep(1.5)
                        pi2go.forward(speed)
                        print 'Forward to SOUTH', speed
                        time.sleep(1.5)
                        pi2go.stop()
                        westBool = False;
                        south()
                        
   if keyp == 'w' or keyp == UP and westBool:
                        pi2go.spinRight(speed)
                        print 'TURING north RIGHT', speed
                        time.sleep(1.5)
                        pi2go.forward(speed)
                        print 'Forward to NORTH', speed
                        time.sleep(1.5)
                        pi2go.stop()
                        westBool = False;
                        north()                 

   if keyp == 'a' or keyp == LEFT and westBool:
                        pi2go.forward(speed)
                        print 'West Forward', speed
                        time.sleep(1.5)
                        pi2go.stop()
   if keyp == '/':
                        print 'Exiting.....'
                        exit()



#FORWARD IS FACING SOUTH
def south():
  southBool = True;
  while(southBool):
   keyp = readkey()
   if keyp == 'd' or keyp == RIGHT and southBool:
                        pi2go.spinLeft(speed)
                        print 'TURING East LEFT', speed
                        time.sleep(1.5)
                        pi2go.forward(speed)
                        print 'Forward to EAST', speed
                        time.sleep(1.5)
                        pi2go.stop()
                        southBool= False;
                        east()
   if keyp == 's' or keyp == DOWN and southBool:
                        pi2go.forward(speed)
                        print 'South Forward', speed
                        time.sleep(1.5)
                        pi2go.stop()
                        
   if keyp == 'w' or keyp == UP and southBool:
                        pi2go.reverse(speed)
                        print 'Backward north', speed
                        time.sleep(1.5)
                        pi2go.stop()

   if keyp == 'a' or keyp == LEFT and southBool:
                        pi2go.spinRight(speed)
                        print 'TURING west RIGHT', speed
                        time.sleep(1.5)
                        pi2go.forward(speed)
                        print 'Forward to WEST', speed
                        time.sleep(1.5)
                        pi2go.stop()
                        southBool= False;
                        west()          
   if keyp == '/':
                        print 'Exiting.....'
                        exit()


#FORWARD IS FACING NORTH
def north():
  northBool = True;
  while(northBool):
   keyp = readkey()
   if keyp == 'd' or keyp == RIGHT and northBool:
                        pi2go.spinRight(speed)
                        print 'TURING east RIGHT', speed
                        time.sleep(1.5)
                        pi2go.forward(speed)
                        print 'Forward to EAST', speed
                        time.sleep(1.5)
                        pi2go.stop()
                        northBool = False;
                        east()

   if keyp == 's' or keyp == DOWN and northBool:
                        pi2go.reverse(speed)
                        print 'Backward south', speed
                        time.sleep(1.5)
                        pi2go.stop()                    
   if keyp == 'w' or keyp == UP and northBool:
                        pi2go.forward(speed)
                        print 'North Forward', speed
                        time.sleep(1.5)
                        pi2go.stop()

   if keyp == 'a' or keyp == LEFT and northBool:
                        pi2go.spinLeft(speed)
                        print 'TURING west LEFT', speed
                        time.sleep(1.5)
                        pi2go.forward(speed)
                        print 'Forward to WEST', speed
                        time.sleep(1.5)
                        pi2go.stop()
                        northBool = False;
                        west()
   if keyp == '/':
                        print 'Exiting.....'
                        exit()

#Here is the code for a method that will be affected by current direction the robot is facing
navigation = {0:east,
                        1:west,
                        2:south,
                        3:north
}
pi2go.init()
#make a method for navigation
#make it so when robot turns to new direction turn the robot, then move it based on other varibles
try:
        while True:
                keyp = readkey()
                if keyp == 'd' or keyp == RIGHT:
                        print 'East is the head'
                        navigation[0]();
                elif keyp == 'a' or keyp == LEFT:
                        print 'West is the head'
                        navigation[1]();
                elif keyp == 's' or keyp == DOWN:
                        print 'South is the head'
                        navigation[2]();
                elif keyp == 'w' or keyp == UP:
                        print 'North is the head'
                        navigation[3]();
                elif keyp == '/':
                        print 'Exiting.....'
                        exit()

except KeyboardInterrupt:
        pi2go.cleanup()
