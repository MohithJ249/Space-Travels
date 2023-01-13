import pygame 
import random
import math
from pygame import mixer
import cv2
import mediapipe as mp
import pyautogui


# initialize pygame
pygame.init()

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_x, index_y = 0, 0

# create the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Background 
background = pygame.image.load("background.jpeg")
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
    ret, frame = cap.read()
    
    # this is to flip the frame on y-axis (indicated by 1) because
    # in this way, if I move my hand to the right, the frame shows the same thing
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hand_landmarks = output.multi_hand_landmarks
    
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
        
    if(hand_landmarks):
        for landmarksInFrame in hand_landmarks:
            drawing_utils.draw_landmarks(frame, landmarksInFrame)
            landmarks = landmarksInFrame.landmark
            for id, landmark in enumerate(landmarks):
                
                # the x and y coordindates are in fraction form of the opencv frame
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                
                # 8 indicates the tip of the index finger
                if(id == 8):
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0,255,255))
                    # this will scale the mouse movement to whole computer window instead
                    # of having it move within the opencv frame's resolution
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    pyautogui.moveTo(index_x, index_y)
       
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)             
        
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