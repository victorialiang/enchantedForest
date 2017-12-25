import random

# rgbString helper function from 112 notes
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def getLegalMoves(data):
	legalMoves = list()
	board = data.maze.realBoard
	rows = len(board)
	cols = len(board[0])
	currentRow = data.position[0]
	currentCol = data.position[1]
	for direction in [data.NORTH,data.SOUTH,data.EAST,data.WEST]:
		dRow = direction[0]
		dCol = direction[1]
		# data.lastPosition = (None,None) when it is the first move
		if ((data.lastPosition == (None,None) or 
			data.lastPosition != (currentRow+dRow,currentCol+dCol)) 
			and currentRow+dRow >= 0 and currentRow+dRow < rows and 
			currentCol+dCol>=0 and currentCol+dCol<cols 
			and board[currentRow+dRow][currentCol+dCol]):
			legalMoves.append(direction)
	return legalMoves

def getRandomPosition(data):
	position = (None,None)
	rows = len(data.maze.realBoard)//2
	cols = len(data.maze.realBoard[0])//2
	isLegal = False
	while (isLegal != True):
		row = random.randint(0,rows-1)
		col = random.randint(0,cols-1)
		isLegal = data.maze.realBoard[row][col]
		if (data.position == (row,col)):
			isLegal = False
		position = (row,col)
	return position

# Helper functions maxItemLength and print2dList taken from notes:

def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows = len(a)
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(cols):
            if (col > 0): print(", ", end="")
            # The next 2 lines print a[row][col] with the given fieldWidth
            formatSpec = "%" + str(fieldWidth) + "s"
            print(formatSpec % str(a[row][col]), end="")
        print(" ]", end="")
    print("]")


# The random maze generation is largely referenced from here: https://www.cs.cmu.edu/~112/notes/maze-solver.py
# I changed it by reorganizing the structure to use a Maze and Node class
# The drawing part is entirely my own

class Maze(object):
	def __init__(self,data,rows=5,cols=5):
		self.rows = rows
		self.cols = cols
		self.board = [ [0] * cols for row in range(rows)]
		self.mazeX = data.width*3/4
		self.mazeY = data.margin
		#data.margin = 20
		self.width = data.width/4 - data.margin
		self.height = self.width

	def makeBoard(self):
		counter = 0
		for row in range(self.rows):
			for col in range(self.cols):
				self.board[row][col] = Node(counter)
				counter += 1
		self.connectNodes()
		# make real board
		self.realBoard = [[False for row in range(2*self.rows-1)] 
		for col in range(2*self.cols-1)] 
		for row in range(len(self.board)):
			for col in range(len(self.board[0])):
				self.realBoard[row*2][col*2]=True
				if (self.board[row][col].east):
					self.realBoard[row*2][col*2+1] = True
				if (self.board[row][col].south):
					self.realBoard[row*2+1][col*2] = True
		#print2dList(self.realBoard)

	def flipCoin(self):
		return random.choice([True, False])

	def connectNodes(self):
		(rows,cols) = (len(self.board), len(self.board[0]))
		for i in range (rows*cols-1):
			self.makeBridges()

	def makeBridges(self):
		(rows,cols) = (len(self.board),len(self.board[0]))
		while True: # doesn't break until a bridge is made
			(row,col) = (random.randint(0,self.rows-1), 
				random.randint(0,self.cols-1))
			start = self.board[row][col]
			if self.flipCoin(): #try to go east
			    if col==cols-1: continue
			    target = self.board[row][col+1]
			    if start.num==target.num: continue
			    #the bridge is valid, so 1. connect them and 2. rename them
			    start.east = True
			    self.renameNodes(start,target)
			else: #try to go south
			    if row==rows-1: continue
			    target = self.board[row+1][col]
			    if start.num==target.num: continue
			    #the bridge is valid, so 1. connect them and 2. rename them
			    start.south = True
			    self.renameNodes(start,target)
			#only got here if a bridge was made
			return

	def renameNodes(self,node1,node2):
	    n1,n2 = node1.num,node2.num
	    lo,hi = min(n1,n2),max(n1,n2)
	    for row in self.board:
	        for node in row:
	            if node.num==hi: node.num=lo
	            # if nodes have the same number, they are connected

	def drawMaze(self,canvas,data):
		# draw board
		mazeColor = data.skyGradient[len(data.skyGradient)//2]
		canvas.create_rectangle(self.mazeX,self.mazeY,self.mazeX + self.width,
								self.mazeY+self.height,
								fill=rgbString(mazeColor[0],mazeColor[1],mazeColor[2]),
								outline=rgbString(mazeColor[0],mazeColor[1],mazeColor[2]))
		# draw nodes and connections to nodes
		self.drawPath2(canvas,data)

	def drawPath2(self,canvas,data):
		mazeColor = data.skyGradient[0]
		color = rgbString(mazeColor[0],mazeColor[1],mazeColor[2])

		self.blockWidth = self.width/(2*self.rows+1)
		numRows = len(data.maze.realBoard)
		numCols = len(data.maze.realBoard[0])
		for row in range(len(self.realBoard)):
			for col in range(len(self.realBoard[0])):
				if (self.realBoard[row][col] == True):
					# print("hi")
					top = self.mazeY + self.blockWidth*(row+1)
					left = self.mazeX + self.blockWidth*(col+1)
					bottom = top + self.blockWidth
					right = left + self.blockWidth
					#print("tpbr = %s %s %s %s" % (top,left,bottom,right))
					
					
					if (row == numRows-1 and col == numCols-1):
						canvas.create_rectangle(left,top,right,bottom,
							fill=data.colors[10],outline=data.colors[10])
					else:
						canvas.create_rectangle(left,top,right,bottom,
							fill=data.brown,outline=data.colors[0])
					if (data.position[0]==row and data.position[1]==col):
						canvas.create_rectangle(left,top,right,bottom,
							fill=data.red,outline=data.red)

		#self.drawPlayer(canvas,data)

	def drawPlayer(self,canvas,data):
		(row,col) = data.position
		top = self.mazeY + self.blockWidth * col
		left = self.mazeX + self.blockWidth * row
		bottom = top + self.blockWidth
		right = left + self.blockWidth
		canvas.create_rectangle(left,top,right,bottom,fill="#5D3E3E")


class Node(object):
	def __init__(self,num,east=False,south=False):
		self.num = num
		self.east = east
		self.south = south