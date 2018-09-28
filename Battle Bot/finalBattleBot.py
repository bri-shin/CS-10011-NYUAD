
import network
import random,time,os
from random import randint
ans = 'start'

name = input ("Please enter your name")

# create boards
dispBoard, size, shipSize, mines = network.createBoards(name, True)
# hidboard, dispBoard, size, shipSize, mines = network.createBoards(name)


hints1 = [[-1,0],[1,0],[0,1],[0,-1],[-1,1],[-1,-1],[1,1],[1,-1]]	# mine neighbors
hints2 = [[-1,0],[1,0],[0,1],[0,-1]]								# boat neighbors
hintsVertical = [[-1,0],[1,0]]										# once boat is hit (vertical direction)
hintsHorizontal = [[0,1],[0,-1]]									# once boat is hit (horizontal direction)


hor = False
ver = False
directionChange=None
ultimateRow=None
ultimateCol=None

firstHit = False
secondHit = False 
thirdHit = False

hints2loop = 3

def checkRepeat(r,c):
	#returns True if it's a repeat
	if firstHitCoordinates[0][0] ==r and firstHitCoordinates[0][1] ==c:
		return True
	else:
		return False


# boat
def hint2guess(r,c, hints2loop):
	

	while True:
		if not checkRepeat(r+hints2[hints2loop][0], c+hints2[hints2loop][1]):
			return str(r+hints2[hints2loop][0]) +','+ str(c+hints2[hints2loop][1])
		hints2loop -=1 

hints1loop = 7

# mine
def hintguess(r,c):
	a = str(r+hints1[hints1loop][0]) +','+ str(c+hints1[hints1loop][1])
	return a


def opTurn():
	################################################################################
	# Opponents ##time to hit (waiting for opponent hit)
	# - either you will lose
	# - or opponent hit empty location or a ship location
	# - or opponent hit a mine 
	# 	- You get additional info about a nearby location to the opponent's ship
	################################################################################
	ansGot = network.receive()
	time.sleep(0.5)

	if ansGot == 'lost':			# All of my boat hit
		return True #break

	elif ansGot == None:			# Either one of by boat or nothing is hit
		return 'pass'

	else:
		ansGot = list(map(int,ansGot.split(',')))		# Mine is hit
		print (ansGot[0],ansGot[1], "is nearby location of the ship")
		return ansGot 


hintCoordinates = []
firstHitCoordinates = []
secondHitCoordinates = []
thirdHitCoordinates = []



	

hint = 0 # 0= no hints recieved


while True:

	lose = opTurn() # possible values: True, hint coordinates or pass
	if lose == True:	#When all of the boats are hit
		break

	if lose != 'pass':	# when mine is hit
		hintCoordinates.append(lose) #error fix with .append() instead of = ????
		hint += 1


		# win, XMorSpace, guess = ourTurn(hor, ver, hints2loop, directionChange)

		################################################################################
	# Your turn to hit
	# You will get back either ' ', 'x', 'M'
	#
	# need to make your own logic to come up with a string "r,c" to send to opponent
	################################################################################ 
	b = 'minus'
	c = 'subtract'


	if hint > 0 and hints1loop > -1 and firstHit == False:

		guess = hintguess(hintCoordinates[0][0],hintCoordinates[0][1]) #will return a guess to be used
		ans = network.send(guess)
		time.sleep(0.5)
		
		win = b
		XMorSpace= ans

	elif firstHit == True and secondHit == False and hints2loop > -1:    

		guess = hint2guess(firstHitCoordinates[0][0],firstHitCoordinates[0][1], hints2loop)

		ans = network.send(guess)
		#time.sleep(0.5)
		
		win =c
		XMorSpace=ans


	elif secondHit == True:

		print("we've already hit twice, we're inside the second elif")
		if (not hor) and (not ver):

			directionChange = False
			if firstHitCoordinates[0][0] == secondHitCoordinates[0][0]:
				hor = True
				ultimateRow = firstHitCoordinates[0][0]
				ultimateCol = min(int(firstHitCoordinates[0][1]), int(secondHitCoordinates[0][1]))

			else:
				ver = True
				ultimateCol = firstHitCoordinates[0][1]
				ultimateRow = min(int(firstHitCoordinates[0][0]),int(secondHitCoordinates[0][0]))
	
		if hor:
			print(directionChange)
			if not directionChange: #going left 
				ultimateCol-=1
				if 10>ultimateCol>=0:
					XMorSpace = network.send( str(ultimateRow)+','+str(ultimateCol))
					if ans != 'x':
						directionChange = True
						ultimateCol = max(int(firstHitCoordinates[0][1]), int(secondHitCoordinates[0][1]))

				else:
					directionChange = True
					ultimateCol = max(int(firstHitCoordinates[0][1]), int(secondHitCoordinates[0][1]))

			if directionChange:		
				ultimateCol+=1
				XMorSpace = network.send( str(ultimateRow)+','+str(ultimateCol))

		if ver:
			print(directionChange)
			if not directionChange: #going Up

				ultimateRow-=1
				if 10>ultimateRow>=0:
					ans = network.send( str(ultimateRow)+','+str(ultimateCol))
					if ans != 'x':
						directionChange = True
						ultimateRow = max(int(firstHitCoordinates[0][0]), int(secondHitCoordinates[0][0]))

				else:
					directionChange = True
					ultimateRow = max(int(firstHitCoordinates[0][0]), int(secondHitCoordinates[0][0]))

			if directionChange:		
				ultimateRow+=1
				XMorSpace = network.send( str(ultimateRow)+','+str(ultimateCol))

		win = 'meh'
		guess= str(ultimateRow)+','+str(ultimateCol)
		time.sleep(0.5)

	else:
		guess = (str(randint(0,9))+','+str(randint(0,9)))
		
		time.sleep(0.5)
		ans = network.send(guess)
		win= 'normal'
		XMorSpace = ans



	print(guess)
	if win == 'minus':
		hints1loop -= 1
	if win == 'subtract':
		hints2loop -= 1


	if XMorSpace == 'x' and firstHit != True:		# first boat is hit
		print("firstHit!")
		firstHit = True 
		guess = list(map(int,guess.split(',')))
		firstHitCoordinates.append(guess)
		
	
	elif XMorSpace == 'x' and firstHit == True and not secondHit:	#second boat is hit
		print("secondHit!")

		secondHit = True
		guess = list(map(int,guess.split(',')))
		secondHitCoordinates.append(guess)
		

	if XMorSpace=='win':	#winning statement
		print("we have actually won!")
		ans='win'
		break


# Printing final result
print(guess)
finalList=[]
if type(guess) is str: 
	finalList.append(list(map(int,guess.split(','))))
else:
	finalList.append(guess)

if ans == 'win':

	guessList = list(map(int,guess.split(',')))
	if (-1<int(finalList[0][0]) <10) and (-1<int(finalList[0][1])<10):
		dispBoard[guessList[0]][guessList[1]]='x'
	network.printBoard()
	print ("you have won the game")
else:
	network.printBoard()
	print ("you have lost the game")