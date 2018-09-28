#	Shin Seung Heon Brian - shs522

#	Import modules

import os
import time
import random


#	0. Parameters

numRow = 6
numCol = 7
board = []
numPlayers = 2
checkers = ["X","O"]
count = 0
numWin = 4
numRange = []


#	0.	Set Player

player1 = input("Name of Player 1:	")
player2 = input("Name of Player 2:	")

player_list = [player1,player2]

#	0.	Choosing Order

player_number = int(random.randint(0,1))
player_start = player_list[player_number]
print("\n"*3 + str(player_start) + " starts with the symbol 'O'" + "\n"*3)
time.sleep(2)

#	1. Create Board

for rows in range(numRow):
	tempList = []
	for cols in range(numCol):
		tempList.append(" ")
	board.append(tempList)

#	2. Printing Board

for cols in range(numCol):
	print("   " + str(cols), end = "")
print()

for rows in range(numRow):
	print (str(rows) + " ", end = "")
	for  cols in range(numCol):
		print(board[rows][cols] + " | ", end = "")
	print("\n " + "---+"*numCol)
print()


#	3. player1 choose column

while count < (numRow*numCol):

	try:
		if count % numPlayers == 1:
			player = int(input(player_list[abs(player_number-1)]+ " choose your column (0-6):\t"))
		else: 
			player = int(input(player_start + " choose your column (0-6):\t"))    


		if board[0][player] == " ":
			count += 1
			for row in range(numRow):
				board[0][player] = str(checkers[count%numPlayers])


		for cols in range(numCol):
			print("  " + str(cols), end=" ")
		print()

		for rows in range(numRow):
			print(str(rows) + " ", end = "")
			for cols in range(numCol):
				print(board[rows][cols] + " | ", end = "")
			print("\n " + "---+"*numCol)
		print()


	#	Fall

		for i in range(numRow-1):
			for r in range(numRow-2,-1,-1):
				for c in range(numCol):
					if board[r][player] != " " and board[r+1][player] == " ":
						board[r][player] = " "
						board[r+1][player] = str(checkers[count%numPlayers])


			os.system("Clear")


			for cols in range(numCol):
				print("  " + str(cols), end=" ")
			print()

			for rows in range(numRow):
				print(str(rows) + " ", end="")
				for cols in range(numCol):
					print(board[rows][cols] + " | ", end="")
				print("\n " + "---+" * numCol)
			print()

			time.sleep(0.3)

	except:
		print ("Invalid move!")

#	4. Evaluating winner
	
	# 	Horizontal Win
	for r in range(numRow):
		for c in range(numCol-3):
			xWin = 0
			oWin = 0
			for i in range(numWin):
				if board[r][c+i] == str(checkers[count%numPlayers]):
					xWin += 1
				if board[r][c+i] == str(checkers[count%numPlayers]):
					oWin += 1
			if xWin == numWin:
				print("Congratulations! " + player_start + " wins!")
				quit()
			elif oWin == numWin:
				print("Congratulations! " + player_list[abs(player_number-1)] + " wins!")		
				quit()

	#	Vertical Win
	for c in range(numCol):
		for r in range(numRow-3):
			xWin = 0
			oWin = 0
			for i in range(numWin):
				if board[r+i][c] == str(checkers[count%numPlayers]):
					xWin += 1
				if board[r+i][c] == str(checkers[count%numPlayers]):
					oWin += 1
			if xWin == numWin:
				print("Congratulations! " + player_start + " wins!")
				quit()
			elif oWin == numWin:
				print("Congratulations! " + player_list[abs(player_number-1)] + " wins!")		
				quit()

	#	Diagonal Win - 1



	for r in range(numRow-3):
		for c in range(numCol-3):
			xWin = 0
			oWin = 0
			for i in range(numWin):
				if board[r+i][c+i] == str(checkers[count%numPlayers]):
					xWin += 1
				if board[r+i][c+i] == str(checkers[count%numPlayers]):
					oWin += 1
			if xWin == 4:
				print("Congratulations! " + player_start + " wins!")
				quit()
			elif oWin == 4:
				print("Congratulations! " + player_list[abs(player_number-1)] + " wins!")		
				quit()


	#	Diagonal Win - 2

	for c in range(3,numCol):
		for r in range(numRow-3):
			xWin = 0
			oWin = 0
			for i in range(numWin):
				if board[r+i][c-i]== str(checkers[count%numPlayers]):
					xWin+=1
				if board[r+i][c-i]== str(checkers[count%numPlayers]):
					oWin+=1	
			if xWin == numWin:
				print("Congratulations! " + player_start + " wins!")
				quit()
			elif oWin == numWin:
				print("Congratulations! " + player_list[abs(player_number-1)] + " wins!")		
				quit()

print("TIE")
