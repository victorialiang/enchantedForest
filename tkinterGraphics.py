from tkinter import *
#from colour import *
from trees import *
from mazeFunctions import *
import random


def drawHelpScreen(canvas,data):
	drawGradient(canvas,0,0,data.width,data.height,data.endGradient)
	canvas.create_text(data.width/2,data.height/3,
		text="\nThe goal of this game is to reach the purple square."+
		" \n\nUse the arrow keys to move through the maze."+
		" \n\nBe wary of perspective changes! "+
		"\n\nPressing the down key will place you in a new forest.",
		font = ("Verdana",20),fill = "gray")
	canvas.create_polygon(data.margin*2,data.margin*2,data.margin*2,
						  data.margin*2+data.margin,data.margin*2-data.margin,
						  data.margin*2+10,fill = "gray")
	canvas.create_text(data.margin*4,data.margin*2+10,text = "Back",
					   fill = "gray",font = ("Verdana",20))




def drawButtons(canvas,data):
	maze = data.maze
	x0 = maze.mazeX + maze.width/3
	y0 = maze.mazeY + maze.height + data.margin
	x1 = x0 + 10
	y1 = y0 + 10
	x2 = x0
	y2 = y0 + data.margin
	canvas.create_polygon(x0,y0,x1,y1,x2,y2,fill=data.colors[1])
	canvas.create_text(x1+data.margin,y1,text="Skip",
					   font=("Verdana",10),fill="white")
	canvas.create_polygon(x0,y0+30,x1,y1+30,x2,y2+30,fill = data.colors[2])
	canvas.create_text(x1+data.margin,y1+30,text="Help",
					   font=("Verdana",10),fill="white")

def getRandomSky(data):
	skies = [data.SUNRISE,data.SUNSET,data.NOON,data.NIGHT]

	if (data.skyColors == None):
		sky = random.randint(0,len(skies)-1)
		return skies[sky]
	else:
		sky = random.randint(0,len(skies)-1)
		while(skies[sky] == data.skyColors):
			print("hi")
			sky = random.randint(0,len(skies)-1)
		return skies[sky]

def makeGradient(colors,divs):
	rList = list()
	gList = list()
	bList = list()
	
	for i in range(len(colors)-1):
		color = getGradient(colors[i],colors[i+1],divs)
		rList+= color[0]
		gList+= color[1]
		bList += color[2]

	colorList = list()
	for i in range(len(rList)):
		colorList.append((rList[i],gList[i],bList[i]))
	   
	return colorList

def getGradient(c1,c2,steps):
	deltaR = (max(c1[0],c2[0])-min(c1[0],c2[0]))//steps
	deltaG = (max(c1[1],c2[1])-min(c1[1],c2[1]))//steps
	deltaB = (max(c1[2],c2[2])-min(c1[2],c2[2]))//steps

	rList = list()
	gList = list()
	bList = list()

	for i in range(steps):
		rList.append(min(c1[0],c2[0])+deltaR*i)
		gList.append(min(c1[1],c2[1])+deltaG*i)
		bList.append(min(c1[2],c2[2])+deltaB*i)
	return (rList,gList,bList)

def drawGradient(canvas,xTop,yTop,xBottom,yBottom,colorList):
	divisions = len(colorList)
	width = (xBottom-xTop)/divisions
	height = (yBottom-yTop)/divisions
	div = 0
	for color in colorList:
		canvas.create_rectangle(xTop,yTop+height*div,
								xBottom,yTop+height*(div+1),
								fill=rgbString(color[0],color[1],color[2]),
								outline=rgbString(color[0],color[1],color[2]))
		div+=1


def getRandomColor(num1,num2):
	colors = list()
	for i in range(3):
		colors.append(random.randint(num1,num2))
	return (colors[0],colors[1],colors[2])

# rgbString helper function from 112 notes
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def drawTextBox(canvas,xc,yc,text,color):

	width = len(text) * 10
	x0 = xc - width/2
	y0 = yc - 20
	x1 = xc+ width/2
	y1 = yc + 20
	if "\n" in text:
		x0 += width/8
		x1 -= width/8
	canvas.create_rectangle(x0, y0, x1, y1, fill = color,outline=color)
	canvas.create_text(xc,yc,text = text,fill = "white",font=("Verdana", 10))
	mid = xc
	canvas.create_polygon(mid-10, y1, mid+10, y1, mid,y1+10,fill=color)

# xStart and yStart are at the base of the trees
def drawForestInGame(canvas,data,numTrees,xStart,yStart,width,height):
	for i in range(numTrees):
		tree = threeSplitTree(4)
		
		tree.drawTree(canvas,height,tree.level,
					  xStart+ width*(i),yStart-height,
					  xStart + width*(i),yStart,10,
					  rgbString(data.treeGradient[i][0],data.treeGradient[i][1],
					  	data.treeGradient[i][2]))


def drawStraightPathForest(canvas,data,numTrees):
	if (data.finished): return
	margin = (data.screenBottom-data.horizonLine)/numTrees
	for i in range(numTrees-1,-1,-1):
		tree = threeSplitTree(4)
		#self,canvas,height,level,xtop,ytop,xbottom,ybottom,width=10,color="#947A6F"
		height = data.horizonLine/2
		ybottom = data.screenBottom-(margin*(i+1))
		tree.drawTree(canvas,height,tree.level,
					 (i+1)*margin,ybottom-height,
					 (i+1)*margin,ybottom,10,
					 rgbString(data.treeGradient[i][0],data.treeGradient[i][1],
					 	data.treeGradient[i][2]))

		tree.drawTree(canvas,height,tree.level,
					 data.screenRight-(i+1)*margin+data.margin,ybottom-height,
					 data.screenRight-(i+1)*margin+data.margin,ybottom,10,
					 rgbString(data.treeGradient[i][0],data.treeGradient[i][1],
					 	data.treeGradient[i][2]))


def draw2DirectionsForest(canvas,data):
	if (data.finished): return
	if (data.stepsToSplit==2):
		translation = data.margin*2
		numTrees = 1
		width = ((data.screenRight-data.margin) - (data.screenLeft+data.margin)) / numTrees

		drawForestInGame(canvas,data,numTrees,data.screenRight/2,
						data.horizonLine+translation,0,data.horizonLine/2)
		
		
	elif (data.stepsToSplit==1):
		translation = data.margin*2
		width = ((data.screenRight-data.margin) - (data.screenLeft+data.margin)) / 3

		numTrees = 2
		drawForestInGame(canvas,data,numTrees,width*1.2,
			data.horizonLine+translation,width-data.margin*2,data.horizonLine/2)

		numTrees = 1
		width = ((data.screenRight-data.margin) - (data.screenLeft+data.margin)) / numTrees

		drawForestInGame(canvas,data,numTrees,data.screenRight/2,
			data.horizonLine*1.5+translation,0,data.horizonLine/2)

		
		
	else:
		numTrees = 5
		width = ((data.screenRight-data.margin) - (data.screenLeft+data.margin)) / numTrees
		drawForestInGame(canvas,data,numTrees,width,data.horizonLine+data.margin,
			width,data.horizonLine/2)
		numTrees = 4
		width = ((data.screenRight-data.margin) - (data.screenLeft+data.margin)) / numTrees
		drawForestInGame(canvas,data,numTrees,width-data.margin,data.horizonLine*1.5,
			width,data.horizonLine/2)
		numTrees = 3
		width = ((data.screenRight-data.margin) - (data.screenLeft+data.margin)) / numTrees
		drawForestInGame(canvas,data,numTrees,width-data.margin,data.horizonLine*1.7,
			width-data.margin*2,data.horizonLine/2)
		numTrees = 2
		drawForestInGame(canvas,data,numTrees,width*1.2,data.horizonLine*2,
			width-data.margin*2,data.horizonLine/2)

		numTrees = 1
		width = ((data.screenRight-data.margin) - (data.screenLeft+data.margin)) / numTrees

		drawForestInGame(canvas,data,numTrees,data.screenRight/2,
			data.horizonLine*2.2,0,data.horizonLine/2)
		drawStraightPathForest(canvas,data,2)





def draw2Directions(canvas,data):


	if (data.stepsToSplit==2):
		draw2DirectionsForest(canvas,data)
		draw2AwayFrom2Directions(canvas,data)

		return
	elif (data.stepsToSplit==1):
		draw2DirectionsForest(canvas,data)
		draw1AwayFrom2Directions(canvas,data)

		return
	else:
		
		draw2DirectionsForest(canvas,data)

		canvas.create_polygon(data.screenLeft+data.screenWidth/4,data.screenBottom,
							data.screenLeft,data.screenHeight/2,
							data.screenLeft,data.horizonLine,
							data.screenLeft+data.margin,data.horizonLine,
							data.screenLeft+ data.screenWidth*3/4,data.screenBottom,fill=data.brown)
		canvas.create_polygon(data.screenLeft+ data.screenWidth*3/4,data.screenBottom,
							data.screenRight,data.screenHeight/2,
							data.screenRight,data.horizonLine,
							data.screenRight-data.margin,data.horizonLine,
							data.screenLeft+data.screenWidth/4,data.screenBottom,fill=data.brown)



def draw3Directions(canvas,data):
	temp = data.stepsToSplit
	data.stepsToSplit = 0
	draw2Directions(canvas,data)
	drawStraightPath(canvas,data)
	
	data.stepsToSplit = temp

def draw2AwayFrom2Directions(canvas,data):
	canvas.create_polygon(data.screenLeft+data.screenWidth/4,data.screenBottom,
						
						data.screenLeft+data.screenWidth/5+data.margin,data.horizonLine,
						data.screenLeft+data.screenWidth/5*2+data.margin,data.horizonLine,
						data.screenLeft+ data.screenWidth*3/4,data.screenBottom,
						fill=data.brown)
	canvas.create_polygon(data.screenRight-data.screenWidth/4,data.screenBottom,
						
						data.screenRight-data.screenWidth/5-data.margin,data.horizonLine,
						data.screenRight-data.screenWidth/5*2-data.margin,data.horizonLine,
						data.screenRight- data.screenWidth*3/4,data.screenBottom,
						fill=data.brown)
	

def draw1AwayFrom2Directions(canvas,data):
	canvas.create_polygon(data.screenLeft+data.screenWidth/4,data.screenBottom,
						
						data.screenLeft+data.screenWidth/7+data.margin,data.horizonLine,
						data.screenLeft+data.screenWidth/7*2+data.margin,data.horizonLine,
						data.screenLeft+ data.screenWidth*3/4,data.screenBottom,
						fill=data.brown)
	canvas.create_polygon(data.screenRight-data.screenWidth/4,data.screenBottom,
						
						data.screenRight-data.screenWidth/7-data.margin,data.horizonLine,
						data.screenRight-data.screenWidth/7*2-data.margin,data.horizonLine,
						data.screenRight- data.screenWidth*3/4,data.screenBottom,fill=data.brown)
	

def drawStraightPath(canvas,data):

	canvas.create_polygon(data.screenLeft+data.screenWidth/4,data.screenBottom,
						data.screenLeft+data.screenWidth/2-data.margin,data.horizonLine,
						data.screenLeft+data.screenWidth/2+data.margin,data.horizonLine,
						data.screenLeft+ data.screenWidth*3/4, data.screenBottom,
						fill = data.brown)
	drawStraightPathForest(canvas,data,4)

def drawBendInRoad(canvas,data):
	canvas.create_rectangle(data.screenLeft+data.screenWidth/2-data.margin,data.horizonLine,
							data.screenRight,data.horizonLine*4/3,fill=data.brown,
							outline=data.brown)
	drawStraightPath(canvas,data)

	
	

def drawFirstPersonView(canvas,data):
	
	if len(data.legalMoves)==0:
		# at dead end
		data.straight = True
		drawStraightPath(canvas,data)
	if len(data.legalMoves)==1:
		firstMove = data.lastMove
		secondMove = data.legalMoves[0]
		if (abs(firstMove[0])==abs(secondMove[1]) and abs(firstMove[1])==abs(secondMove[0])):
			data.bend = True
			drawBendInRoad(canvas,data)
		else:
			data.straight = True
			drawStraightPath(canvas,data)
	if len(data.legalMoves)==2:
		firstMove = data.legalMoves[0]
		secondMove = data.legalMoves[1]
		if (-firstMove[0]==secondMove[0] and -firstMove[1]==secondMove[1]and 
			data.lastMove in data.legalMoves):
			data.straight = True
			data.split = False
		
			drawStraightPath(canvas,data)
			return
		else:	
			data.split = True
			data.straight = False
			
			draw2Directions(canvas,data)
	if len(data.legalMoves)==3 or len(data.legalMoves)==4:
		data.straight = False
		data.threeSplit = True
		draw3Directions(canvas,data)

def drawScreen(canvas,data):
	# draw screen background

	canvas.create_rectangle(0,0,data.width,data.height,fill=data.colors[5],outline=data.colors[5])

	

	canvas.create_rectangle(data.screenLeft,data.screenTop,data.screenRight,
		data.screenBottom,fill="#71B3A4",outline="#71B3A4")

	currentRow = data.position[0]
	currentCol = data.position[1]


	height = data.horizonLine/11
	for color in range(11):
		if (color == 10):
			canvas.create_rectangle(data.screenLeft,data.screenTop+height*(color),
									data.screenRight,data.screenBottom,
									fill=data.colors[color],outline=data.colors[color])
		else:
			canvas.create_rectangle(data.screenLeft,data.screenTop+height*(color),
								data.screenRight,data.screenTop+(height*2)*(color+1),
								fill=data.colors[color],outline=data.colors[color])


def makeTrees():
	treeLevel = 5
	treeList = []
	for i in range(10):
		funkyTree = threeSplitTree(treeLevel)
		treeList.append(funkyTree)
	return treeList

def drawForest(canvas,data):
	# self,canvas,height,level,xtop,ytop,xbottom,ybottom,width=10
	treeList = data.treeList
	increment = data.width/5
	exp = increment

	xtop = increment

	ytop = data.height/7
	height = data.height/3
	xbottom = xtop
	ybottom = ytop + height
	for tree in treeList:
			
		tree.drawTree(canvas,height,tree.level,xtop,ytop,xbottom,ybottom,10,data.brown)
		

		xtop+= increment
		xbottom = xtop
		exp+= exp

def drawssPath(canvas,data):
	data.margin = 20

	data.sspathMid = data.height/2+data.margin+data.height/12

	canvas.create_rectangle(0,data.height/2+data.margin,data.width+5,
		data.height/2+data.margin+data.height/6,
							fill=data.brown2,outline=data.brown2)

	# draw sign

	canvas.create_rectangle(data.width*3/4,data.height/3+data.margin,
		data.width*3/4+data.width/10,data.height/3+data.margin*3,
							fill=data.brown2,outline=data.brown2)
	canvas.create_rectangle(data.width*3/4+data.width/20-5,
							data.height/3+data.margin*3,
							data.width*3/4+data.width/20+5,
							data.height/2,fill=data.brown2,outline=data.brown2)

	canvas.create_text(data.width*3/4+data.width/20,data.height/3+data.margin*2,
		text="Enchanted \nForest ",fill="white")

def drawCat(canvas,data):
	data.white = "white"
	r = data.catR
	height = r*3

	canvas.create_polygon(data.catX,data.catY-height+r,
						  data.catX-r,data.catY,
						  data.catX+r,data.catY,fill=data.white) # triangle cone
	
	ovalR = 5
	canvas.create_oval(data.catX-r,data.catY-ovalR,data.catX+r,data.catY+ovalR,
	fill=data.white,outline=data.white) # circle cone
	canvas.create_oval(data.catX-r,data.catY-height-r,data.catX+r,data.catY-height+r,
	fill=data.white,outline=data.white) # head
	ear = r/3
	canvas.create_polygon(data.catX-r,data.catY-height,
						  data.catX-r+ear*2,data.catY-height,
						  data.catX-r+ear,data.catY-height-2*r,fill=data.white) # draw left ear
	canvas.create_polygon(data.catX+r-ear*2,data.catY-height,
						  data.catX+r,data.catY-height,
						  data.catX+r+ear-ear*2,data.catY-height-2*r,fill=data.white) # draw right ear
	


def drawWolf(canvas,data):
	data.gray = "#2e1f1f"
	r = 15
	height = r*4
	
	canvas.create_polygon(data.wolfX,data.wolfY-height+r,
						  data.wolfX-r,data.wolfY,
						  data.wolfX+r,data.wolfY,fill=data.gray) # triangle cone
	
	ovalR = 5
	canvas.create_oval(data.wolfX-r,data.wolfY-ovalR,data.wolfX+r,
	data.wolfY+ovalR,fill=data.gray,outline=data.gray) # circle cone
	canvas.create_oval(data.wolfX-r,data.wolfY-height-r,data.wolfX+r,
	data.wolfY-height+r,fill=data.gray,outline=data.gray) # head
	ear = r/3
	canvas.create_polygon(data.wolfX-r,data.wolfY-height,
						  data.wolfX-r+ear*2,data.wolfY-height,
						  data.wolfX-r+ear,data.wolfY-height-2*r,fill=data.gray) # draw left ear
	canvas.create_polygon(data.wolfX+r-ear*2,data.wolfY-height,
						  data.wolfX+r,data.wolfY-height,
						  data.wolfX+r+ear-ear*2,data.wolfY-height-2*r,fill=data.gray) # draw right ear
	nose = r*2
	canvas.create_polygon(data.wolfX,data.wolfY-height,
						  data.wolfX+nose,data.wolfY-height,data.wolfX,
						  data.wolfY-height+r,fill=data.gray) # draw nose


def drawSplashScreenRed(canvas,data):
	
	height = data.redRadius*4
	data.redY = data.sspathMid

	canvas.create_polygon(data.redX,data.redY-data.redHeight+data.redRadius,
						  data.redX-2*data.redRadius,data.redY,
						  data.redX+2*data.redRadius,data.sspathMid,fill=red) # triangle cone
	# center = data.redX,data.sspathMid
	ovalR = 5
	canvas.create_oval(data.redX-2*r,data.sspathMid-ovalR,
					   data.redX+2*r,data.sspathMid+ovalR,
					   fill=red,outline=red) # circle cone
	canvas.create_oval(data.redX-2*r,data.sspathMid-height-2*r,
					   data.redX+2*r,data.sspathMid-height+r,
					   fill=red,outline=red) # hood
	canvas.create_oval(data.redX-r,data.sspathMid-height-r,
					   data.redX+r,data.sspathMid-height+r,
					   fill="white",outline="white") # head
	canvas.create_polygon(data.redX-2*r,data.sspathMid-height-r,
						  data.redX,data.sspathMid-height-7/2*r,
						  data.redX+2*r,data.sspathMid-height-r,fill=red)
	data.redY = data.sspathMid-height-7/2*r - data.margin



def drawRed(canvas,data):
	red = data.red
	r = data.redRadius
	height = r*4
	if (data.splashScreen):

		canvas.create_polygon(data.redX,data.sspathMid-height+r,
							  data.redX-2*r,data.sspathMid,
							  data.redX+2*r,data.sspathMid,fill=red) # triangle cone
		# center = data.redX,data.sspathMid
		ovalR = 5
		canvas.create_oval(data.redX-2*r,data.sspathMid-ovalR,data.redX+2*r,
		data.sspathMid+ovalR,fill=red,outline=red) # circle cone
		canvas.create_oval(data.redX-2*r,data.sspathMid-height-2*r,data.redX+2*r,
		data.sspathMid-height+r,fill=red,outline=red) # hood
		canvas.create_oval(data.redX-r,data.sspathMid-height-r,data.redX+r,
		data.sspathMid-height+r,fill="white",outline="white") # head
		canvas.create_polygon(data.redX-2*r,data.sspathMid-height-r,
							  data.redX,data.sspathMid-height-7/2*r,
							  data.redX+2*r,data.sspathMid-height-r,fill=red)
		data.redY = data.sspathMid-height-7/2*r - data.margin

	else:
		data.redX = (data.screenRight+data.margin)/2

		if (data.endScreen):
			data.redY = data.height/2 + data.margin*1.5
			data.redX = data.width/2 + data.margin*4

		elif not (data.finished):
			data.redY = data.screenBottom-data.margin*3

		# data.redY = data.screenBottom-data.margin*3
		(data.hoodTopX,data.hoodTopY) = (data.redX,data.redY-height-7/2*r)
		(data.hoodBX,data.hoodBY) = (data.redX+2*r,data.redY-height-r)
		canvas.create_polygon(data.redX,data.redY-height+r,
							  data.redX-2*r,data.redY,
							  data.redX+2*r,data.redY,fill=red) # triangle cone
		ovalR = 5
		canvas.create_oval(data.redX-2*r,data.redY-ovalR,data.redX+2*r,
		data.redY+ovalR,fill=red,outline=red) # circle cone
		canvas.create_oval(data.redX-2*r,data.redY-height-2*r,data.redX+2*r,
		data.redY-height+r,fill=red,outline=red) # hood
		if (data.endScreen):
			canvas.create_oval(data.redX-r,data.redY-height-r,data.redX+r,
			data.redY-height+r,fill="white",outline="white") # head

		canvas.create_polygon(data.redX-2*r,data.redY-height-r,
							  data.hoodTopX,data.hoodTopY,
							  data.redX+2*r,data.redY-height-r,fill=red)

def drawRedText(canvas,data):
	redTexts4=["...","I'm not sure if that helped..."]

	if (data.space>=len(redTexts4)):
		data.showRed2 = False
		data.space = 0
		return

	drawTextBox(canvas,data.redX,data.redY-data.redRadius*4-7/2*data.redRadius-data.margin*2,
		redTexts4[data.space],data.brown2)

def drawBackText(canvas,data):
	backTexts = [" ? ","Have I been here before?","This is a strange forest."]

	if (data.space>=len(backTexts)):
		data.showBackText = False
		return

	drawTextBox(canvas,data.redX,data.redY-data.redRadius*4-7/2*data.redRadius-data.margin*2,
		backTexts[data.space],data.brown2)



def drawWolfTexts2(canvas,data):
	r = 15
	height = r*4

	catTexts4 = ["Here we are!"]

	if (data.space>=len(catTexts4)):
		data.showRed2 = True
		data.showWolf2 = False
		data.space = 0
		return
	
	drawTextBox(canvas,data.wolfX,data.wolfY-height-2*r-data.margin*2,
		catTexts4[0],data.colors[0])
	

def drawWolfTexts(canvas,data):
	# cat is really wolf

	catTexts = ["Hullo","Where are you going?"]
	redTexts = ["I'm going to my \ngrandmother's house"]
	catTexts2 = [" Oh! ","I know a shortcut"]
	redTexts2 = ["Do you really?"]
	catTexts3 = ["Follow me!"]
	redTexts3=["..."," Sure "]
	catTexts4 = ["Here we are!"]
	redTexts4=["...","I don't think that helped"]

	if (data.space<len(catTexts)):
		text = catTexts[data.space]
		character = "cat"
	elif (data.space<len(redTexts)+len(catTexts)):
		text = redTexts[data.space-len(catTexts)]
		character = "red"
	elif (data.space<len(redTexts)+len(catTexts)+len(catTexts2)):
		text = catTexts2[data.space-(len(redTexts)+len(catTexts))]
		character = "cat"

	elif (data.space<len(redTexts)+len(catTexts)+len(catTexts2)+len(redTexts2)):
		text = redTexts2[data.space-(len(redTexts)+len(catTexts)+len(catTexts2))]
		data.showMap = True
		character = "red"

	elif (data.space<len(redTexts)+len(catTexts)+len(catTexts2)+len(redTexts2)+
		len(catTexts3)):
		text = catTexts3[data.space-(len(redTexts)+len(catTexts)+len(catTexts2)+
			len(redTexts2))]
		character = "cat"

	elif (data.space<len(redTexts)+len(catTexts)+len(catTexts2)+len(redTexts2)+
		len(catTexts3)+len(redTexts3)):
		text = redTexts3[data.space-(len(redTexts)+len(catTexts)+len(catTexts2)+
			len(redTexts2)+len(catTexts3))]
		character = "red"


	
	else:
		data.position = getRandomPosition(data)
		data.lastPosition = (None,None)
		data.bend = False
		data.straight = False
		data.split = False
		data.threeSplit = False
		data.legalMoves = getLegalMoves(data)
		data.showWolf = False
		data.showWolf2 = True
		data.space = 0
		return
	

	r = 15
	height = r*4

	if (character == "red"):
		drawTextBox(canvas,data.redX,data.redY-data.redRadius*4-7/2*data.redRadius-data.margin*2,
			text,data.brown2)
	elif (character == "cat"):
		drawTextBox(canvas,data.wolfX,data.wolfY-height-2*r-data.margin*2,text,
			data.colors[6])


def drawText(canvas,data):
	if (data.splashScreen):
		height = 40
		texts = ["Press Space to Begin","Keep pressing Space to interact!",
		"And arrow keys to move","Try going right!"]

		if (data.space>=len(texts)):
			data.space = len(texts)-1
		# canvas,xc,yc,text,color

		drawTextBox(canvas,data.redX,data.redY-2*data.redRadius,texts[data.space],
			data.brown2)		

	elif (data.showCat and data.space>=0):
		catTexts = ["Hello","I am the Spirit of the forest","What business do you have here?"]
		redTexts = ["I'm going to my \ngrandmother's house","I'm bringing her some \ncake and wine"]
		catTexts2 = [" Oh! ","How lovely!","Please take a map"]
		redTexts2 = ["Thanks!"]
		catTexts3 = ["This is a strange forest","If you turn around, you might get lost"]
		redTexts3=["..."]
		catTexts4 = ["Good luck!","And watch out for that wolf!"]

		if (data.space<len(catTexts)):
			text = catTexts[data.space]
			character = "cat"
		elif (data.space<len(redTexts)+len(catTexts)):
			text = redTexts[data.space-len(catTexts)]
			character = "red"
		elif (data.space<len(redTexts)+len(catTexts)+len(catTexts2)):
			text = catTexts2[data.space-(len(redTexts)+len(catTexts))]
			character = "cat"

		elif (data.space<len(redTexts)+len(catTexts)+len(catTexts2)+len(redTexts2)):
			text = redTexts2[data.space-(len(redTexts)+len(catTexts)+len(catTexts2))]
			data.showMap = True
			character = "red"

		elif (data.space<len(redTexts)+len(catTexts)+len(catTexts2)+len(redTexts2)
			+len(catTexts3)):
			text = catTexts3[data.space-(len(redTexts)+len(catTexts)+len(catTexts2)
				+len(redTexts2))]
			character = "cat"

		elif (data.space<len(redTexts)+len(catTexts)+len(catTexts2)+len(redTexts2)
			+len(catTexts3)+len(redTexts3)):
			text = redTexts3[data.space-(len(redTexts)+len(catTexts)+len(catTexts2)
				+len(redTexts2)+len(catTexts3))]
			character = "red"

		elif (data.space<len(redTexts)+len(catTexts)+len(catTexts2)+len(redTexts2)
			+len(catTexts3)+len(redTexts3)+len(catTexts4)):
			text = catTexts4[data.space-(len(redTexts)+len(catTexts)+len(catTexts2)
				+len(redTexts2)+len(catTexts3)+len(redTexts3))]
			character = "cat"

		else:
			data.showCat = False
			data.space = 0
			return


		if (character == "red"):
			drawTextBox(canvas,data.redX,data.redY-data.redRadius*4-7/2*data.redRadius-data.margin*2,
				text,data.brown2)
		elif (character == "cat"):
			drawTextBox(canvas,data.catX,data.catY-7*data.catR,text,data.colors[6])
	elif (data.showWolf):
		drawWolfTexts(canvas,data)
	elif (data.showWolf2):
		drawWolfTexts2(canvas,data)
	elif (data.showRed2):
		drawRedText(canvas,data)
	elif (data.showBackText):
		drawBackText(canvas,data)


def drawSky(canvas,data):
	colors = data.colors
	height = data.sspathMid/11
	for i in range(11):
		if i == 10:
			canvas.create_rectangle(0,0+height*i,data.width,data.height,
				fill=colors[i],outline=colors[i])
		else: canvas.create_rectangle(0,0+height*i,data.width,height*(i+1),
			fill=colors[i],outline=colors[i])

def drawHouse(canvas,data):

	margin = (data.screenRight-data.margin)/6
	data.houseLeft = data.screenLeft+margin*2
	data.houseRight = data.screenLeft+margin*4
	canvas.create_rectangle(data.screenLeft+margin*2,data.horizonLine/2,
		data.screenLeft+margin*4,data.horizonLine,fill=data.brown
		,outline=data.brown)
	canvas.create_polygon(data.screenLeft+margin*2,data.horizonLine/2+data.margin*3,
						  data.screenLeft+(data.screenRight-data.margin)/2,data.horizonLine/4,
						  data.screenRight-margin*2,data.horizonLine/2+
						  data.margin*3,fill=data.brown)