#Summative

#make a game that's similar to plants vs zombies
#The "zombies" going in the pathway are the non enviormentally recycled electronics
#What the user has to do is place good guys (recyclers) on the pathways, which recycles the electornic waste from reaching the end of the production plant. (end of the path)
#the enemies will go inside them (colide) and they lose health, but if they reach the end of the path sucessfully then the player loses health.
#each stage will use randomness to decide which enemies (e-waste) will be placed / go through the pathway?

from pygame import*
import os
import random

#this is under development, but is only visible once the user dies. Once done, the user is able to see his score and other player's score, and add his score to the scoreboard.
def scoreboardMenu():
    global scoreboardList
    numFile = open("scoreboard.dat", "r")
    if len(scoreboardList) == 0: #this way, when the game keeps calling this function, it doesn't repeat the same data into the scoreboardList.
        while True:
            text = numFile.readline()
            #rstrip removes the newline character read at the end of the line
            text = text.rstrip("\n")
            if text=="": 
                break
            text = text.split(",")
            scoreboardList.append(text)
        numFile.close()
        
        addToScoreboard() #see if the user has a score in the top 10, then output.
        
        draw.rect(screen, BLACK, (0, 0, 1000, 700))
        for record in range(len(scoreboardList)):
            for field in range(len(scoreboardList[record])):
                displayText = smallFont.render(scoreboardList[record][field], 1, WHITE)
                screen.blit(displayText, Rect(field * 100, record * 30, 500, 500))
                
        numFile = open("scoreboard.dat", "w")
        for record in scoreboardList:
            writeLine = "%s,%s\n" % (record[0], record[1])
            numFile.write(writeLine)
        numFile.close()
#to do, display only the top 10 scores.

#this function finds adds the users score in the appropriate place to the scoreboardList, so it can be displayed in the scoreboardMenu function.
def addToScoreboard():
    global scoreboardList
    scoreAdded = False
    
    for player in scoreboardList:
        if score > int(player[1]): #if the player's score is bigger then the other player's score. this works as it looks through the score of the highest players first.
            #slice the list
            usersPlace = scoreboardList.index(player)
            scoreboardListTemp1 = scoreboardList[:usersPlace]
            scoreboardListTemp2 = scoreboardList[usersPlace:]
            #add score in between slice.
            scoreboardList = scoreboardListTemp1 + [[playerName, str(score)]] + scoreboardListTemp2
            scoreAdded = True
            break
    #if his score is not bigger than any score, add it to the end.
    if scoreAdded == False:
        scoreboardList.append([playerName, str(score)]) #score must be a string, otherwise: builtins.TypeError: text must be a unicode or bytes


def mainMenu(): #main menu
    global mx, my
    global menu
    global game
    draw.rect(screen, BLACK, (0, 0, 100, 700))
    draw.rect(screen, BLUE, (450, 375, 100, 50))
    
    #playername
    draw.rect(screen, WHITE, (30, 30, 250, 40))
    nameText = smallFont.render(playerName, 1, BLACK)
    screen.blit(nameText, Rect(35, 35, 500, 500))    
    
    if 550 > mx > 450 and 425 > my > 375:
        game = True
        menu = False
        #print(playerName)
    

def gameMenu(): #game
    global roundStarted
    global generateEnemies
    global greenCoins
    global game
    global scoreboard
    global score
    
    if playerHealth <= 0:
        game = False
        scoreboard = True
        
    score = roundNumber * 10
    
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
    
    #buy and sell recycler button
    draw.rect(screen, GREEN, (450, 600, 100, 50))
    draw.rect(screen, RED, (650, 600, 100, 50))
    
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
    
    #userEvents()
    
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

            #code saying if the enemy reaches the end of the path, reduce player health
            if eWasteX[eWaste] == 990: #if the e-waste the end of the path.
                playerHealth -= 10
                eWasteStatus[eWaste] = 0 #0 for dead, 1 for alive        
    
    #Damage protocol, used for determining colision and ewaste/player health. If ewaste reaches the end or is out of health, it gets removed from the  
    for machine in range(len(recyclerX)):
        for eWaste in range(len(eWasteX)):
            if eWasteStatus[eWaste] == 1 and recyclerStatus[machine] == 1: #checks to see if the enemy is alive.
                if eWasteX[eWaste] == recyclerX[machine] and eWasteY[eWaste] == recyclerY[machine]: #if the e-waste colides with a recycler, the e-waste loses 10 health
                    eWasteHealth[eWaste] -= recyclerDamage[machine] #the damage the recycler does to the e-waste health
                    if eWasteHealth[eWaste] <= 0: #if the health of the e-waste is dead, delete it from list
                        eWasteStatus[eWaste] = 0 #it's not alive, so change it's status to dead
                        greenCoins += eWasteCoinDrop[eWaste] #give the coins that it dropped

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
    global sellRecycler
    global greenCoins
    global indexForRecyclerPlacementCheck
    
    #checks if user presses buy button and if they have enough money to purchase it.
    if 550 > mx > 450 and 650 > my > 600 and greenCoins >= 10:
        placeRecycler = True
    elif 750 > mx > 650  and 650 > my > 600 and placeRecycler == False: #placeRecycler must be false otherwise the user deletes the recycler right after they placed it. 
        sellRecycler = True
    xPosition = recyclerPositionFactor(mx) #this makes the placement of the recyclers follow a grid that's spaced by 90 pixels. Based off where the user clicks.
    xPositionHover = recyclerPositionFactor(hoverX) #this is when the user is hovering over where he wants to place it, but hasn't clicked it.
    
    if placeRecycler == True:
        #place it in the lane the user wants it to be in, following the invisible grid.
        
        #when the user is hovering the mouse, show a preview of where it'll be
        if 400 > hoverY > 300: #preview recycler on middle track
            draw.rect(screen, GREEN, (xPositionHover, 325, 50, 50)) #screen, color, (x, y, w, l)
        
        elif 300 > hoverY > 200: #...top track
            draw.rect(screen, GREEN, (xPositionHover, 225, 50, 50)) #screen, color, (x, y, w, l)
        
        elif 500 > hoverY > 400: #or bottom track
            draw.rect(screen, GREEN, (xPositionHover, 425, 50, 50)) #screen, color, (x, y, w, l)      
        
        #when the user clicks, place the recycler.
        if 400 > my > 300: #user placing recycler on middle track
            placingRecycler(xPosition, 325)
        
        elif 300 > my > 200: #user placing recycler on top track
            placingRecycler(xPosition, 225)
        
        elif 500 > my > 400: #user placing recycler on bottom track
            placingRecycler(xPosition, 425)
            
    elif sellRecycler == True:
        if 400 > my > 300: #middle track
            if recyclerPlacementCheck(xPosition, 325) == True:
                recyclerStatus[indexForRecyclerPlacementCheck] = 0
                greenCoins += recyclerSellPrice[indexForRecyclerPlacementCheck]
                sellRecycler = False
                
        elif 300 > my > 200: #top track
            if recyclerPlacementCheck(xPosition, 225) == True:
                recyclerStatus[indexForRecyclerPlacementCheck] = 0
                greenCoins += recyclerSellPrice[indexForRecyclerPlacementCheck]
                sellRecycler = False
        
        elif 500 > my > 400: #bottom track
            if recyclerPlacementCheck(xPosition, 425) == True:
                recyclerStatus[indexForRecyclerPlacementCheck] = 0
                greenCoins += recyclerSellPrice[indexForRecyclerPlacementCheck]
                sellRecycler = False
                
    #draw the recycler
    for machine in range(len(recyclerX)): #how many recyclers there are.
        if recyclerStatus[machine] == 1: #if the recycler is not sold
            draw.rect(screen, GREEN, (recyclerX[machine], recyclerY[machine], 50, 50)) #screen, color, (x, y, w, l)

#this function places the recyclers onto the map if there isn't one already placed in the desired location
def placingRecycler(xPosition, yLane):
    global placeRecycler
    global greenCoins
    if recyclerPlacementCheck(xPosition, yLane) == False:
        recyclerX.append(xPosition)
        recyclerY.append(yLane)
        recyclerDamage.append(50) #this is level 1 damage that recycler does to e-waste
        recyclerStatus.append(1) #the recycler has not been sold yet.
        recyclerSellPrice.append(5) #the price that the user can sell the recycler at
        mx = 0
        my = 0
        placeRecycler = False
        greenCoins -= 10
    else: print("error: already placed, click another spot")

#This function checks if there is already a recycler where the user is trying to place it.
def recyclerPlacementCheck(mx, my):
    global indexForRecyclerPlacementCheck #this is used so we can know what number 'machine' lands on to make the condition true. This will be used for deleting recycler.
    alreadyPlaced = False
    for machine in range(len(recyclerX)):
        if recyclerX[machine] == mx and recyclerY[machine] == my and recyclerStatus[machine] == 1:
            indexForRecyclerPlacementCheck = machine
            alreadyPlaced = True
    return alreadyPlaced

#We use this as a seperate function to clear up code.
def userEvents():
    global mx, my
    global hoverX, hoverY
    global playerName
    #if the user does not drags the window do the lines of code below
    for evnt in event.get():
        if evnt.type == MOUSEBUTTONDOWN:
            mx, my = evnt.pos
        if evnt.type == MOUSEMOTION:
            hoverX, hoverY = evnt.pos
        if menu == True and evnt.type == KEYDOWN: #when the user is entering his name in the main menu.
            if key.name(evnt.key) == "backspace": #if user hits backspace, delete last key
                    playerName = playerName[:-1]
            else: playerName += evnt.unicode

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
game = False #we haven't created a main menu yet, so set this to true for now.
menu = True
scoreboard = False
started = True
placeRecycler = False #used for placing recycler
sellRecycler = False
roundStarted = False #if a round / wave / match is started.
generateEnemies = False
roundNumber = 0

#global mouse x and y position
mx = 0
my = 0
hoverX = 0
hoverY = 0
indexForRecyclerPlacementCheck = -1
playerHealth = 100
greenCoins = 50 #this is the currency / coin system
score = 0

recyclerX = [] #number of recyclers, and their x position.
recyclerY = []
recyclerDamage = [] #how much damage each recycler does to the health of the eWaste
recyclerStatus = [] #0 if sold, 1 if not sold.
recyclerSellPrice = []

eWasteX = [] #x-position of the e-waste's
eWasteY = [] #y-position
eWasteHealth = [] #ewaste health
eWasteDamage = [] #the damage the e-waste deals to player
eWasteColor = []
eWasteStatus = []
eWasteCoinDrop = []
eWasteSpeed = []

scoreboardList = []

playerName = ""

#entire loop
while running:
    if menu == True:
        mainMenu()
    elif game == True:
        gameMenu()
    elif scoreboard == True:
        scoreboardMenu()
    
    userEvents()
    myClock.tick(60)
    display.flip()
quit()
