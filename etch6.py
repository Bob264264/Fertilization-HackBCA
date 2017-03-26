import serial
import time
import random
from graphics import *

MAX_X_SIZE = 800
MAX_Y_SIZE = 600

def distanceBtwPts(x, y):
    return (((x.getX()-y.getX())**2)
            +(x.getY()-y.getY())**2)**0.5

def areCirclesTouching(x, y):
    dist = distanceBtwPts(x.getCenter(), y.getCenter())
    return dist <= x.getRadius()+y.getRadius()

def areObstaclesTouching(x, y):
    dist = distanceBtwPts(x.getCenter(), y.getCenter())
    if dist<=25+distanceBtwPts(x.getCenter(), x.getP1())+distanceBtwPts(y.getCenter(),y.getP1()):
        return True
    return False
def areCircleAndObstacleTouching(c, o):
    xMinBound = min(o.getP1().getX(), o.getP2().getX())-c.getRadius()
    xMaxBound = max(o.getP1().getX(), o.getP2().getX())+c.getRadius()
    yMinBound = min(o.getP1().getY(), o.getP2().getY())-c.getRadius()
    yMaxBound = max(o.getP1().getY(), o.getP2().getY())+c.getRadius()
    return (c.getCenter().getX() <= xMaxBound and c.getCenter().getX() >= xMinBound) and (c.getCenter().getY() <= yMaxBound and c.getCenter().getY() >= yMinBound)

def areObstaclesTouchingInList(l, x):
    for o in l:
        if areObstaclesTouching(x, o):
            return True
    return False

win = GraphWin("title", MAX_X_SIZE, MAX_Y_SIZE)
title = Text(Point(MAX_X_SIZE/2, MAX_Y_SIZE/2-20), "FERTILIZE THAT EGG!")
title.setSize(32)
title.setFill("red")
title.draw(win)
prompt = Text(Point(MAX_X_SIZE/2, MAX_Y_SIZE/2+50), "Click Anywhere to Start")
prompt.setSize(24)
prompt.draw(win)
win.getMouse()
win.close()

roundNum = 1

ser = serial.Serial("COM7",9600)
x=100
y=100
pt = Circle(Point(x,y),10)
pt.setFill("purple")
goal = Circle(Point(600, 400), 40)
goal.setFill("yellow")
    
obstacles = [pt, goal]

while True:
    win = GraphWin("etch", MAX_X_SIZE, MAX_Y_SIZE)
    roundName = Text(Point(MAX_X_SIZE/2, MAX_Y_SIZE/2), "ROUND "+str(roundNum))
    roundName.setSize(32)
    roundName.setFill("red")
    roundName.draw(win)
    three = Text(Point(MAX_X_SIZE/2, MAX_Y_SIZE/2+70), str(3))
    three.setSize(18)
    three.draw(win)
    time.sleep(1)
    three.undraw()
    two = Text(Point(MAX_X_SIZE/2, MAX_Y_SIZE/2+70), str(2))
    two.setSize(18)
    two.draw(win)
    time.sleep(1)
    two.undraw()
    one = Text(Point(MAX_X_SIZE/2, MAX_Y_SIZE/2+70), str(1))
    one.setSize(18)
    one.draw(win)
    time.sleep(1)
    one.undraw()
    roundName.undraw()

    pt.draw(win)
    goal.draw(win)
    loseCt = 3
    isLose = False

    for i in range(20):
        obs_x = random.randint(90,MAX_X_SIZE-90)
        obs_y = random.randint(50,MAX_Y_SIZE-50)
        obs = Rectangle(Point(obs_x, obs_y), Point(obs_x+80,obs_y+20))
        while areObstaclesTouchingInList(obstacles, obs):
            obs_x = random.randint(90,MAX_X_SIZE-90)
            obs_y = random.randint(50,MAX_Y_SIZE-50)
            obs = Rectangle(Point(obs_x, obs_y), Point(obs_x+80,obs_y+20))
        obstacles.append(obs)
        obs.setFill("red")
        obs.draw(win)
    obstacles.remove(pt)
    obstacles.remove(goal)

    loser = False
    while not loser:
        displayLives = Text(Point(MAX_X_SIZE-50, MAX_Y_SIZE-575), "Lives: "+ str(loseCt))
        displayLives.setSize(18)
        displayLives.undraw()
        displayLives.draw(win)
        while True and not loser:
            coords = [str(x) for x in str(ser.readline()).split(" ")]
            x += int(coords[0][2:])
            y += int(coords[1][:-5])
            x %= MAX_X_SIZE
            y %= MAX_Y_SIZE
            pt = Circle(Point(x,y),5)
            pt.setFill("cyan")
            pt.draw(win)
            for o in obstacles:
                if areCircleAndObstacleTouching(pt,o):
                    loseCt-=1
                    loser = True
                    break
            if areCirclesTouching(pt, goal):
                win.close()
                loser = False
                break
            time.sleep(0.01)
        if not loser:
            win = GraphWin("Winner!", MAX_X_SIZE, MAX_Y_SIZE)
            mes = Text(Point(MAX_X_SIZE/2, MAX_Y_SIZE/2), "You Have Reached The Egg!")
            mes.setSize(32)
            mes.draw(win)
            playAgain = Text(Point(MAX_X_SIZE/2, MAX_Y_SIZE/2+75), "Click To Play Again")
            playAgain.setSize(18)
            playAgain.draw(win)
            break
        else:
            win.close()
            win = GraphWin("etch2", MAX_X_SIZE, MAX_Y_SIZE)
            x=100
            y=100
            pt = Circle(Point(x,y),10)
            pt.setFill("red")
            pt.draw(win)
            goal = Circle(Point(600, 400), 40)
            goal.setFill("purple")
            goal.draw(win)
            for o in obstacles:
                o.draw(win)
        loser = False
        if loseCt == 0:
            win.close()
            win = GraphWin("Loser :/", MAX_X_SIZE, MAX_Y_SIZE)
            mes = Text(Point(MAX_X_SIZE/2, MAX_Y_SIZE/2), "No Children For You!")
            mes.setSize(32)
            mes.draw(win)
            playAgain = Text(Point(MAX_X_SIZE/2, MAX_Y_SIZE/2+75), "Click To Play Again")
            playAgain.setSize(18)
            playAgain.draw(win)
            break
        roundNum+=1
        if loser:
            loser = False
            roundNum = 1
        win.getMouse()
        win.close()
    
        


