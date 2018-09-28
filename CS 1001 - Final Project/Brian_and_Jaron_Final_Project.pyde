from random import randint
add_library('sound')
import time
import os
path = os.getcwd()

winSound = SoundFile(this, path+"/clap.wav")
loseSound = SoundFile(this, path+"/lose.wav")
titleSound = SoundFile(this, path+"/patience.mp3")
gameSound  = SoundFile(this, path+"/water.mp3")
bulletSound = SoundFile(this, path+"/bullet.mp3")
itemSound = SoundFile(this, path+"/nice.mp3")
class Begin:
    
    def mainGame(self):

        global asteroids
        
        for i in range(len(asteroids)):
            # time.sleep(2)
            if  ship.collide(asteroids[i]):
                loseSound.play()
                global stage
                stage = 5
            asteroids[i].display()
            noFill()
            asteroids[i].update()
            asteroids[i].border()
            
        for i in range(len(bullets)-1,-1,-1):
            bullets[i].display()
            bullets[i].update()
            if bullets[i].offscreen():
                bullets.remove(bullets[i])
            else:
                for a in range(len(asteroids)-1,-1,-1):
                    currentBullet = bullets[i]
                    if currentBullet.collide(asteroids[a]):
                        if asteroids[a].ar > 10:
                            
                            newAsteroids = asteroids[a].breakUp()
                            asteroids = asteroids + newAsteroids
        
                        asteroids.remove(asteroids[a])
                        bullets.remove(currentBullet)
                        break
        
        global items
        for i in range (len(items)-1,-1,-1):
            items[i].display()
            if ship.itemHit(items[i]):
                itemSound.play()
                newItems = items[i].update()
                items.remove(items[i])
            elif time.time() == 50:
                items.remove(items[i])
            

class Game:
    def __init__(self):
        self.bg = loadImage(path + "/background.jpg")
        self.intro = loadImage(path + "/sunset.jpg")
        self.play = loadImage(path + "/play.png")
        self.gameOver = loadImage(path + "/gameover.png")
        self.inst = loadImage(path + "/inst.png")
        self.arrow = loadImage(path + "/keys.png")
        self.shift = loadImage(path + "/shift.png")
        self.back = loadImage(path + "/return.png")
        self.about = loadImage(path + "/about.png")
        self.us = loadImage(path + "/us.png")
        self.home = loadImage(path + "/home.png")
        self.again = loadImage(path + "/again.png")
        self.points = 0
        self.timeLimit = 60
        self.se = loadImage(path+"/item.png")

    def timer(self):
        global stage
        if stage == 2:
            global timeStart
            timeStart = time.time()
            timeDiff = int(timeStart) -  int(currentTime)
            text((self.timeLimit - timeDiff),50,50)
            # text(self.timeStart,100,100)
            if int(self.timeLimit - timeDiff )  == 0:
                global gameSound
                gameSound.stop()
                winSound.play()
                stage = 5
        
    def display(self):
        image(game.bg,0,0,1280,720)
    
    def mainMenu(self):
        image(self.intro,0,0,3840,2160)
    
        for i in range(len(asteroids)):
            asteroids[i].display()
            asteroids[i].update()
            asteroids[i].border()
        
        textSize(25)
        fill(255,255,255)
        text("WELCOME TO",515,250)
        textSize(40)
        fill(255,255,255)
        text("BRIAN AND JARON'S 50 ASTEROIDS THREAT",190,350)
        image(self.play,510,520,180,40)
        image(self.inst, 510,570,180,40)
        image(self.about,510,620,180,40)
    def instScreen(self):
        pushStyle()
        background(0)
        image(self.se, 50, 100)
        textSize(20)
        text("You have 60 secons to shoot the asteroids", 50,50)
        text("Each asteroid is worth 10 points",50,80)
        text("= 100 POINTS!", 110, 130)
        image(self.arrow,500,150,200,132)
        textSize(40)
        text("BOOST", 538,134)
        text("Left Rotation",235,273)
        text("Right Rotation",720,273)
        fill(255)
        rect(0,350,1200,700)
        image(self.shift,460,380,300,250)
        fill(0)
        text("SHOOT BULLETS",452,680)
        image(self.back, 1100,600)
        popStyle()
    
    def endScreen(self):
        global gameSound
        gameSound.stop()
        image(self.gameOver,0,0,1200,700)
        # image(self.again, 970, 550, 180,40)
        image(self.home, 970, 600, 180,40)
        fill(255)
        textSize(40)
        text("Your Final Score:", 800,80)
        textSize(70)
        text(self.points, 920,160)
       
    def aboutUs(self):
        image(self.us,0,0,1200,700) 
        image(self.back, 1100,600)
    
    def pointUpdate(self):
        textSize(40)
        text(self.points, 1100,50)
         
    
################################################
        
class Ship:
    def __init__(self, xo, yo,xs,ys):
        self.position = PVector(xo,yo)
        self.r = 15
        self.theta = 0
        self.xo = xo
        self.yo = yo 
        self.xs = xs
        self.ys = ys
        self.velocity = PVector(0,0)
        self.isBoosting = False
        self.rotation = 0
        self.img = loadImage(path +"/rocket.png")
        
    def display(self):
        pushMatrix()
        translate(ship.position.x,ship.position.y)
        rotate(radians(ship.theta) + PI/2)
        strokeWeight(3)
        stroke(255)
        triangle(-self.r,self.r,self.r,self.r,0,-self.r)
        fill(156)
        smooth()
        popMatrix()
        
        
    def turn(self): #rotation
        self.theta += self.rotation
    
    def setRotation(self,angle): #rotation
        self.rotation = angle
        
    def border(self):
        if self.position.x > 1200 +self.r:
            self.position.x = -self.r
        elif self.position.x < -self.r:
            self.position.x = 1200 + self.r
            
        if self.position.y > 700 +self.r:
            self.position.y = -self.r
        elif self.position.y < -self.r:
            self.position.y = 700 + self.r
    
    def update(self): #going forward
        if self.isBoosting:
            self.boost()
        self.position.add(self.velocity) 
        self.velocity.mult(0.95)
    
    def boost(self): #boosting
        force = PVector.fromAngle(radians(self.theta)) 
        force.mult(0.3)
        self.velocity.add(force)
        
    
    def boosting(self, b): #boosting 
        self.isBoosting = b

    def collide(self,asteroid):
        d =  dist(self.position.x, self.position.y, asteroid.position.x, asteroid.position.y)
        if d < self.r + asteroid.ar:
            return True 
        else:
            return False
        
    def itemHit(self, item):
        distance = dist(self.position.x, self.position.y, item.position.x,  item.position.y)
        if distance < item.r:
            game.points +=100
            return True
        else:
            return False
#######################################

class Asteroid:
    def __init__(self, pos,  ar):
        if pos:
            self.position = pos.copy()
        else:  
            self.position = PVector(randint(0,1200),randint(0,700))
        
        if ar:
            self.ar = ar*0.5
        else:
            self.ar = randint(30,50)
        
        self.total = randint(5,15)
        self.offset = []
        for i in range(self.total):
            self.offset.append(randint(-self.ar//2, self.ar//2))
            # self.offset[i] = randint(-15,15)
        
        self. velocity = PVector.random2D()

        
    def display(self):
        pushMatrix()
        translate(self.position.x, self.position.y)
        strokeWeight(1)
        stroke(20)
        fill(99)
        # translate(self.position.x, self.position.y)
        beginShape()
        for i in range(self.total):
            angle = map(i,0, self.total,0, TWO_PI)
            x = (self.ar + self.offset[i]) * cos(angle)
            y = (self.ar + self.offset[i]) * sin(angle)
            vertex (x,y)
        endShape(CLOSE)
        popMatrix()
        #translate(randint(1,100),randint(1,100))
        #translate(self.position.x, self.position.y)
        
    def border(self):
        if self.position.x > 1200 +self.ar:
            self.position.x = -self.ar
        elif self.position.x < -self.ar:
            self.position.x = 1200 + self.ar
            
        if self.position.y > 700 +self.ar: 
            self.position.y = -self.ar
        elif self.position.y < -self.ar:
            self.position.y = 700 + self.ar
    def update(self):
        self.position.add(self.velocity)
        
    def breakUp(self):
        newA= []
        newA.append(Asteroid(self.position, self.ar))
        newA.append(Asteroid(self.position, self.ar))
        return  newA

#######################################

class Bullets():
    def __init__(self, shipPos,angle):
        self.position = PVector(shipPos.x, shipPos.y)
        self.velocity = PVector.fromAngle(radians(angle))
        self.velocity.mult(10)

        
    def display(self):
            
        pushStyle()
        stroke(255)
        strokeWeight(4)
        # ellipse(self.position.x,self.position.y,50,50)
        point(self.position.x,self.position.y)
        strokeWeight(1)
        popStyle()
        
    def update(self):
        self.position.add(self.velocity)
    
    def offscreen(self):
        if self.position.x > 1200 or self.position.x < 0:
            return True
        if self.position.y > 700 or self.position.y < 0:
            return True
        
        return False
            
    def collide(self,asteroid):
        distance = dist(self.position.x, self.position.y, asteroid.position.x,  asteroid.position.y)
        if distance < asteroid.ar:
            game.points +=10
            return True
        else:
            return False

        
class Item:
    def __init__(self):
        self.se = loadImage(path+"/item.png")
        self.position = PVector(randint(0,1200),randint(0,700))
        self.r = 50

    def display(self):
        x = self.position.x
        y =  self.position.y
        ellipse(x+25,y+25,self.r,self.r)
        image(self.se,x,y,self.r,self.r)
        
    def update(self):
        newI= []
        newI.append(Item())
        return  newI
                

game = Game()        
ship = Ship(600,350,10,14)
asteroids = []
bullets  = []
stage = 1
begin = Begin()
items = []


def setup():

    size (1200,700)
    game.display() 
    ship.display()   

    
    titleSound.play()
    for i in range(20):
        x = Asteroid(PVector(randint(10,1200),randint(10,700)), int(randint(15,50)))
        asteroids.append(x)
    
    for i in range(1):
        x = Item()
        items.append(x)
    
        
def draw():
    global asteroids
    game.display();
    if stage == 1:
        game.mainMenu()
    
    if stage == 2:
        clear()
        game.display()
        # image(ship.img,ship.position.x,ship.position.y,40,90)
        ship.display()    
        ship.turn()
        ship.update()
        ship.border()
        game.timer()
        game.pointUpdate()
        begin.mainGame()
    
        
    if stage == 3:
        game.instScreen()
        
    if stage == 4:
        game.aboutUs()
        
    if stage == 5:
        game.endScreen()
    
def keyReleased():
    if keyCode == UP:
        ship.boosting(False)

    ship.setRotation(0)
    

def keyPressed():

    if keyCode == UP:
        ship.boosting(True)
    if keyCode == LEFT:
        ship.setRotation(-7)
    if keyCode == RIGHT:
        ship.setRotation(7)
    if keyCode == SHIFT:
        bulletSound.play()
        x = Bullets(ship.position,ship.theta)
        bullets.append(x)

def mouseClicked():
    global stage
    if stage == 1 and 120<mouseX<160 and 100<mouseY<180:
        pass
    
    if stage ==1 and 510<mouseX<690 and 520<mouseY<560:
        global currentTime
        currentTime = time.time()
        timeStart = millis() //1000
        begin.mainGame()
        global asteroids
        asteroids = []
        global ship
        ship = Ship(600,350,10,14)
        titleSound.stop()
        gameSound.play()
        
        for i in range(50):
            x = Asteroid(PVector(randint(0,500) + randint(700,1200), randint(0,300) + randint(400,700)), int(randint(15,50)))
            asteroids.append(x)
        
        global items
        items = []
        
        for i in range(3):
            x = Item()
            items.append(x)
            
        stage = 2
    if stage == 1 and 510<mouseX<690 and 570<mouseY<610:
        stage = 3 
    if stage == 1 and 510<mouseX<690 and 620<mouseY<660:
        stage = 4
        
    if 970<mouseX<1170 and 600<mouseY<670:
        if stage == 5:
            titleSound.play()
        stage = 1
        game.points = 0 