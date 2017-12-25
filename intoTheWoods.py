from tkinter import *
from trees import *
from mazeFunctions import *
from tkinterGraphics import *
from weather import *
#from curvy import *
from doors import *
from grandma import *
import random

# This file initializes everything and handles the controls

def init(data):
	data.splashScreen = True # for test convenience 
	data.weather = None
	data.centers = initWeather(data)
	initShows(data)
	data.keyDown = 0
	data.stepsToSplit = 2
	data.finished = False # for testing convenience
	data.margin = 20
	initColors(data)
	data.space = 0
	data.maze = Maze(data)
	data.maze.makeBoard()
	data.treeList = makeTrees()
	data.counter = 0
	data.wolf = (0,0)
	data.lastMove = (0,0)
	data.reachesEnd = False
	data.prevPositions = list()
	data.margin = 20
	initScreenPositions(data)
	initRedData(data)
	initDirections(data)
	data.legalMoves = getLegalMoves(data)
	initPositions(data)
	data.keyPresses = 0
	data.skyGradient = makeGradient(data.skyColors,50)
	data.treeGradient = makeGradient(data.TREES,5)
	data.showBackText = False
	initHouse(data)
	initDoor(data)
	initEnding(data)


def initRedData(data):
	(data.hoodTopX,data.hoodTopY) = (0,0)
	(data.hoodBX,data.hoodBY) = (0,0)
	data.redRadius = 10
	data.position = (0,0)
	data.lastPosition = (None,None)
	data.redX = data.width/2
	data.redY = data.screenBottom-data.margin*3

def initShows(data):
	data.showHelp = False
	data.showMap = False # for testing convenience
	data.showCat =  False # for testing convenience
	data.showWolf = False
	data.showWolf2 = False
	data.showRed2 = False
	data.showText = True

def initColors(data):
	data.red = "#800101"
	data.SUNRISE = [(209,107,108),(249,161,101)]
	data.SUNSET = [(229,129,105),(190,25,84)]
	data.NOON = [(177,222,249),(0, 88, 148)]
	data.NIGHT = [(224,135,145),(13,15,45)]
	data.TREES = [(136,194,134),(20,54,36)]
	data.skyColors = None
	data.skyColors = getRandomSky(data) # gets a pair of colors
	data.colors2 = [ (249,161,101),  (229,129,105), (209,107,108),
					 (188,107,124), (168,104,131)]
	data.colors = ["#FAA165","#EF9A67","#E5946A","#DB8E6D",
	"#D18870","#C78273","#BC7C76","#B27679","#A8707C","#9E6A7F","#946482"]
	data.brown = "#a37575"
	data.brown2 = "#996666"
	data.lightBrown = "#b79494"
	data.darkBrown = "#7a5151"

def initDirections(data):
	data.bend = False
	data.straight = False
	data.split = False
	data.threeSplit = False
	data.direction = None #for printing
	data.NORTH = (-1,0)
	data.SOUTH = (1,0)
	data.EAST = (0,1)
	data.WEST = (0,-1)

def initPositions(data):
	data.catX = (data.screenRight+data.margin)/3
	data.catY = data.horizonLine*9/4
	data.catR = 20
	data.wolfX = (data.screenRight+data.margin)/3
	data.wolfY = data.horizonLine*2

def initScreenPositions(data):
	data.sspathMid = data.height/2+data.margin+data.height/12
	data.screenTop = data.screenLeft= data.margin
	data.screenRight = data.width*3/4-data.margin
	data.screenBottom = data.height-data.margin
	data.screenWidth = data.screenRight-data.screenLeft
	data.screenHeight = data.screenBottom-data.screenTop
	data.horizonLine = data.height/3

# makes a new maze for when the player presses down
def makeNewForest(data):
	data.maze = Maze(data)
	data.maze.makeBoard()
	data.position = getRandomPosition(data)
	data.lastPosition = (None,None)
	data.bend = False
	data.straight = False
	data.split = False
	data.threeSplit = False
	data.legalMoves = getLegalMoves(data)

# run function adapted from 112 notes here:
# https://www.cs.cmu.edu/~112/notes/events-example0.py

def mousePressed(event, data):
	if (data.showHelp):
		if (clickOnBack(event,data)):
			data.showHelp = False

	if (clickOnSkip(event,data)):
		if (data.showCat):
			data.showCat = False
			data.showMap = True
		elif (data.showWolf):
			data.showWolf = False
		elif (data.showWolf2):
			data.showWolf2 = False
		elif (data.showRed2):
			data.showRed2 = False
		elif (data.showBackText):
			data.showBackText = False
		data.space = 0
	if (clickOnHelp(event,data)):
		data.showHelp = True


def clickOnHelp(event,data):
	maze = data.maze
	x0 = maze.mazeX + maze.width/3
	y0 = maze.mazeY + maze.height + data.margin + 30
	x1 = x0 + 10
	y1 = y0 + 40
	x2 = x0
	y2 = y0 + data.margin + 30
	return event.x >= x0 and event.x <= x1 + data.margin*3 and event.y >= y0 and event.y <= y1

def clickOnBack(event,data):
	x0 = data.margin*2
	y0 = data.margin*2
	x1 = data.margin*6
	y1 = data.margin*4
	x2 = x0
	y2 = y0 + data.margin + 30
	return True
	return event.x >= x0 and event.x <= x1 + data.margin*3 and event.y >= y0 and event.y <= y1

def clickOnSkip(event,data):
	
	maze = data.maze
	x0 = maze.mazeX + maze.width/3
	y0 = maze.mazeY + maze.height + data.margin
	x1 = x0 + 10
	y1 = y0 + 10
	x2 = x0
	y2 = y0 + data.margin
	
	return event.x >= x0 and event.x <= x1 + data.margin*3 and event.y >= y0 and event.y <= y1

def sskeyPressed(event,data):
	if (event.keysym == "Right"):
		data.showText = False
		data.redX += 100
	if (event.keysym == "Left"):
		data.redX -= 100
	if (event.keysym ==  "space"):
		data.space += 1

def endKeyPressed(event,data):
	if (event.keysym == "Up"):
		data.redY -= 30
		if (data.redY <= data.horizonLine):
			data.finished = False
			data.endScreen = True
	elif (event.keysym == "Down"):
		data.redY += 30

def splitKeyPressed(event,data):
	
	if (data.stepsToSplit != 0):
		if (data.stepsToSplit<0):
			data.stepsToSplit = 2
		if (event.keysym == "Up"):
			data.stepsToSplit -=1
			return
		else:
			return
	if (event.keysym == "Left"):
		if ((data.WEST in data.legalMoves and data.SOUTH in data.legalMoves) 
			or (data.NORTH in data.legalMoves and data.EAST in data.legalMoves)):
			move = data.legalMoves[0]
		elif ((data.WEST in data.legalMoves and data.NORTH in data.legalMoves) 
			or (data.SOUTH in data.legalMoves and data.EAST in data.legalMoves)):
			move = data.legalMoves[1]
		elif (data.NORTH in data.legalMoves and data.SOUTH in data.legalMoves):
			if (data.lastMove == (0,+1)): # went left last time
				move = data.legalMoves[0]
			else:
				move = data.legalMoves[1]
		elif (data.WEST in data.legalMoves and data.EAST in data.legalMoves):
			if (data.lastMove == (-1,0)): # went down last time
				move = data.legalMoves[1]
			else:
				move = data.legalMoves[0]



	elif (event.keysym == "Right"):
		if (data.WEST in data.legalMoves and data.SOUTH in data.legalMoves 
			or data.NORTH in data.legalMoves and data.EAST in data.legalMoves):
			move = data.legalMoves[1]
		elif ((data.WEST in data.legalMoves and data.NORTH in data.legalMoves) 
			or (data.SOUTH in data.legalMoves and data.EAST in data.legalMoves)):
			move = data.legalMoves[0]
		elif (data.NORTH in data.legalMoves and data.SOUTH in data.legalMoves):
			if (data.lastMove == (0,+1)): # went left last time
				move = data.legalMoves[1]
			else:
				move = data.legalMoves[0]
		elif (data.WEST in data.legalMoves and data.EAST in data.legalMoves):
			if (data.lastMove == (-1,0)): # went down last time
				move = data.legalMoves[0]
			else:
				move = data.legalMoves[1]
	else: 
		return
	dRow = move[0]
	dCol = move[1]
	return (move,dRow,dCol)

def removeStraightPath(legalMoves):
	for move in legalMoves:
		if ((-move[0],-move[1]) not in legalMoves):
			legalMoves.remove(move)
			return

def keyPressed(event, data):

	if (data.finished):
		endKeyPressed(event,data)
		return

	if (event.keysym == "r"):
		init(data)
		return

	if (data.splashScreen == True):
		sskeyPressed(event,data)
		return

	if (event.keysym == "space" or data.showCat or data.showWolf or 
		data.showWolf2 or data.showRed2 or data.showBackText):
		
		data.space += 1
		return

	data.keyPresses+=1

	if (data.keyPresses >= 7):
		data.showWolf = True
		data.keyPresses-=100

	currentRow = data.position[0]
	currentCol = data.position[1]

	if (event.keysym == "Down"):
		data.keyDown += 1
		data.skyColors = getRandomSky(data)
		data.skyGradient = makeGradient(data.skyColors,50)
		data.centers = initWeather(data)
		makeNewForest(data)
		if (data.keyDown==1):
			data.showBackText = True
		return 
	
	if (data.straight):
		if (event.keysym=="Up"):
			if (len(data.legalMoves)==2):
				dRow = data.lastMove[0]
				dCol = data.lastMove[1]
			elif (len(data.legalMoves)==1):
				dRow = data.legalMoves[0][0]
				dCol = data.legalMoves[0][1]
			else:
				return

		else:
			return

	if (data.bend):
		
		if (event.keysym=="Right" or event.keysym=="Up"):
			move = data.legalMoves[0]
			dRow = move[0]
			dCol = move[1]
		else:
			return

	if (data.split):
		returned = splitKeyPressed(event,data)
		if (returned != None):
			(move,dRow,dCol) = returned
		else:
			return

	if (data.threeSplit):
		if (event.keysym == "Up"): # What if lastMove is (None,None) ??
			dRow = data.lastMove[0]
			dCol = data.lastMove[1]
		else:
			if ((data.lastMove[0],data.lastMove[1])==(None,None)):
				for move in (data.NORTH,data.SOUTH,data.WEST,data.EAST):
					if (move not in data.legalMoves):
						data.lastMove = move
			else:
				removeStraightPath(data.legalMoves)
				#data.legalMoves.remove((data.lastMove[0],data.lastMove[1]))
			(move,dRow,dCol) = splitKeyPressed(event,data)

	data.lastPosition = data.position
	data.position = (currentRow+dRow,currentCol+dCol)
	data.lastMove = (dRow,dCol)
	data.prevPositions.append(data.lastPosition)
	data.split = False
	data.straight = False
	data.bend = False
	data.threeSplit = False

	data.legalMoves = getLegalMoves(data)

	rows = len(data.maze.realBoard)
	cols = len(data.maze.realBoard[0])

	if(data.position == (rows-1,cols-1)):
		data.finished = True
		data.space = 0


def timerFired(data):
    if (data.redX > data.width and data.splashScreen):
    	data.splashScreen = False
    	data.showCat = True
    	data.space = -1
    if (data.finished):
    	doorTimerFired(data)
    if (data.weather == "SNOW"):
    	snowTimerFired(data)
    elif (data.weather == "RAIN"):
    	rainTimerFired(data)

 
def ssredrawAll(canvas,data):
	drawGradient(canvas,0,0,data.width,data.height,data.skyGradient)
	drawForest(canvas,data)
	drawssPath(canvas,data)
	drawRed(canvas,data)
	if (data.showText):
		drawText(canvas,data)

def redrawAll(canvas, data):
	if (data.showHelp == True):
		drawHelpScreen(canvas,data)
		return

	if (data.endScreen == True):
		endRedrawAll(canvas,data)
		return


	if (data.splashScreen == True):
		ssredrawAll(canvas,data)
		return
	drawGradient(canvas,0,0,data.width,data.height,data.skyGradient)
	
	
	drawFirstPersonView(canvas,data)
	if (data.finished):
		drawHouse(canvas,data)
		drawInsideOfHouse(canvas,data)
		drawDoor(canvas,data)

	if (data.showMap):
		data.maze.drawMaze(canvas,data)
	drawText(canvas,data)
	drawRed(canvas,data)
	if (data.showCat):
		drawCat(canvas,data)
	if (data.showWolf or data.showWolf2):
		drawWolf(canvas,data)
	
	drawButtons(canvas,data)
	if (data.weather == "SNOW"):
		drawSnow(canvas,data)
	elif (data.weather == "RAIN"):
		drawRain(canvas,data)
	
def run(width=1100, height=700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
    	# if (event.keysym == "r"):
    	# 	root.quit()
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

run()
