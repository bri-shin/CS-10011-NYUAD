add_library('sound')
import os, random
path = os.getcwd()

winList = []
for i in range(16):
    winList.append(i)

row = 4
col = 4
finish = False

class Tile:

    def __init__(self, img, xPos, yPos, num):
        self.img = img
        self.leng = 100
        self.xPos = xPos
        self.yPos = yPos
        self.num = num
        
        
    def display(self):
        image(self.img, self.xPos * self.leng, self.yPos * self.leng)

class Puzzle:

    def __init__(self, row, col, tileList):
        self.row = row
        self.col = col
        self.tileList = tileList

    


    def display(self):
        for row in self.tileList:
            for block in row:
                block.display()
                
    def win(self):
        numList = []
        for row in tileList:
            for element in row:
                theNum = element.num
                numList.append(theNum)
        print(numList)    
        
        if numList == winList:

            return True
            
        else:
            return False
                
    def mix(self, startX, startY):
        x = startX
        y = startY
        for i in range(200):
            choiceList = []
            #LEFT
            if myPuzzle.tileList[x][y].xPos>0:
                choiceList.append('left')
                
            #RIGHT 
            if myPuzzle.tileList[x][y].xPos < 3: #right swtich
                choiceList.append('right')
            #UP
            if myPuzzle.tileList[x][y].yPos > 0: #up swtich
                choiceList.append('up')
        
            #DOWN
            if myPuzzle.tileList[x][y].yPos < 3: #down swtich
                choiceList.append('down')
                
            random.shuffle(choiceList)
            choice = choiceList[0]
            
            if choice == 'left':
                self.leftSwitch(x, y)
                x = x-1
            if choice == 'right':
                self.rightSwitch(x, y)
                x = x+1
            if choice == 'up':
                self.upSwitch(x, y)
                y = y-1
            if choice == 'down':
                self.downSwitch(x, y)
                y = y+1
            
        

    def upSwitch(self, x, y):
        n1 = self.tileList[x][y]
        n2 = self.tileList[x][y-1]
        n1x = self.tileList[x][y].xPos
        n1y = self.tileList[x][y].yPos
        n2x = self.tileList[x][y-1].xPos
        n2y = self.tileList[x][y-1].yPos
        self.tileList[x][y] = n2
        self.tileList[x][y-1] = n1 
        self.tileList[x][y].xPos = n1x
        self.tileList[x][y].yPos = n1y
        self.tileList[x][y-1].xPos = n2x
        self.tileList[x][y-1].yPos = n2y
            
    def downSwitch(self, x, y):
        n1 = self.tileList[x][y]
        n2 = self.tileList[x][y+1]
        n1x = self.tileList[x][y].xPos
        n1y = self.tileList[x][y].yPos
        n2x = self.tileList[x][y+1].xPos
        n2y = self.tileList[x][y+1].yPos
        
        self.tileList[x][y] = n2
        self.tileList[x][y+1] = n1 
        self.tileList[x][y].xPos = n1x
        self.tileList[x][y].yPos = n1y
        self.tileList[x][y+1].xPos = n2x
        self.tileList[x][y+1].yPos = n2y
        
        
    
    def rightSwitch(self, x, y):
        n1 = self.tileList[x][y]
        n2 = self.tileList[x+1][y]
        n1x = self.tileList[x][y].xPos
        n1y = self.tileList[x][y].yPos
        n2x = self.tileList[x+1][y].xPos
        n2y = self.tileList[x+1][y].yPos
        
        self.tileList[x][y] = n2
        self.tileList[x+1][y] = n1 
        self.tileList[x][y].xPos = n1x
        self.tileList[x][y].yPos = n1y
        self.tileList[x+1][y].xPos = n2x
        self.tileList[x+1][y].yPos = n2y
    
        
    def leftSwitch(self, x, y):
        n1 = self.tileList[x][y]
        n2 = self.tileList[x-1][y]
        n1x = self.tileList[x][y].xPos
        n1y = self.tileList[x][y].yPos
        n2x = self.tileList[x-1][y].xPos
        n2y = self.tileList[x-1][y].yPos
        
        self.tileList[x][y] = n2
        self.tileList[x-1][y] = n1 
        self.tileList[x][y].xPos = n1x
        self.tileList[x][y].yPos = n1y
        self.tileList[x-1][y].xPos = n2x
        self.tileList[x-1][y].yPos = n2y
        


def setup():
    global row
    global col
    global tileList
    global gameSound
    global endSound

    tileList = []
    for i in range(row):
        tmp = []
        for j in range(col):
            cnt = j*row + i 
            numboi = i*row +j
            img = loadImage(path + "/" + str(cnt) + ".png")
            tmp.append(Tile(img, 0, 0, numboi))
        tileList.append(tmp)

    i = 0
    for x in range(row):
        for y in range(col):
            tileList[x][y].xPos = x
            tileList[x][y].yPos = y
            i += 1
        
    size(400, 400)
    # background(255, 0, 0)
    global myPuzzle
    myPuzzle = Puzzle(4, 4, tileList)
    myPuzzle.mix(3,3)
    gameSound = SoundFile(this, path+"/banana.mp3")
    endSound = SoundFile(this, path+"/tada.mp3")
    gameSound.play()


def draw():

    if finish:
        lastImg = loadImage(path + "/banana.png")
        image(lastImg,-5,-5,415,415)
        gameSound.stop()
    else:
        myPuzzle.display()



def mouseClicked():
    x = mouseX // 100
    y = mouseY // 100



    if myPuzzle.tileList[x][y].num != 15:

        #LEFT
        if myPuzzle.tileList[x][y].xPos>0:
            if myPuzzle.tileList[x-1][y].num == 15:
                myPuzzle.leftSwitch(x, y)
            
        #RIGHT 
        if myPuzzle.tileList[x][y].xPos < 3: #right swtich
            if myPuzzle.tileList[x+ 1][y].num == 15:
                myPuzzle.rightSwitch(x, y)
        
        #UP
        if myPuzzle.tileList[x][y].yPos > 0: #up swtich
            if myPuzzle.tileList[x][y-1].num == 15:
                myPuzzle.upSwitch(x, y)
    
        #DOWN
        if myPuzzle.tileList[x][y].yPos < 3: #down swtich
            if myPuzzle.tileList[x][y+1].num == 15:
                myPuzzle.downSwitch(x, y)
    
    myPuzzle.display()
    if myPuzzle.win():
        global finish
        finish = True
        endSound.play()