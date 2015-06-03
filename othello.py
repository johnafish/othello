#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Othello Program
# John Fish
# Updated from May 29, 2015 - June 26, 2015
#
# Has both basic AI (random decision) as well as
# educated AI (minimax).
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Library import
from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy

#Tkinter setup
root = Tk()
screen = Canvas(root, width=500, height=600, background="#444",highlightthickness=0)
screen.pack()

class Board:
	def __init__(self):
		#White goes first (0 is white and player,1 is black and computer)
		self.player = 0
		
		#Initializing an empty board
		self.array = []
		for x in range(8):
			self.array.append([])
			for y in range(8):
				self.array[x].append(None)

		#Initializing center values
		self.array[3][3]="w"
		self.array[3][4]="b"
		self.array[4][3]="b"
		self.array[4][4]="w"

	#Updating the board to the screen
	def update(self):
		for x in range(8):
			for y in range(8):
				#Could replace the circles with images later, if I want
				if self.array[x][y]=="w":
					screen.create_oval(52+50*x,52+50*y,48+50*(x+1),48+50*(y+1),fill="white",outline="white")
				if self.array[x][y]=="b":
					screen.create_oval(52+50*x,52+50*y,48+50*(x+1),48+50*(y+1),fill="black",outline="black")
		#Draw the scoreboard and update the screen
		self.drawScoreBoard()
		screen.update()

	#Moves to position
	def boardMove(self,x,y):
		#Move and update screen
		self.array = move(self.array,x,y)
		
		
		#Switch Player
		self.player = 1-self.player
		self.update()
		
		#Check if player must pass
		self.passTest()
		self.update()

		#If the computer is AI, make a move
		if self.player==1:
			self.array = self.minimax(self.array,3,1)[1]
			self.player = 1-self.player
			self.update()
			

	#METHOD: Draws scoreboard to screen
	def drawScoreBoard(self):
		#Deleting prior score elements
		screen.delete("score")

		#Scoring based on number of tiles
		player_score = 0
		computer_score = 0
		for x in range(8):
			for y in range(8):
				if self.array[x][y]=="w":
					player_score+=1
				elif self.array[x][y]=="b":
					computer_score+=1

		if self.player==0:
			player_colour = "green"
			computer_colour = "gray"
		else:
			player_colour = "gray"
			computer_colour = "green"

		screen.create_oval(5,540,25,560,fill=player_colour,outline=player_colour)
		screen.create_oval(380,540,400,560,fill=computer_colour,outline=computer_colour)

		#Pushing text to screen
		screen.create_text(30,550,anchor="w", tags="score",font=("Consolas", 50),fill="white",text=player_score)
		screen.create_text(400,550,anchor="w", tags="score",font=("Consolas", 50),fill="black",text=computer_score)

	#FUNCTION: Checks if a move is valid: returns True or False
	def valid(self,x,y):
		#Sets player colour
		if self.player==0:
			colour="w"
		else:
			colour="b"
			
		#If there's already a piece there, it's an invalid move
		if self.array[x][y]!=None:
			return False

		else:
			#Generating the list of neighbours
			neighbour = False
			neighbours = []
			for i in range(max(0,x-1),min(x+2,8)):
				for j in range(max(0,y-1),min(y+2,8)):
					if self.array[i][j]!=None:
						neighbour=True
						neighbours.append([i,j])
			#If there's no neighbours, it's an invalid move
			if not neighbour:
				return False
			else:
				#Iterating through neighbours to determine if at least one line is formed
				valid = False
				for neighbour in neighbours:

					neighX = neighbour[0]
					neighY = neighbour[1]
					
					#If the neighbour colour is equal to your colour, it doesn't form a line
					#Go onto the next neighbour
					if self.array[neighX][neighY]==colour:
						continue
					else:
						#Determine the direction of the line
						deltaX = neighX-x
						deltaY = neighY-y
						tempX = neighX
						tempY = neighY

						while 0<=tempX<=7 and 0<=tempY<=7:
							#If an empty space, no line is formed
							if self.array[tempX][tempY]==None:
								break
							#If it reaches a piece of the player's colour, it forms a line
							if self.array[tempX][tempY]==colour:
								valid=True
								break
							#Move the index according to the direction of the line
							tempX+=deltaX
							tempY+=deltaY
				return valid

	#METHOD: Test if player must pass: if they do, switch the player
	def passTest(self):
		mustPass = True
		for x in range(8):
			for y in range(8):
				if self.valid(x,y):
					mustPass=False
		if mustPass:
			self.player = 1-self.player

	#METHOD: Stupid AI - Chooses a random move
	def dumbMove(self):
		#Generates all possible moves
		choices = []
		for x in range(8):
			for y in range(8):
				if self.valid(x,y):
					choices.append([x,y])
		#Chooses a random move, moves there
		dumbChoice = choice(choices)
		self.boardMove(dumbChoice[0],dumbChoice[1])

	#METHOD: Not so stupid AI - Chooses a move based on what will get it the most pieces next turn
	def slightlyLessDumbMove(self):
		#Generates all possible choices and boards corresponding to those
		boards = []
		choices = []
		for x in range(8):
			for y in range(8):
				if self.valid(x,y):
					test = move(self.array,x,y)
					boards.append(test)
					choices.append([x,y])

		#Determines the best score based on the prior generated boards and a "Dumb" Heuristic: dumbScore()
		bestScore = -float("inf")
		bestIndex = 0
		for i in range(len(boards)):
			score= dumbScore(boards[i],self.player)
			if score>bestScore:
				bestIndex=i
				bestScore = score
		#Move to the best location based on dumbScore()
		self.boardMove(choices[bestIndex][0],choices[bestIndex][1])

	#METHOD: Actually Decent AI - Choose a move based on a simple heuristic
	#Same as slightlyLessDumbMove() just uses slightlyLessDumbScore()
	def decentMove(self):
		#Generates all possible choices and boards corresponding to those
		boards = []
		choices = []
		for x in range(8):
			for y in range(8):
				if self.valid(x,y):
					test = move(self.array,x,y)
					boards.append(test)
					choices.append([x,y])

		bestScore = -float("inf")
		bestIndex = 0
		#Determines the best score based on the prior generated boards and a "Meh" Heuristic: slightlyLessDumbScore()
		for i in range(len(boards)):
			score= slightlyLessDumbScore(boards[i],self.player)
			if score>bestScore:
				bestIndex=i
				bestScore = score
		#Move to the best location based on slightlyLessDumbScore()
		self.boardMove(choices[bestIndex][0],choices[bestIndex][1])


	#This will contain minimax... later.
	def minimax(self, node, depth, maximizing):
		boards = []
		choices = []

		for x in range(8):
			for y in range(8):
				if self.valid(x,y):
					test = move(node,x,y)
					boards.append(test)
					choices.append([x,y])

		if depth==0 or len(choices)==0:
			return ([decentHeuristic(node,1-maximizing),node])

		if maximizing:
			bestValue = -float("inf")
			bestBoard = []
			for board in boards:
				val = self.minimax(board,depth-1,0)[0]
				if val>bestValue:
					bestValue = val
					bestBoard = board
			return ([bestValue,bestBoard])

		else:
			bestValue = float("inf")
			bestBoard = []
			for board in boards:
				val = self.minimax(board,depth-1,1)[0]
				if val<bestValue:
					bestValue = val
					bestBoard = board
			return ([bestValue,bestBoard])


#FUNCTION: Returns a board after making a move according to Othello rules
#Assumes the move is valid
def move(passedArray,x,y):
	#Must copy the passedArray so we don't alter the original
	array = deepcopy(passedArray)
	#Set colour and set the moved location to be that colour
	if board.player==0:
		colour = "w"
		
	else:
		colour="b"
	array[x][y]=colour
	
	#Determining the neighbours to the square
	neighbours = []
	for i in range(max(0,x-1),min(x+2,8)):
		for j in range(max(0,y-1),min(y+2,8)):
			if array[i][j]!=None:
				neighbours.append([i,j])
	
	#Which tiles to convert
	convert = []

	#For all the generated neighbours, determine if they form a line
	#If a line is formed, we will add it to the convert array
	for neighbour in neighbours:
		neighX = neighbour[0]
		neighY = neighbour[1]
		#Check if the neighbour is of a different colour - it must be to form a line
		if array[neighX][neighY]!=colour:
			#The path of each individual line
			path = []
			
			#Determining direction to move
			deltaX = neighX-x
			deltaY = neighY-y

			tempX = neighX
			tempY = neighY

			#While we are in the bounds of the board
			while 0<=tempX<=7 and 0<=tempY<=7:
				path.append([tempX,tempY])
				value = array[tempX][tempY]
				#If we reach a blank tile, we're done and there's no line
				if value==None:
					break
				#If we reach a tile of the player's colour, a line is formed
				if value==colour:
					#Append all of our path nodes to the convert array
					for node in path:
						convert.append(node)
					break
				#Move the tile
				tempX+=deltaX
				tempY+=deltaY
				
	#Convert all the appropriate tiles
	for node in convert:
		array[node[0]][node[1]]=colour

	return array


#Method for drawing the gridlines
def drawGridBackground(outline=False):
	#If we want an outline on the board then draw one
	if outline:
		screen.create_rectangle(50,50,450,450,outline="#222")

	#Drawing the intermediate lines
	for i in range(7):
		lineShift = 50+50*(i+1)

		#Horizontal line
		screen.create_line(50,lineShift,450,lineShift,fill="#222")

		#Vertical line
		screen.create_line(lineShift,50,lineShift,450,fill="#222")

	screen.update()


#Simple heuristic. Compares number of each tile.
def dumbScore(array,player):
	score = 0
	#Set player and opponent colours
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"
	#+1 if it's player colour, -1 if it's opponent colour
	for x in range(8):
		for y in range(8):
			if array[x][y]==colour:
				score+=1
			elif array[x][y]==opponent:
				score-=1
	return score

#Less simple but still simple heuristic. Weights corners and edges as more
def slightlyLessDumbScore(array,player):
	score = 0
	#Set player and opponent colours
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"
	#Go through all the tiles	
	for x in range(8):
		for y in range(8):
			#Normal tiles worth 1
			add = 1
			#Edge tiles worth 3
			if (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
				add=3
			#Corner tiles worth 5
			elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
				add = 5
			#Add or subtract the value of the tile corresponding to the colour
			if array[x][y]==colour:
				score+=add
			elif array[x][y]==opponent:
				score-=add
	return score

def decentHeuristic(array,player):
	score = 0
	#Set player and opponent colours
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"
	#Go through all the tiles	
	for x in range(8):
		for y in range(8):
			#Normal tiles worth 1
			add = 1
			#Adjacent to corners are worth -3
			if (x==0 and (y==1 or y==6)) or (x==7 and (y==1 or y==6)) or (x==1 and (0<=y<=1 or 6<=y<=7)) or (x==7 and (0<=y<=1 or 6<=y<=7)):
				add=-3
			#Edge tiles worth 3
			elif (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
				add=3
			#Corner tiles worth 15
			elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
				add = 15
			#Add or subtract the value of the tile corresponding to the colour
			if array[x][y]==colour:
				score+=add
			elif array[x][y]==opponent:
				score-=add
	return score
#When mouse moves, we want a green highlight to appear for valid moves, red for invalid
def mouseMovementHandle(event):
	#Is it the player's turn?
	if board.player==0:
		#Delete the other highlight(s)
		screen.delete("highlight")

		#Determine the grid index for where the mouse is
		xMouse = event.x
		yMouse = event.y
		x = int((event.x-50)/50)
		y = int((event.y-50)/50)
		#If we're inside the board, test validity
		if 0<=x<=7 and 0<=y<=7:
			if board.valid(x,y):
				#Create a green highlight if it's a valid move
				screen.create_oval(52+50*x,52+50*y,48+50*(x+1),48+50*(y+1),tags="highlight",fill="green",outline="green")
			else:
				#Create a red highlight if it's a valid move
				screen.create_oval(52+50*x,52+50*y,48+50*(x+1),48+50*(y+1),tags="highlight",fill="red",outline="red")

#When the user clicks, if it's a valid move, make the move
def clickHandle(event):
	#Is it the player's turn?
	if board.player==0:
		#Delete the highlights
		screen.delete("highlight")
		#Determine the grid index for where the mouse was clicked
		xMouse = event.x
		yMouse = event.y
		x = int((event.x-50)/50)
		y = int((event.y-50)/50)
		#If the click is inside the bounds and the move is valid, move to that location
		if 0<=x<=7 and 0<=y<=7:
			if board.valid(x,y):
				board.boardMove(x,y)

#Draw the background
drawGridBackground()

#Create the board and update it
board = Board()
board.update()

#Binding, setting
screen.bind("<Motion>", mouseMovementHandle)
screen.bind("<Button-1>", clickHandle)
screen.focus_set()

#Run forever
root.mainloop()