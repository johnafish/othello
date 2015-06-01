#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Othello Program
# John Fish
# Updated from May 29, 2015 - June 26, 2015
#
# Has both basic AI (random decision) as well as
# educated AI (minimax).
#
# Supports player vs. player play also.
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
				if self.array[x][y]=="w":
					screen.create_oval(52+50*x,52+50*y,48+50*(x+1),48+50*(y+1),fill="white",outline="white")
				if self.array[x][y]=="b":
					screen.create_oval(52+50*x,52+50*y,48+50*(x+1),48+50*(y+1),fill="black",outline="black")
		self.drawScoreBoard()
		screen.update()

	#Moves to position
	def boardMove(self,x,y):
		self.array = move(self.array,x,y)
		self.update()
		self.player = 1-self.player
		self.passTest()
		if self.player==1:
			sleep(0.3)
			self.slightlyLessDumbMove()
		
	def drawScoreBoard(self):
		screen.delete("score")
		player_score = 0
		computer_score = 0
		for x in range(8):
			for y in range(8):
				if self.array[x][y]=="w":
					player_score+=1
				elif self.array[x][y]=="b":
					computer_score+=1
		screen.create_text(0,550,anchor="w", tags="score",font=("Consolas", 50),fill="white",text=player_score)
		screen.create_text(500,550,anchor="e", tags="score",font=("Consolas", 50),fill="black",text=computer_score)

	def valid(self,x,y):
		if self.player==0:
			colour="w"
		else:
			colour="b"

		if self.array[x][y]!=None:
			return False
		else:
			neighbour = False
			neighbours = []
			for i in range(max(0,x-1),min(x+2,8)):
				for j in range(max(0,y-1),min(y+2,8)):
					if self.array[i][j]!=None:
						neighbour=True
						neighbours.append([i,j])

			if not neighbour:
				return False
			else:
				valid = False
				for neighbour in neighbours:

					neighX = neighbour[0]
					neighY = neighbour[1]

					if self.array[neighX][neighY]==colour:
						continue
					else:
						deltaX = neighX-x
						deltaY = neighY-y
						tempX = neighX
						tempY = neighY

						while 0<=tempX<=7 and 0<=tempY<=7:
							if self.array[tempX][tempY]==None:
								break
							if self.array[tempX][tempY]==colour:
								valid=True
								break
							tempX+=deltaX
							tempY+=deltaY
				return valid

	def passTest(self):
		mustPass = True
		for x in range(8):
			for y in range(8):
				if self.valid(x,y):
					mustPass=False
					break
		if mustPass:
			self.player = 1-self.player

	def dumbMove(self):
		choices = []
		for x in range(8):
			for y in range(8):
				if self.valid(x,y):
					choices.append([x,y])
		dumbChoice = choice(choices)
		self.boardMove(dumbChoice[0],dumbChoice[1])

	def slightlyLessDumbMove(self):
		boards = []
		choices = []
		for x in range(8):
			for y in range(8):
				if self.valid(x,y):
					test = move(self.array,x,y)
					boards.append(test)
					choices.append([x,y])

		bestScore = -32
		bestIndex = 0
		for i in range(len(boards)):
			score= dumbScore(boards[i])
			if score>bestScore:
				bestIndex=i
				bestScore = score
		self.boardMove(choices[bestIndex][0],choices[bestIndex][1])

	def decentMove(self):
		boards = []
		choices = []
		for x in range(8):
			for y in range(8):
				if self.valid(x,y):
					test = move(self.array,x,y)
					boards.append(test)
					choices.append([x,y])

		bestScore = -32
		bestIndex = 0
		for i in range(len(boards)):
			score= slightlyLessDumbScore(boards[i])
			if score>bestScore:
				bestIndex=i
				bestScore = score
		self.boardMove(choices[bestIndex][0],choices[bestIndex][1])


def move(passedArray,x,y):
	array = deepcopy(passedArray)
	if board.player==0:
		array[x][y]="w"
		colour = "w"
	else:
		array[x][y]="b"
		colour = "b"

	#Determining the neighbours to the square
	neighbours = []
	for i in range(max(0,x-1),min(x+2,8)):
		for j in range(max(0,y-1),min(y+2,8)):
			if array[i][j]!=None:
				neighbours.append([i,j])
	
	#Which tiles to convert
	convert = []

	for neighbour in neighbours:
		neighX = neighbour[0]
		neighY = neighbour[1]

		if array[neighX][neighY]!=colour:
			
			path = []

			deltaX = neighX-x
			deltaY = neighY-y

			tempX = neighX
			tempY = neighY

			while 0<=tempX<=7 and 0<=tempY<=7:
				path.append([tempX,tempY])
				value = array[tempX][tempY]
				if value==None:
					break
				if value==colour:
					for node in path:
						convert.append(node)
					path=[]
					break

				tempX+=deltaX
				tempY+=deltaY

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
def dumbScore(array):
	score = 0
	colour="b"
	opponent="w"
	for x in range(8):
		for y in range(8):
			if array[x][y]==colour:
				score+=1
			elif array[x][y]==opponent:
				score-=1
	return score

def slightlyLessDumbScore(array):
	score = 0
	colour="b"
	opponent="w"
	for x in range(8):
		for y in range(8):
			add = 1
			if (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
				add=3
			elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
				add = 5
			if array[x][y]==colour:
				score+=add
			elif array[x][y]==opponent:
				score-=add
	return score

def mouseMovementHandle(event):
	if board.player==0:
		screen.delete("highlight")
		xMouse = event.x
		yMouse = event.y
		x = int((event.x-50)/50)
		y = int((event.y-50)/50)
		if 0<=x<=7 and 0<=y<=7:
			if board.valid(x,y):
				screen.create_oval(52+50*x,52+50*y,48+50*(x+1),48+50*(y+1),tags="highlight",fill="green",outline="green")

def clickHandle(event):
	if board.player==0:
		screen.delete("highlight")
		xMouse = event.x
		yMouse = event.y
		x = int((event.x-50)/50)
		y = int((event.y-50)/50)
		if 0<=x<=7 and 0<=y<=7:
			if board.valid(x,y):
				board.boardMove(x,y)
board = Board()
board.update()


drawGridBackground()

screen.bind("<Motion>", mouseMovementHandle)
screen.bind("<Button-1>", clickHandle)
screen.focus_set()
root.mainloop()