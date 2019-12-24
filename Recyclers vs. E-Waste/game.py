#Summative

#make a game that's similar to plants vs zombies
#The "zombies" going in the pathway are the non enviormentally recycled electronics
#What the user has to do is place good guys (recyclers) on the pathways, which recycles the electornic waste from reaching the end of the production plant. (end of the path)
#the enemies will go inside them (colide) and they lose health, but if they reach the end of the path sucessfully then the player loses health.
#each stage will use randomness to decide which enemies (e-waste) will be placed / go through the pathway?
from pygame import*

def gameMenu(): #game
    enemiesMoving()
    

def enemiesMoving(): #will have feature to randomly select different levels of enemies soon.
    global playerHealth
    enemyHealth = 100
    for i in range(950):
        draw.rect(screen, BLACK, (0, 0, 1000, 700))
        draw.rect(screen, WHITE, (0, 300, 1000, 100))
        draw.rect(screen, BLUE, (i, 325, 50, 50))
        time.wait(5)
        display.flip()
        userEvents()
        
        #some code saying if the enemy colides with a recycler, lose health
        #some code saying that if enemy health reaches 0, break out of loop
        
        #code saying if the enemy reaches the end of the path, reduce player health
        if i == 949:
            playerHealth -= 10
            print(playerHealth)
    

#We use this as a seperate function to clear up code. This also allows us to use input when the enemyMoving function is running
def userEvents():
    #if the user does not drags the window do the lines of code below
    for evnt in event.get():
        if evnt.type == MOUSEBUTTONDOWN:
            print("clk")


init()
SIZE = (1000, 700)
screen = display.set_mode(SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
myClock = time.Clock()

running = True
game = True #we haven't created a main menu yet, so set this to true for now.
started = True

playerHealth = 100

while running:
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
    if game == True:
        gameMenu()

    myClock.tick(60)
quit()
