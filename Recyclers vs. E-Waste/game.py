#Summative

#make a game that's similar to plants vs zombies
#The "zombies" going in the pathway are the non enviormentally recycled electronics
#What the user has to do is place good guys (recyclers) on the pathways, which recycles the electornic waste from reaching the end of the production plant. (end of the path)
#the enemies will go inside them (colide) and they lose health, but if they reach the end of the path sucessfully then the player loses health.
#each stage will use randomness to decide which enemies (e-waste) will be placed / go through the pathway?

from pygame import*
import os
import random

#tutorial menu, accessed through mainMenu
def tutorialMenu():
    screen.blit(tutorialPic, Rect(0, 0, 1000, 700))
    draw.rect(screen, RED, (875, 40, 100, 50)) #exit button. the activation for this is seen in userEvents function
    line1 = "Welcome, %s! Our recycling plant has been experiencing an influx of electronic waste." %playerName
    line2 = "It is your duty to recycle the electronic waste before it reaches the end."
    line3 = "You can do this by buying a recycler and placing it on any of the lanes."
    line4 = "Green button is for a tier 1 recycler costing 10 green coins,"
    line5 = "while blue is for tier 2 for 50. Tier 2 allows you to repel your enemies back."
    line6 = "If there is a recycler already there, place it somewhere else."
    line7 = "If you wish to sell a recycler, press the red button."
    line8 = "Then, press the white button to start the round."
    line9 = "If you want the next round to automatically start, press it midround."
    line10 = "To turn autostart back off, press it again."
    line11 = "e-waste have 3 tiers, increasing in heath and speed the higher the tier."
    line12 = "Now lets start recycling!"
    lines = [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12]
    for i in range(len(lines)):
        text = mediumFont.render(lines[i], 1, WHITE)
        screen.blit(text, Rect(15, 5 + 40 * i, 0, 0))
    
    

#only visible once the user dies. The user is able to see his score and other player's score, and add his score to the scoreboard.
def scoreboardMenu():
    global scoreboardList
    global usersPlace
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
        
        addToScoreboard() #place the user's score in the appropriate place
        
        numFile = open("scoreboard.dat", "w")
        for record in scoreboardList:
            writeLine = "%s,%s\n" % (record[0], record[1]) #playerName, score
            numFile.write(writeLine)
        numFile.close()
        
        #limit the list to show only the top 10 scores.
        if len(scoreboardList) > 10:
            scoreboardList = scoreboardList[:10] #indexes from 0 to 9, the top 10 scores        
        
        #format the numbers to be right adjacent (but with 0's instead of spaces)
        for row in scoreboardList:
            if len(row[1]) == 1:
                row[1] = "00%s" % row[1]
            elif len(row[1]) == 2:
                row[1] = "0%s" % row[1]
                
        #visuals
        screen.blit(scoreboardPic, Rect(0, 0, 1000, 700)) #background
        topBarText = largeFont.render("Congratulations %s, you placed at #%i!" %(playerName, usersPlace + 1), 1, WHITE) #top bar text that shows the user's rank and name.
        screen.blit(topBarText, Rect(25, 20, 500, 500))
        #exit button. activation of the exit button is seen in the userEvents() function
        draw.rect(screen, RED, (850, 20, 100, 50))
        restartText = mediumFont.render("Restart", 1, BLACK) #restart text
        screen.blit(restartText, Rect(865, 30, 500, 500))              
        for record in range(len(scoreboardList)):
            for field in range(len(scoreboardList[record])):
                displayText = largeFont.render(scoreboardList[record][field], 1, BLACK)
                screen.blit(displayText, Rect(60 + field * 350, 100 + record * 60, 500, 500))

#this function finds adds the users score in the appropriate place to the scoreboardList, so it can be displayed in the scoreboardMenu function.
def addToScoreboard():
    global scoreboardList
    global usersPlace #only place this is used aside from this function is above, in topBarText.
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
        else: usersPlace = len(scoreboardList) #if the user is last place
        
    #if his score is not bigger than any score, add it to the end / last.
    if scoreAdded == False:
        scoreboardList.append([playerName, str(score)]) #score must be a string, otherwise: builtins.TypeError: text must be a unicode or bytes

#main menu
def mainMenu():
    global mx, my
    global menu, game, tutorial
    global playerName
    screen.blit(menuPic, Rect(0, 0, 1000, 700))
    screen.blit(titlePic, Rect(50, 10, 900, 160))
    #game button
    draw.rect(screen, RED, (375, 350, 250, 80))
    gameGuideText = largeFont.render("Start", 1, WHITE)
    screen.blit(gameGuideText, Rect(465, 365, 500, 500))    
    #tutorial button
    draw.rect(screen, PURPLE, (375, 450, 250, 80)) 
    tutorialGuideText = largeFont.render("Tutorial", 1, WHITE)
    screen.blit(tutorialGuideText, Rect(450, 465, 500, 500))    
    
    #player's name textbox. the user inputs their name through userEvents()
    draw.rect(screen, WHITE, (300, 225, 400, 75)) #this box can only fit a maximum of 18 characters
    nameText = largeFont.render(playerName, 1, BLACK)
    screen.blit(nameText, Rect(315, 245, 500, 500))
    
    guidingText = smallFont.render("Enter your name in the box and press start to play!", 1, BLACK)
    screen.blit(guidingText, Rect(337, 225, 500, 500))    
    
    #if the user enters a name, allow them to access the Play Game button and Tutorial button.
    if len(playerName) > 0:
        if 625 > mx > 375 and 430 > my > 350:
            game = True
            menu = False
            hint.play()

        elif 625 > mx > 375 and 530 > my > 450:
            tutorial = True
            menu = False
            hint.play()
    else: #tells the user to type on their keyboard. this is only visible when the user has not entered anything
        guidingText2 = mediumFont.render("Type on your keyboard to enter a name.", 1, BLACK)
        screen.blit(guidingText2, Rect(325, 250, 500, 500))
    

def gameMenu(): #game
    global roundStarted
    global generateEnemies
    global game, scoreboard
    global score, status, greenCoins
    
    #once the player loses all their health, switch over to the scoreboardMenu
    if playerHealth <= 0:
        game = False
        scoreboard = True
        victory.play() #victory sound
        
    score = roundNumber * 10
    
    #track
    screen.blit(floorPic, (0, 0, 1000, 700)) #floor
    screen.blit(pathPic, (0, 200, 1000, 100)) #top track
    screen.blit(pathPic, (0, 300, 1000, 100)) #middle track
    screen.blit(pathPic, (0, 400, 1000, 100)) #bottom track
    
    #top bar
    draw.rect(screen, BLUE, (0, 0, 1000, 80))
    #health
    playerHealthBar()
    #coins
    coinText = smallFont.render("Coins: $%i" %greenCoins, 1, WHITE)
    screen.blit(coinText, Rect(900, 30, 0, 0)) #displays coin
    #score
    scoreText = smallFont.render("Score: %i" %score, 1, WHITE)
    screen.blit(scoreText, Rect(800, 30, 0, 0)) #player health text
    #round number
    roundText = smallFont.render("Round %i" %roundNumber, 1, WHITE)
    screen.blit(roundText, Rect(700, 30, 0, 0)) #round number text
    #status
    statusText = smallFont.render("Message: %s" %status, 1, WHITE)
    screen.blit(statusText, Rect(10, 30, 0, 0))
    
    #buttons
    #buy tier 2 recycler
    draw.rect(screen, BLUE, (250, 600, 100, 50))
    tier2GuideText = smallFont.render("Tier2: $50", 1, BLACK)
    screen.blit(tier2GuideText, Rect(265, 615, 0, 0))
    #buy tier 1 recycler
    draw.rect(screen, GREEN, (450, 600, 100, 50)) 
    tier1GuideText = smallFont.render("Tier1: $10", 1, BLACK)
    screen.blit(tier1GuideText, Rect(465, 615, 0, 0))
    #sell recycler
    draw.rect(screen, RED, (650, 600, 100, 50)) 
    sellGuideText = smallFont.render("Sell", 1, BLACK)
    screen.blit(sellGuideText, Rect(685, 615, 0, 0))
    
    startButton() #to start the round and generate enemies
    
    
    #the generate the e-waste and if the round has started, show the e-waste. Show recyclers regardless if round has started or not. 
    if generateEnemies:
        #tier 1 e-waste spawns every round
        enemyTier1(roundNumber)
        
        #second tier 1 e-waste has a 50% chance of spawning
        spawnTier1 = random.choice([1, 0])
        if spawnTier1 == 1: #50% chance      
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
        status = "10 coin new round bonus."
        #maybe add sound here
    
    if roundStarted:
        enemiesMoving()
        
    recycler() #display the recyclers.
    
#animation for the e-waste moving through the screen.
def enemiesMoving(): #will have feature to randomly select different levels of enemies soon.
    global playerHealth
    global recyclerX, recyclerStatus, recyclerTier, recyclerHealth
    global eWasteX, eWasteHealth, eWasteDamage, eWaseColor, eWasteCoinDrop 
    global greenCoins
    
    #electronic waste          
    for eWaste in range(len(eWasteX)): #how many e-waste enemies there are. nested loop because of enemyHealth requiring information from machine
        if eWasteStatus[eWaste] == 1: #checks to see if the enemy is alive.
            screen.blit(eWastePic[eWaste], Rect(eWasteX[eWaste], eWasteY[eWaste], 50, 50))
            draw.rect(screen, eWasteColor[eWaste], (eWasteX[eWaste], eWasteY[eWaste] + 5, 35, 20)) #screen, color, (x, y, w, l)
            enemyHealthText = smallFont.render(str(eWasteHealth[eWaste]), 1, WHITE)
            screen.blit(enemyHealthText, Rect(eWasteX[eWaste] + 5, eWasteY[eWaste] + 5, 0, 0)) #e-waste health text
            eWasteX[eWaste] += eWasteSpeed[eWaste] #increase the x position of e-waste to the right by it's speed.

            #code saying if the enemy reaches the end of the path, reduce player health
            if eWasteX[eWaste] == 990: #if the e-waste the end of the path.
                playerHealth -= eWasteDamage[eWaste] #damages the player.
                eWasteStatus[eWaste] = 0 #0 for dead, 1 for alive
                machineGrinding.play() #machine grinding sound
    
    #Damage protocol, used for determining colision and ewaste/player health. If ewaste reaches the end or is out of health, it gets removed from the  
    for machine in range(len(recyclerX)):
        for eWaste in range(len(eWasteX)):
            if eWasteStatus[eWaste] == 1 and recyclerStatus[machine] == 1: #checks to see if the enemy is alive.
                if eWasteX[eWaste] == recyclerX[machine] and eWasteY[eWaste] == recyclerY[machine]: #if the e-waste colides with a recycler
                    eWasteHealth[eWaste] -= recyclerDamage[machine] #the damage the recycler does to the e-waste health
                    if eWasteHealth[eWaste] <= 0: #if the health of the e-waste is dead, delete it from list
                        eWasteStatus[eWaste] = 0 #it's not alive, so change it's status to dead
                        greenCoins += eWasteCoinDrop[eWaste] #give the coins that it dropped
                        ping.play() #ping sound
                    elif recyclerTier[machine] == 2: #if it's a tier 2 recycler...
                        eWasteX[eWaste] -= 50*(eWasteSpeed[eWaste]) #repel the e-waste back by 20 times it's move speed
                        recyclerHealth[machine] -= eWasteDamage[eWaste] #the recycler loses health
                        if recyclerHealth[machine] <= 0: #and if the recycler lost all it's health... 
                            recyclerStatus[machine] = 0 #... it is no longer a real entity.

def enemyTier1(roundNumber):
    global eWasteX
    global eWasteHealth
    global eWasteDamage
    global eWasteColor
    global eWasteCoinDrop
    
    #below are some attributes of the e-waste
    eWasteX.append(0)
    eWasteY.append(random.choice([225, 325, 425])) #randomly chooses which lane the e-waste goes through
    eWasteHealth.append(100 + 5*(roundNumber - 1)) #adding the roundNumber*5 to the health increases the difficulty factor each round, aka first round is 100 health, while 11th round is 120 health
    eWasteDamage.append(15)
    eWasteColor.append(BLUE)
    eWastePic.append(tier1Pic)
    eWasteStatus.append(1)
    eWasteCoinDrop.append(10)
    eWasteSpeed.append(2) #how many units right does this move each iteration / frame

def enemyTier2(roundNumber):
    global eWasteX
    global eWasteHealth
    global eWasteDamage
    global eWasteColor
    global eWasteCoinDrop
    
    eWasteX.append(0)
    eWasteY.append(random.choice([225, 325, 425]))
    eWasteHealth.append(125 + 10*(roundNumber - 1)) #base health + 10 times the roundNumber
    eWasteDamage.append(30)
    eWasteColor.append(PURPLE)
    eWastePic.append(tier2Pic)
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
    eWasteHealth.append(150 + 10*(roundNumber - 1))
    eWasteDamage.append(40)
    eWasteColor.append(RED)
    eWastePic.append(tier3Pic)
    eWasteStatus.append(1)
    eWasteCoinDrop.append(30)
    eWasteSpeed.append(3)
    

#This is the function that previews where the user wants to place the recycler, and draws it once placed. Otherwise, the user can sell the recycler.
def recycler():
    global mx, my
    global recyclerX, placeRecyclerTier1, placeRecyclerTier2, sellRecycler
    global greenCoins
    
    #checks if user presses tier 1 buy button and if they have enough money to purchase it.
    if 550 > mx > 450 and 650 > my > 600 and greenCoins >= 10 and placeRecyclerTier1 == False:
        placeRecyclerTier1 = True
        sellRecycler = False #just in case the user presses sell button and then buy button without selling recycler.
        hint.play()
    
    #checks if user presses tier 1 buy button and if they have enough money to purchase it.
    elif 350 > mx > 250 and 650 > my > 600 and greenCoins >= 50 and placeRecyclerTier2 == False:
        placeRecyclerTier2 = True
        sellRecycler = False #just in case the user presses sell button and then buy button without selling recycler.
        hint.play()
    elif 750 > mx > 650 and 650 > my > 600 and placeRecyclerTier1 == False and placeRecyclerTier2 == False: #placeRecyclerTierX must be false otherwise the user deletes the recycler right after they placed it. 
        sellRecycler = True
        hint.play()

    xPosition = recyclerPositionFactor(mx) #this makes the placement of the recyclers follow a grid that's spaced by 90 pixels. Based off where the user clicks.
    xPositionHover = recyclerPositionFactor(hoverX) #this is when the user is hovering over where he wants to place it, but hasn't clicked it.
    
    #if the user wants to change his mind and cancel their action, let them do so.
    if placeRecyclerTier1 == True or placeRecyclerTier2 == True or sellRecycler == True:
        #drawing the button
        draw.rect(screen, BLACK, (850, 600, 100, 50))
        tier2GuideText = smallFont.render("Cancel", 1, WHITE)
        screen.blit(tier2GuideText, Rect(865, 615, 0, 0))
        #canceling the action
        if 950 > mx > 850  and 650 > my > 600:
            placeRecyclerTier1 = False
            placeRecyclerTier2 = False
            sellRecycler = False
            hint.play()
    
    if placeRecyclerTier1 == True: #if the user wants to buy a tier 1 recycler
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
            placingRecycler(xPosition, 325, 1)
        
        elif 300 > my > 200: #user placing recycler on top track
            placingRecycler(xPosition, 225, 1)
        
        elif 500 > my > 400: #user placing recycler on bottom track
            placingRecycler(xPosition, 425, 1)
        
    elif placeRecyclerTier2 == True: #if the user wants to buy a tier 2 recycler
        #place it in the lane the user wants it to be in, following the invisible grid.
        
        #when the user is hovering the mouse, show a preview of where it'll be
        if 400 > hoverY > 300: #preview recycler on middle track
            draw.rect(screen, BLUE, (xPositionHover, 325, 50, 50)) #screen, color, (x, y, w, l)
        
        elif 300 > hoverY > 200: #...top track
            draw.rect(screen, BLUE, (xPositionHover, 225, 50, 50)) #screen, color, (x, y, w, l)
        
        elif 500 > hoverY > 400: #or bottom track
            draw.rect(screen, BLUE, (xPositionHover, 425, 50, 50)) #screen, color, (x, y, w, l)      
        
        #when the user clicks, place the recycler.
        if 400 > my > 300: #user placing recycler on middle track
            placingRecycler(xPosition, 325, 2)
        
        elif 300 > my > 200: #user placing recycler on top track
            placingRecycler(xPosition, 225, 2)
        
        elif 500 > my > 400: #user placing recycler on bottom track
            placingRecycler(xPosition, 425, 2)
            
    elif sellRecycler == True: #if the user wants to sell the recycler
        if 400 > my > 300: #middle track
            if recyclerPlacementCheck(xPosition, 325) == True:
                sellingRecycler()
            else: 
                status = "There is no recycler where you tried to click."
                error.play()
                
        elif 300 > my > 200: #top track
            if recyclerPlacementCheck(xPosition, 225) == True:
                sellingRecycler()
            else: 
                status = "There is no recycler where you tried to click."
                error.play()
        
        elif 500 > my > 400: #bottom track
            if recyclerPlacementCheck(xPosition, 425) == True:
                sellingRecycler()
            else: 
                status = "There is no recycler where you tried to click."
                error.play()
                
    #draw the recyclers
    for machine in range(len(recyclerX)): #how many recyclers there are.
        if recyclerStatus[machine] == 1: #if the recycler is an entity in the game
            screen.blit(recyclerPic[machine], Rect(recyclerX[machine], recyclerY[machine], 50, 50))
            if recyclerTier[machine] == 2:
                recyclerHealthText = smallFont.render(str(recyclerHealth[machine]), 1, BLACK)
                draw.rect(screen, WHITE, (recyclerX[machine], recyclerY[machine] + 5, 35, 20))
                screen.blit(recyclerHealthText, Rect(recyclerX[machine] + 5, recyclerY[machine] + 5, 0, 0)) #tier 2 recycler health text                
            
#this function places the recyclers onto the map if there isn't one already placed in the desired location
def placingRecycler(xPosition, yLane, tier):
    global placeRecyclerTier1, placeRecyclerTier2
    global greenCoins
    global status
    if recyclerPlacementCheck(xPosition, yLane) == False:
        recyclerX.append(xPosition)
        recyclerY.append(yLane)
        recyclerHealth.append(100) #this isn't really used for tier 1 recyclers, only tier 2. When the tier 2 recycler blocks the e-waste, the e-waste deals damage to it. When it's recyclerHealth hits zero, it's no longer an entity in the game.
        recyclerDamage.append(50) #this is current damage that recycler does to e-waste
        recyclerStatus.append(1) #the recycler has not been sold yet.
        ironClang.play()
        if tier == 1: #tier 1
            recyclerTier.append(1)
            greenCoins -= 10
            recyclerSellPrice.append(5) #the price that the user can sell the recycler at
            recyclerPic.append(recyclerTier1Pic)
            status = "Recycler placed, 10 coin deducted."
            placeRecyclerTier1 = False
        elif tier == 2: #tier 2
            recyclerTier.append(2)
            greenCoins -= 50
            recyclerSellPrice.append(10) #the price that the user can sell the recycler at
            recyclerPic.append(recyclerTier2Pic)
            status = "Recycler placed, 50 coin deducted."    
            placeRecyclerTier2 = False
    else: 
        status = "Please place your recycler in a different spot!" #tells the user to place the recycler in a different spot, as there is a recycler already there.
        error.play()

#when called, the recycler status becomes sold, and the user is given his coins.
def sellingRecycler():
    global sellRecycler, indexForRecyclerPlacementCheck, recyclerStatus
    global greenCoins
    recyclerStatus[indexForRecyclerPlacementCheck] = 0
    greenCoins += recyclerSellPrice[indexForRecyclerPlacementCheck]  
    sellRecycler = False
    status = "Recycler sold, $%i coins returned." % recyclerSellPrice[indexForRecyclerPlacementCheck]  
    thud.play()

#This function checks if there is already a recycler where the user is trying to place it.
def recyclerPlacementCheck(mx, my):
    global indexForRecyclerPlacementCheck #this is used so we can know what number 'machine' lands on to make the condition true. This will be used for deleting recycler.
    alreadyPlaced = False
    for machine in range(len(recyclerX)):
        if recyclerX[machine] == mx and recyclerY[machine] == my and recyclerStatus[machine] == 1:
            indexForRecyclerPlacementCheck = machine
            alreadyPlaced = True
    return alreadyPlaced

#This function is what captures the users input.
def userEvents():
    global mx, my
    global hoverX, hoverY
    global playerName, playerHealth, roundNumber, scoreboardList
    global menu, scoreboard, tutorial, running
    #after every click, reset mx and my back to 0. that way the code doesn't think the user is still trying to activate a button even if they're not clicking.
    mx = 0
    my = 0
    
    #if the user does not drags the window do the lines of code below
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False        
        if evnt.type == MOUSEBUTTONDOWN:
            mx, my = evnt.pos
        if evnt.type == MOUSEMOTION:
            hoverX, hoverY = evnt.pos
        if menu == True and evnt.type == KEYDOWN: #when the user is entering his name in the main menu.
            if key.name(evnt.key) == "backspace": #if user hits backspace, delete last key
                    playerName = playerName[:-1]
            elif len(playerName) < 18 and key.name(evnt.key) != "return": playerName += evnt.unicode #maximum 18 characters can be fit on the textbox, so don't let them add more than 18.
        #if the user presses the exit button from the scoreboard
        elif scoreboard == True and 950 > mx > 850 and 70 > my > 20:
            menu = True
            scoreboard = False
            resetVariables()
            roundNumber = 0
            hint.play() #button activation sound
            theme.play() #plays main menu theme for when the user returns to main menu
        elif tutorial == True and 975 > mx > 875 and 90 > my > 40:
            tutorial = False
            menu = True

#This is the player's health bar that is displayed on the screen
def playerHealthBar():
    draw.rect(screen, RED, (400, 25, 200, 30))
    draw.rect(screen, GREEN, (400, 25, 2 * playerHealth, 30))
    playerHealthText = smallFont.render(str(playerHealth), 1, BLACK)
    screen.blit(playerHealthText, Rect(405, 30, 0, 0)) #player health text   
    
#This is the button to start the round
def startButton():
    global mx, my
    global roundStarted, roundNumber, autoStart
    global generateEnemies
    draw.rect(screen, WHITE, (50, 600, 100, 50))
    
    if autoStart == 1: #if the next round will automatically start, display to the user that they have enabled it.
        playerHealthText = smallFont.render("autoStart ON", 1, BLACK)
        screen.blit(playerHealthText, Rect(55, 615, 0, 0))  
        
    #The logic here is that if the round is already ongoing, set roundStarted to false so that way in the next block of code the user can't start
    #... another wave of enemies before the current one has finished.
    onGoing = roundOnGoing()
    if onGoing == False:
        roundStarted = False
    
    if (150 > mx > 50 and 650 > my > 600) or autoStart == 1: #if the button is clicked or the next round is set to automatically start...
        if roundStarted == False: #... and if the round has not already started, start the round.
            roundStarted = True
            roundNumber += 1
            generateEnemies = True #set this to true, so in the game loop we can generate a wave of enemies.
            autoStart = -1 #disable autoStart
            if 150 > mx > 50 and 650 > my > 600: #if the user actually clicked the button, set mx and my to (0,0) so the elif statement below doesn't get automatically activated and play a sound
                hint.play()
        
        #... and if there already is an ongoing round, let the user flip between auto-starting the next round, or not if they click again.
        elif roundStarted == True and (150 > mx > 50 and 650 > my > 600): #Here, I make sure the user actually clicks the button by adding "and (350 > mx ..."
            autoStart *= -1
            #reset the mouse click back to (0, 0) so this doesn't get automatically activated again
            hint.play() #confirmation sound

#This function checks if there is an ongoing round
def roundOnGoing(): 
    #the logic here is that by default the variable will be false. if all of the enemies are not alive, it will remain False.
    onGoing = False
    for status in eWasteStatus:
        if status == 1:
            onGoing = True
    return onGoing

#checks if the position is a factor of 90 to prevent e-waste with a faster movement speed from skipping over it (as 90 has a factor of 2 and 3, the movespeed for tier 1, 2, and 3 e-waste).
def recyclerPositionFactor(position): 
    #this makes it so the farthest the user can place one is 900 pixels, preventing it from clipping off screen while still being a factor of 90.
    if position >= 900:
        position = 900
    #prevents the user from placing it at the very left of the screen
    elif position <= 90:
        position = 90
    else: #makes it a factor of 90, and makes it follow a grid system spaced by 90 pixels.
        position = position / 90 
        position = 90 * round(position)
    return position

#this function makes the game fresh for when the user wants to play again. only seen when the user presses the leave button in scoreboardMenu()
def resetVariables():
    global playerHealth, playerName, greenCoins, score, roundNumber, autoStart, status
    global recyclerX, recyclerPic, recyclerHealth, recyclerDamage, recyclerStatus, recyclerTier, recyclerSellPrice
    global eWasteX, eWasteY, eWasteHealth, eWasteDamage, eWastePic, eWasteColor, eWasteStatus, eWasteCoinDrop, eWasteSpeed
    global scoreboardList
    greenCoins = 50 #this is the currency / coin system
    score = 0
    roundNumber = 0
    autoStart = -1 #if -1, next round won't automatically start. if 1, next round will.
    playerName = "" #resets the playerName to "", otherwise when the user goes to the main menu from scoreboard menu he will see his previously typed name.
    playerHealth = 100 #reset the player health back to 100
    status = "To start a round, click the bottom white button."
    
    #recycler's attributes
    recyclerX = [] #number of recyclers, and their x position.
    recyclerY = []
    recyclerPic = [] #the picture to be used for recycler
    recyclerHealth = [] #really only needed for tier 2 recycler
    recyclerDamage = [] #how much damage each recycler does to the health of the eWaste
    recyclerStatus = [] #0 if sold, 1 if not sold.
    recyclerTier = [] #tier 1 does not block the e-waste, tier 2 repels / blocks the e-waste but has a health / is disposable
    recyclerSellPrice = []
    
    #e-waste's attributes
    eWasteX = [] #x-position of the e-waste's
    eWasteY = [] #y-position
    eWasteHealth = [] #ewaste health
    eWasteDamage = [] #the damage the e-waste deals to player
    eWastePic = []
    eWasteColor = []
    eWasteStatus = []
    eWasteCoinDrop = []
    eWasteSpeed = []
    
    scoreboardList = [] #reset the scoreboardList's length to 0. Otherwise, when scoreboardMenu() is called, if won't display a scoreboard as it's dependant on it's length being 0.
    

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)
mixer.pre_init(44100, -16, 1, 512)
init()
SIZE = (1000, 700)
screen = display.set_mode(SIZE)
display.set_caption("Recyclers vs. E-Waste") #caption
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
myClock = time.Clock()
smallFont = font.SysFont("Arial", 18)
mediumFont = font.SysFont("Arial", 24)
largeFont = font.SysFont("Arial", 36)

#visuals
menuPic = image.load("images\\menu.png").convert_alpha()
titlePic = image.load("images\\title.png").convert()
pathPic = image.load("images\\path.png").convert_alpha()
floorPic = image.load("images\\floor.png").convert()
recyclerTier1Pic = image.load("images\\recycling.jpg").convert()
recyclerTier2Pic = image.load("images\\recyclingTier2.png").convert()
tier1Pic = image.load("images\\tier1.png").convert_alpha()
tier2Pic = image.load("images\\tier2.png").convert()
tier3Pic = image.load("images\\tier3.png").convert()
scoreboardPic = image.load("images\\scoreboard.png").convert()
tutorialPic = image.load("images\\tutorial.png").convert()

#sounds
machineGrinding = mixer.Sound("sounds/machineGrinding.wav") #recycler reaching end
ironClang = mixer.Sound("sounds/ironClang.wav") #placing recycler
ping = mixer.Sound("sounds/ping.wav") #e-waste recycled
thud = mixer.Sound("sounds/thud.wav") #selling recycler
victory = mixer.Sound("sounds/victory.wav") #reaching scoreboard
error = mixer.Sound("sounds/error.wav") #when the user places a recycler where there already is one
hint = mixer.Sound("sounds/hint.wav") #when the user presses a button
click = mixer.Sound("sounds/click.wav")
theme = mixer.Sound("sounds/theme.wav")

#states and initializing conditions
running = True
game = False 
menu = True
tutorial = False
scoreboard = False
started = True
placeRecyclerTier1 = False #used for placing tier 1 recycler
placeRecyclerTier2 = False #used for placing tier 2 recycler
sellRecycler = False
roundStarted = False #if a round / wave / match is started.
generateEnemies = False
roundNumber = 0
usersPlace = 0

#global mouse x and y position
mx = 0
my = 0
hoverX = 0
hoverY = 0
indexForRecyclerPlacementCheck = -1
playerHealth = 100
greenCoins = 50 #this is the currency / coin system
score = 0
autoStart = -1 #if -1, next round won't automatically start. if 1, next round will.

#recycler's attributes
recyclerX = [] #number of recyclers, and their x position.
recyclerY = []
recyclerPic = [] #the picture to be used for recycler
recyclerHealth = [] #really only needed for tier 2 recycler
recyclerDamage = [] #how much damage each recycler does to the health of the eWaste
recyclerStatus = [] #0 if sold, 1 if not sold.
recyclerTier = [] #tier 1 does not block the e-waste, tier 2 repels / blocks the e-waste but has a health / is disposable
recyclerSellPrice = []

#e-waste's attributes
eWasteX = [] #x-position of the e-waste's
eWasteY = [] #y-position
eWasteHealth = [] #ewaste health
eWasteDamage = [] #the damage the e-waste deals to player
eWastePic = []
eWasteColor = []
eWasteStatus = []
eWasteCoinDrop = []
eWasteSpeed = []

scoreboardList = []

playerName = ""
status = "To start a round, click the bottom white button."

theme.play() #plays the theme for when the player launches the game

#entire loop
while running:
    if menu == True:
        mainMenu()
    elif tutorial == True:
        tutorialMenu()
    elif game == True:
        gameMenu()
    elif scoreboard == True:
        scoreboardMenu()
    
    userEvents()
    myClock.tick(60)
    display.flip()
quit()

#added resetVariables function so that when the user goes back to mainMenu from scoreboardMenu, the game is started fresh.
#add a text that appears at the top of the screen, so that shows the score you got and your placement.
#allowed the user to click on the buttons again to disable.