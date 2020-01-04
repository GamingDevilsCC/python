#Summative

#make a game that's similar to plants vs zombies
#The "zombies" going in the pathway are the non enviormentally recycled electronics
#What the user has to do is place good guys (recyclers) on the pathways, which recycles the electornic waste from reaching the end of the production plant. (end of the path)
#the enemies will go inside them (colide) and they lose health, but if they reach the end of the path sucessfully then the player loses health.
#each stage will use randomness to decide which enemies (e-waste) will be placed / go through the pathway?

from pygame import*
import os
import random

def gameMenu(): #game
    global roundStarted
    global generateEnemies
    #track
    draw.rect(screen, BLACK, (0, 0, 1000, 700))
    draw.rect(screen, WHITE, (0, 300, 1000, 100))
    playerHealthBar()
    startButton() #to start the round and generate enemies
    
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
            draw.rect(screen, eWasteColor[eWaste], (eWasteX[eWaste], 325, 50, 50)) #screen, color, x, y, w, l
            enemyHealthText = smallFont.render(str(eWasteHealth[eWaste]), 1, WHITE)
            screen.blit(enemyHealthText, Rect(eWasteX[eWaste] + 5, 330, 0, 0)) #e-waste health text
            eWasteX[eWaste] += eWasteSpeed[eWaste] #increase the x position of e-waste to the right by it's speed.
    
    
    #Damage protocol, used for determining colision and ewaste/player health. If ewaste reaches the end or is out of health, it gets removed from the  
    for machine in range(len(recyclerX)):
        for eWaste in range(len(eWasteX)):
            if eWasteStatus[eWaste] == 1: #checks to see if the enemy is alive.
                if eWasteX[eWaste] == recyclerX[machine]: #if the e-waste colides with a recycler, the e-waste loses 10 health
                    eWasteHealth[eWaste] -= recyclerDamage[machine] #the damage the recycler does to the e-waste health
                    if eWasteHealth[eWaste] <= 0: #if the health of the e-waste is dead, delete it from list
                        eWasteStatus[eWaste] = 0 #it's not alive, so change it's status to dead
                        greenCoins += eWasteCoinDrop[eWaste] #give the coins that it dropped
                        print(greenCoins)
                        
                #code saying if the enemy reaches the end of the path, reduce player health
                elif eWasteX[eWaste] == 990: #if the e-waste the end of the path. it's 50 pixels wide, so 950 instead of 1000.
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
    eWasteHealth.append(100 + 2*roundNumber) #adding the roundNumber*2 to the health increases the difficulty factor each round.
    eWasteDamage.append(10)
    eWasteColor.append(BLUE)
    eWasteStatus.append(1)
    eWasteCoinDrop.append(10)
    eWasteSpeed.append(1) #how many units right does this move each iteration / frame

def enemyTier2(roundNumber):
    global eWasteX
    global eWasteHealth
    global eWasteDamage
    global eWasteColor
    global eWasteCoinDrop
    
    eWasteX.append(0)
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
    
    if placeRecycler == True and 400 > my > 300: #These are temporary parameters for now while the game is being developed.
        xPosition = recyclerPositionFactor(mx)
        recyclerX.append(xPosition)
        recyclerDamage.append(10) #this is level 1 damage that recycler does to e-waste
        mx = 0
        my = 0
    
    #draw the recycler
    for machine in range(len(recyclerX)): #how many recyclers there are.                    
        draw.rect(screen, GREEN, (recyclerX[machine], 325, 50, 50)) #Only the x value is set. This way when a user places one down, it doesn't look out of place.

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

#checks if the position is a factor of 90 to prevent e-waste with a faster movement speed from skipping over it (as 90 has a factor of 2 and 3, the movespeed for tier 2 and tier 3 e-waste).
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
placeRecycler = True #true for now, used for placing recycler
roundStarted = False #if a round / wave / match is started.
generateEnemies = False
roundNumber = 0

#global mouse x and y position
mx = 0
my = 0

playerHealth = 100
greenCoins = 0 #this is the currency / coin system
score = 0

recyclerX = [] #number of recyclers, and their x position.
recyclerDamage = [] #how much damage each recycler does to the health of the eWaste

eWasteX = [] #initial x-position of the testing ewaste
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