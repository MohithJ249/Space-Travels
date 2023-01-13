import pygame 
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Background 
background = pygame.image.load("background.jpg")
resized_background = pygame.transform.scale(background, (SCREEN_WIDTH,SCREEN_HEIGHT))

# Title and Icom
pygame.display.set_caption("Space Travels")
icon = pygame.image.load("space-suit.png")
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load("spaceship.png")
playerX = 400
playerY = 300
playerX_change = 0


# Asteroids
asteroidImgs = []
asteroidX = []
asteroidY = []
asteroidX_change = []
# might not need for now
# asteroidY_change = []
totalAsteroids = 5
numAsteroidsOnScreen = 0

    
    
# Score - use seconds so score is on how long a player lasted
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
FPS = 60

def show_score(x, y, timeNow=None):
    global score_value
    if(timeNow):
        score_value = timeNow - start_time
    score = font.render("Score: " + str(math.floor(score_value/1000)), True, (255,255,255))
    screen.blit(score, (x, y))


def game_over():
    over_text = over_font.render("Game Over", True, (255,255,255))
    screen.blit(over_text, (200, 250))
    
def player(x, y):
    screen.blit(playerImg, (x, y))

def asteroid_spawn():
    asteroidImgs.append(pygame.image.load("asteroid.png"))
    # want the asteroid to start from the right-most side
    asteroidX.append(736)
    # 536 because then asteroid doesn't go off bounds y-axis way
    # window SCREEN_HEIGHT = 600 but asteroid is 64x64, so max is 600-64=536
    asteroidY.append(random.randint(0, 536))
    asteroidX_change.append(-5)
    # asteroidY_change.append(0)
    # screen.blit(asteroidImgs[i], (x, y))
    
def isCollision(asteroidX, asteroidY, playerX, playerY):
    distance = math.sqrt( math.pow(playerX - asteroidX, 2) + math.pow(playerY - asteroidY, 2))
    
    return distance < 30    


# define game variables
background_width = background.get_width()
tiles = math.ceil((SCREEN_WIDTH / background_width)) + 1
scroll = 0
pygame.time.set_timer(pygame.USEREVENT, 1000) # 1 second

# Game Loop
running = True
gameOverTimer = False

while running:
    clock.tick(FPS)
    screen.fill((0,0,0))
    
    for i in range(tiles):
        screen.blit(resized_background, (i * background_width + scroll,0))
        
    # scroll background
    scroll -= 5
    
    # reset scroll
    if(abs(scroll) > background_width):
        scroll = 0
    
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        if(event.type == pygame.USEREVENT):
            if(numAsteroidsOnScreen < totalAsteroids):
                numAsteroidsOnScreen += 1
                asteroid_spawn()
        
    mx, my = pygame.mouse.get_pos()
    playerX = mx
    playerY = my
    
    if(playerX <= 0):
        playerX = 0
    elif(playerX >= SCREEN_WIDTH - 64):
        playerX = SCREEN_WIDTH - 64
    
    if(playerY <= 0):
        playerY = 0
    elif(playerY >= SCREEN_HEIGHT - 64):
        playerY = SCREEN_HEIGHT - 64
        
    
    # asteroid movement
    # collision = False
    for i in range(numAsteroidsOnScreen):
        # print(i, numAsteroidsOnScreen, asteroidX, asteroidY)
        screen.blit(asteroidImgs[i], (asteroidX[i], asteroidY[i]))
        if(asteroidY[i] > 1000):
            game_over()
            break
    
        asteroidX[i] += asteroidX_change[i]
        # asteroid_spawn(asteroidX[i], asteroidY[i], i)
        
        if(asteroidX[i] <= 0):
            asteroidX[i] = 736
            asteroidY[i] = random.randint(0, SCREEN_HEIGHT)
            
        # Collision detection
        collision = isCollision(asteroidX[i], asteroidY[i], playerX, playerY)
        if(collision):
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            for j in range(numAsteroidsOnScreen):
                asteroidY[j] = 2000
            gameOverTimer = True
            
        
    # displaying player
    player(playerX,playerY)
      
    # show score
    if(not gameOverTimer):
        timeNow = pygame.time.get_ticks()
        show_score(textX, textY, timeNow)
    else:
        show_score(textX, textY)
    
    pygame.display.update()
    

# pygame.quit()    