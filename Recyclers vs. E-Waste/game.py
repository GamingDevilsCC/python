#Summative

#make a game that's similar to plants vs zombies
#The "zombies" going in the pathway are the non enviormentally recycled electronics
#What the user has to do is place good guys (recyclers) on the pathways, which recycles the electornic waste from reaching the end of the production plant. (end of the path)
#the enemies will go inside them (colide) and they lose health, but if they reach the end of the path sucessfully then the player loses health.
#each stage will use randomness to decide which enemies (e-waste) will be placed / go through the pathway?

from pygame import*
import os

def gameMenu(): #game
    #track
    draw.rect(screen, BLACK, (0, 0, 1000, 700))
    draw.rect(screen, WHITE, (0, 300, 1000, 100))
    
    #the e-waste and recyclers
    enemiesMoving()
    
#animation for the e-waste moving through the screen.
def enemiesMoving(): #will have feature to randomly select different levels of enemies soon.
    global playerHealth
    global recyclerX
    global roundStarted #not used now, may implement later
    
    #electronic waste          
    for eWaste in range(len(eWasteX)): #how many e-waste enemies there are. nested loop because of enemyHealth requiring information from machine
        draw.rect(screen, BLUE, (eWasteX[eWaste], 325, 50, 50))
        modifyButton = smallFont.render(str(eWasteHealth[eWaste]), 1, WHITE)
        screen.blit(modifyButton, Rect(eWasteX[eWaste] + 5, 330, 0, 0)) #e-waste health
        eWasteX[eWaste] += 1 #increase the x position of e-waste 10 units to the right.       
    
    #recyclers
    for machine in range(len(recyclerX)): #how many recyclers there are.                    
        draw.rect(screen, GREEN, (recyclerX[machine], 325, 50, 50)) #Only the x value is set. This way when a user places one down, it doesn't look out of place.
    
    #Damage protocol, used for determining colision and ewaste/player health. If ewaste reaches the end or is out of health, it gets removed from the  
    for machine in range(len(recyclerX)):
        for eWaste in range(len(eWasteX)):
            if eWasteX[eWaste] == recyclerX[machine]: #if the e-waste colides with a recycler, the e-waste loses 10 health
                eWasteHealth[eWaste] -= 10
                if eWasteHealth[eWaste] <= 0: #if the health of the e-waste is dead, delete it from list
                    del eWasteX[eWaste]
                    del eWasteHealth[eWaste]
            #code saying if the enemy reaches the end of the path, reduce player health
            elif eWasteX[eWaste] == 950: #if the e-waste the end of the path. it's 50 pixels wide, so 950 instead of 1000.
                playerHealth -= 10
                print(playerHealth)
                del eWasteX[eWaste]
                del eWasteHealth[eWaste]          
    
    time.wait(5)
    display.flip()
    userEvents()
    recycler()

#This is the function that finds where the user wants to place the recycler.
def recycler():
    global mx, my
    
    if placeRecycler == True and (mx and my) != 0: #These are temporary parameters for now while the game is being developed.
        recyclerX.append(mx)
        recyclerDamage.append(10) #this is level 1 damage that recycler does to e-waste
        mx = 0
        my = 0

#We use this as a seperate function to clear up code.
def userEvents():
    global mx, my
    #if the user does not drags the window do the lines of code below
    for evnt in event.get():
        if evnt.type == MOUSEBUTTONDOWN:
            mx, my = evnt.pos

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)   
init()
SIZE = (1000, 700)
screen = display.set_mode(SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
myClock = time.Clock()
smallFont = font.SysFont("Arial", 18)

running = True
game = True #we haven't created a main menu yet, so set this to true for now.
started = True
placeRecycler = True #true for now, used for placing recycler
roundStarted = True #if a round / wave / match is started. This is not used yet.

#global mouse x and y position
mx = 0
my = 0

playerHealth = 100

recyclerX = [] #number of recyclers, and their x position.
recyclerDamage = [] #how much damage each recycler does

eWasteX = [10] #initial x-position of the testing ewaste
eWasteHealth = [100] #ewaste health

#entire loop
while running:
    if game == True:
        gameMenu()

    myClock.tick(60)
quit()

