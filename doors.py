from tkinter import *
from tkinterGraphics import *

def initHouse(data):
	margin = (data.screenRight-data.margin)/6
	data.houseLeft = data.screenLeft+margin*2
	data.houseRight = data.screenLeft+margin*4

def initDoor(data):
	houseWidth = (data.houseRight - data.houseLeft)
	data.doorWidth = houseWidth/6
	data.doorX0 = data.houseLeft + data.doorWidth * 2
	data.doorY0 = data.horizonLine*2/3
	data.doorX1 = data.doorX0 + data.doorWidth
	data.doorY1 = data.doorY0
	data.doorX2 = data.doorX0 + data.doorWidth*2
	data.doorY2 = data.doorY0
	data.doorX3 = data.doorX0 + data.doorWidth
	data.doorY3 = data.doorY0
	#data.doorDx = -data.doorWidth/6
	#data.doorDy = data.doorDx
	data.doorDx = -3
	data.doorDy = +3
	data.doorHeight = data.horizonLine - data.doorY0


def doorTimerFired(data):
	data.doorX1 += data.doorDx
	data.doorY1 += data.doorDy
	data.doorX3 -= data.doorDx
	data.doorY3 += data.doorDy

	if (data.doorX1 <= data.doorX0-data.doorWidth/4):
		data.doorDx = 0
		data.doorDy = 0

def drawDoor(canvas,data):
	canvas.create_polygon(data.doorX0,data.doorY0,data.doorX1,data.doorY1,
						  data.doorX1,data.doorY1+data.doorHeight,data.doorX0,data.doorY0+data.doorHeight,
						  fill="white")
	canvas.create_polygon(data.doorX2,data.doorY2,data.doorX3,data.doorY3,
						  data.doorX3,data.doorY3+data.doorHeight,data.doorX2,data.doorY2+data.doorHeight,
						  fill="white")

def drawInsideOfHouse(canvas,data):
	#drawGradient(canvas,xTop,yTop,xBottom,yBottom,colorList)
	gradient = makeGradient(data.NIGHT,90)
	drawGradient(canvas,data.houseLeft + data.doorWidth * 2,data.doorY0,
				 data.houseLeft+data.doorWidth*4,data.horizonLine,
				 gradient)
	#color = rgbString(data.NIGHT[1][0],data.NIGHT[1][1],data.NIGHT[1][2])
	# color = rgbString(data.skyColors[0][0],data.skyColors[0][1],data.skyColors[0][2])
	# canvas.create_rectangle(data.houseLeft + data.doorWidth * 2,data.doorY0,
	# 						data.houseLeft+data.doorWidth*4,data.horizonLine,
	# 						fill=color,outline=color)
