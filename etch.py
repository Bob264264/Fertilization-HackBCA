import serial
import time
from graphics import *

MAX_X_SIZE = 800
MAX_Y_SIZE = 600

win = GraphWin("etch", MAX_X_SIZE, MAX_Y_SIZE)
ser = serial.Serial("COM7",9600)
x=100
y=100
pt = Circle(Point(x,y),10)
pt.setFill("red")
pt.draw(win)

while True:
    coords = [str(x) for x in str(ser.readline()).split(" ")]
    x += int(coords[0][2:])
    y += int(coords[1][:-5])
    x %= MAX_X_SIZE
    y %= MAX_Y_SIZE
    pt = Circle(Point(x,y),5)
    pt.setFill("blue")
    pt.draw(win)
    time.sleep(0.01)
