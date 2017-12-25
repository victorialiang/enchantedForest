from tkinter import *
from tkinterGraphics import *

def initEnding(data):
	data.endScreen = False # for testing convenience
	data.endSkyColors = [(200,210,250),(250,215,232)]
	data.endGradient = makeGradient(data.endSkyColors,50)
	data.redY = data.height/4

def drawInterior(canvas,data):
	height = data.height/4
	canvas.create_polygon(data.width/4,data.height/4,
						  data.width/2,data.height/4-data.height/5,
						  data.width/2,data.height/4-data.height/5 + height,
						  data.width/4,data.height/4+height,
						  fill = data.brown)
	canvas.create_polygon(data.width*3/4,data.height/4,
						  data.width/2,data.height/4-data.height/5,
						  data.width/2,data.height/4-data.height/5 + height,
						  data.width*3/4,data.height/4+height,
						  fill = data.lightBrown)
	canvas.create_polygon(data.width/4,data.height/4+height,
						  data.width/2,data.height/4-data.height/5 + height,
						  data.width*3/4,data.height/4+height,
						  data.width/2,data.height/4+data.height/5 + height,
						  fill = data.darkBrown)


def drawEndText(canvas,data):
	canvas.create_text(data.width/4,data.height*4/5,
		text = "You Won!"+"\nPress r to play again",font = ("Verdana",20),fill = "gray")

def endRedrawAll(canvas,data):
	data.redX = data.width*7/12

	drawGradient(canvas,0,0,data.width,data.height,data.endGradient)
	drawInterior(canvas,data)
	drawRed(canvas,data)
	drawEndText(canvas,data)
