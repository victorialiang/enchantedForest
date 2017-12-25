from tkinter import *
import random

def initWeather(data):
	data.weather = getRandomWeather(data)
	if data.weather == "SNOW":
		centers = makeCenters(data,500)
	if data.weather == "RAIN":
		centers = makeCenters(data,500)
	return centers

def getRandomWeather(data):
	weathers = ["SNOW","RAIN"]
	return weathers[random.randint(0,len(weathers)-1)]

def drawRain(canvas,data):
	dropRadius = 1
	for drop in data.centers:
		dropX = drop[0]
		dropY = drop[1]
		canvas.create_rectangle(dropX-dropRadius,dropY-dropRadius,
								dropX+dropRadius,dropY+dropRadius,fill="#B1DEF9",outline="#B1DEF9")


def drawSnow(canvas,data):
	snowRadius = 1
	for flake in data.centers:
		flakeX = flake[0]
		flakeY = flake[1]
		canvas.create_oval(flakeX-snowRadius,flakeY-snowRadius,
						   flakeX+snowRadius,flakeY+snowRadius,fill="white",outline="white")

def drawSnowGround(canvas,data):
	canvas.create_oval(data.screenLeft*9/8,data.screenBottom,data.screenLeft*10,data.screenBottom*3/4,fill="white",outline="white")

def makeCenters(data,numFlakes):
	centers = list()
	xRange = (0,data.width)
	yRange = (0,data.height)
	for i in range(numFlakes):
		center = (random.randint(xRange[0],xRange[1]),random.randint(yRange[0],yRange[1]))
		centers.append(center)
	return centers

def snowTimerFired(data):
	dx = 0
	dy = 0.05
	for flake in data.centers:
		flakeX=flake[0]+dx
		flakeY=flake[1]+dy
		if (flakeY>data.height):
			flakeY = 0
		flake = (flakeX,flakeY)
		data.centers.pop(0)
		data.centers.append(flake)

def rainTimerFired(data):
	dx = 0
	dy = 1
	for flake in data.centers:
		flakeX=flake[0]+dx
		flakeY=flake[1]+dy
		if (flakeY>data.height):
			flakeY = 0
		flake = (flakeX,flakeY)
		data.centers.pop(0)
		data.centers.append(flake)
