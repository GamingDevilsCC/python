#Summative

#make a game that's similar to plants vs zombies
#The "zombies" going in the pathway are the non enviormentally recycled electronics
#What the user has to do is place good guys (recyclers) on the pathways, which recycles the electornic waste from reaching the end of the production plant. (end of the path)
#the enemies will go inside them (colide) and they lose health, but if they reach the end of the path sucessfully then the player loses health.
#each stage will use randomness to decide which enemies (e-waste) will be placed / go through the pathway?

from pygame import*
import os
import random

#this is under development. Once done, the user is able to see his score and other player's score, and add his score to the scoreboard.
def scoreboardMenu():
    global scoreboardList
    numFile = open("scoreboard.dat", "r")
    while True:
        text = numFile.readline()
        #rstrip removes the newline character read at the end of the line
        text = text.rstrip("\n")
        if text=="": 
            break
        text = text.split(",")
        scoreboardList.append(text)
    numFile.close()    
    draw.rect(screen, BLACK, (0, 0, 1000, 700))
    

def gameMenu(): #game
    global roundStarted
    global generateEnemies
    global greenCoins
    #track
    draw.rect(screen, BLACK, (0, 0, 1000, 700))
    draw.rect(screen, WHITE, (0, 200, 1000, 100)) #top track
    draw.rect(screen, WHITE, (0, 300, 1000, 100)) #middle track
    draw.rect(screen, WHITE, (0, 400, 1000, 100)) #bottom track
    
    #health
    playerHealthBar()
    startButton() #to start the round and generate enemies
    
    #coins
    coinText = smallFont.render(str(greenCoins), 1, WHITE)
    screen.blit(coinText, Rect(900, 30, 0, 0)) #player health text
    
    #buy recycler button
    draw.rect(screen, GREEN, (450, 600, 100, 50))
    
    #the generate the e-waste and if the round has started, show the e-waste. Show recyclers regardless if round has started or not. 
    if generateEnemies:
        #tier 1 e-waste spawns every round
        enemyTier1(roundNumber)
        
        #tier 2 e-waste has a 50% chance of spawning
        spawnTier2 = random.choice([1, 0])
        if spawnTier2 == 1: #50% chance
            enemyTier2(roundNumber)
        
        #tier 4 e-waste has a 25% chance of spawning
        spawnTier3 = random.choice([1, 0, 0, 0]) #random.choice looks more organized, so lets use it
        if spawnTier3 == 1:
            enemyTier3(roundNumber)
        generateEnemies = False #set it to false right after generating enemies, so on the next loop it doesn't generate even more.
        greenCoins += 10 #at the start of every round, give the player a 10 coin bonus.
        print("10 coin bonus")
    
    if roundStarted:
        enemiesMoving()
    recycler()
    
    #time.wait(5)
    display.flip()
    userEvents()    
    
#animation for the e-waste moving through the screen.
def enemiesMoving(): #will have feature to randomly select different levels of enemies soon.
    global playerHealth
    global recyclerX
    global eWasteX
    global greenCoins
    
    #electronic waste          
    for eWaste in range(len(eWasteX)): #how many e-waste enemies there are. nested loop because of enemyHealth requiring information from machine
        if eWasteStatus[eWaste] == 1: #checks to see if the enemy is alive.
            draw.rect(screen, eWasteColor[eWaste], (eWasteX[eWaste], eWasteY[eWaste], 50, 50)) #screen, color, (x, y, w, l)
            enemyHealthText = smallFont.render(str(eWasteHealth[eWaste]), 1, WHITE)
            screen.blit(enemyHealthText, Rect(eWasteX[eWaste] + 5, eWasteY[eWaste] + 5, 0, 0)) #e-waste health text
            eWasteX[eWaste] += eWasteSpeed[eWaste] #increase the x position of e-waste to the right by it's speed.
    
    #Damage protocol, used for determining colision and ewaste/player health. If ewaste reaches the end or is out of health, it gets removed from the  
    for machine in range(len(recyclerX)):
        for eWaste in range(len(eWasteX)):
            if eWasteStatus[eWaste] == 1: #checks to see if the enemy is alive.
                if eWasteX[eWaste] == recyclerX[machine] and eWasteY[eWaste] == recyclerY[machine]: #if the e-waste colides with a recycler, the e-waste loses 10 health
                    eWasteHealth[eWaste] -= recyclerDamage[machine] #the damage the recycler does to the e-waste health
                    if eWasteHealth[eWaste] <= 0: #if the health of the e-waste is dead, delete it from list
                        eWasteStatus[eWaste] = 0 #it's not alive, so change it's status to dead
                        greenCoins += eWasteCoinDrop[eWaste] #give the coins that it dropped
                        
                #code saying if the enemy reaches the end of the path, reduce player health
                elif eWasteX[eWaste] == 990: #if the e-waste the end of the path.
                    playerHealth -= 10
                    eWasteStatus[eWaste] = 0 #0 for dead, 1 for alive
                    #maybe simplify code above by changing health to 0 when it contacts edge?

def enemyTier1(roundNumber):
    global eWasteX
    global eWasteHealth
    global eWasteDamage
    global eWasteColor
    global eWasteCoinDrop
    
    #below are some attributes of the e-waste
    eWasteX.append(0)
    eWasteY.append(random.choice([225, 325, 425])) #randomly chooses which lane the e-waste goes through
    eWasteHealth.append(100 + 2*roundNumber) #adding the roundNumber*2 to the health increases the difficulty factor each round.
    eWasteDamage.append(10)
    eWasteColor.append(BLUE)
    eWasteStatus.append(1)
    eWasteCoinDrop.append(10)
    eWasteSpeed.append(1.5) #how many units right does this move each iteration / frame

def enemyTier2(roundNumber):
    global eWasteX
    global eWasteHealth
    global eWasteDamage
    global eWasteColor
    global eWasteCoinDrop
    
    eWasteX.append(0)
    eWasteY.append(random.choice([225, 325, 425]))
    eWasteHealth.append(125 + 3*roundNumber)
    eWasteDamage.append(15)
    eWasteColor.append(PURPLE)
    eWasteStatus.append(1)
    eWasteCoinDrop.append(20)
    eWasteSpeed.append(2)

def enemyTier3(roundNumber):
    global eWasteX
    global eWasteHealth
    global eWasteDamage
    global eWasteColor
    global eWasteCoinDrop
    
    eWasteX.append(0)
    eWasteY.append(random.choice([225, 325, 425]))
    eWasteHealth.append(150 + 4*roundNumber)
    eWasteDamage.append(25)
    eWasteColor.append(RED)
    eWasteStatus.append(1)
    eWasteCoinDrop.append(30)
    eWasteSpeed.append(3)
    

#This is the function that finds where the user wants to place the recycler, and draws it.
def recycler():
    global mx, my
    global recyclerX
    global placeRecycler
    global greenCoins
    
    #checks if user presses buy button and if they have enough money to purchase it.
    if 550 > mx > 450 and 650 > my > 600 and greenCoins >= 10:
        placeRecycler = True
    
    xPosition = recyclerPositionFactor(mx)
    
    #places it in the lane the user wants it to be in a grid with 90 x 90 squares.
    if placeRecycler == True and 400 > my > 300: #user placing recycler on middle track
        xPosition = recyclerPositionFactor(mx)
        if recyclerPlacementCheck(xPosition, 325) == False:
            recyclerX.append(xPosition)
            recyclerY.append(325)
            recyclerDamage.append(50) #this is level 1 damage that recycler does to e-waste
            mx = 0
            my = 0
            placeRecycler = False
            greenCoins -= 10
        else: print("error: already placed, click another spot")
    
    elif placeRecycler == True and 300 > my > 200: #user placing recycler on top track
        xPosition = recyclerPositionFactor(mx)
        if recyclerPlacementCheck(xPosition, 225) == False:
            recyclerX.append(xPosition)
            recyclerY.append(225)
            recyclerDamage.append(50) #this is level 1 damage that recycler does to e-waste
            mx = 0
            my = 0
            placeRecycler = False
            greenCoins -=10
        else: print("error: already placed, click another spot")
    
    elif placeRecycler == True and 500 > my > 400: #user placing recycler on bottom track
        xPosition = recyclerPositionFactor(mx)
        if recyclerPlacementCheck(xPosition, 425) == False:
            recyclerX.append(xPosition)
            recyclerY.append(425)
            recyclerDamage.append(50) #this is level 1 damage that recycler does to e-waste
            mx = 0
            my = 0
            placeRecycler = False
            greenCoins -=10
        else: print("error: already placed, click another spot")
    
    #draw the recycler
    for machine in range(len(recyclerX)): #how many recyclers there are.                    
        draw.rect(screen, GREEN, (recyclerX[machine], recyclerY[machine], 50, 50)) #screen, color, (x, y, w, l)

#This function checks if there is already a recycler where the user is trying to place it.
def recyclerPlacementCheck(mx, my):
    alreadyPlaced = False
    for machine in range(len(recyclerX)):
        if recyclerX[machine] == mx and recyclerY[machine] == my:
            alreadyPlaced = True
    return alreadyPlaced

#We use this as a seperate function to clear up code.
def userEvents():
    global mx, my
    #if the user does not drags the window do the lines of code below
    for evnt in event.get():
        if evnt.type == MOUSEBUTTONDOWN:
            mx, my = evnt.pos

#This is the player's health bar that is displayed on the screen
def playerHealthBar():
    draw.rect(screen, GREEN, (400, 25, 2 * playerHealth, 30))
    playerHealthText = smallFont.render(str(playerHealth), 1, WHITE)
    screen.blit(playerHealthText, Rect(405, 30, 0, 0)) #player health text   
    
#This is the button to start the round
def startButton():
    global mx, my
    global roundStarted
    global roundNumber
    global generateEnemies
    draw.rect(screen, WHITE, (0, 0, 50, 20))
    onGoing = roundOnGoing()
    
    #The logic here is that if the round is already ongoing, set roundStarted to false so that way in the next block of code the user can't start
    #... another wave of enemies before the current one has finished.
    if onGoing == False:
        roundStarted = False
        
        
    if (50 > mx > 0 and 20 > my > 0) and roundStarted == False: #check if the button is clicked and if the round has not already started
        roundStarted = True
        roundNumber += 1
        generateEnemies = True #set this to true, so in the game loop we can generate a wave of enemies.
        mx = 0
        my = 0

#This function checks if there is an ongoing round
def roundOnGoing(): 
    #the logic here is that by default the variable will be false. if all of the enemies are not alive, it will remain False.
    onGoing = False
    for status in eWasteStatus:
        if status == 1:
            onGoing = True
    return onGoing

#checks if the position is a factor of 90 to prevent e-waste with a faster movement speed from skipping over it (as 90 has a factor of 1.5, 2 and 3, the movespeed for tier 1, 2, and 3 e-waste).
def recyclerPositionFactor(position): 
    if position % 90 == 0:
        return position
    else: #if it's not a factor of 90
        roundedPosition = position / 90 
        roundedPosition = 90 * round(roundedPosition)
        return roundedPosition

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)   
init()
SIZE = (1000, 700)
screen = display.set_mode(SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
myClock = time.Clock()
smallFont = font.SysFont("Arial", 18)

running = True
game = True #we haven't created a main menu yet, so set this to true for now.
started = True
placeRecycler = False #true for now, used for placing recycler
roundStarted = False #if a round / wave / match is started.
generateEnemies = False
roundNumber = 0

#global mouse x and y position
mx = 0
my = 0

playerHealth = 100
greenCoins = 50 #this is the currency / coin system
score = 0

recyclerX = [] #number of recyclers, and their x position.
recyclerY = []
recyclerDamage = [] #how much damage each recycler does to the health of the eWaste

eWasteX = [] #x-position of the e-waste's
eWasteY = [] #y-position
eWasteHealth = [] #ewaste health
eWasteDamage = [] #the damage the e-waste deals to player
eWasteColor = []
eWasteStatus = []
eWasteCoinDrop = []
eWasteSpeed = []

#entire loop
while running:
    if game == True:
        gameMenu()

    myClock.tick(60)
quit()
