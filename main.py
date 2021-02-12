import pygame
import math
import random
from pygame import mixer

pygame.init()

#creating screen
screen = pygame.display.set_mode((800,600))
backGround = pygame.image.load('Pictures/892.jpg')
mixer.music.load('Musics/background.wav')
mixer.music.play(-1)

#title & icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Pictures/spaceship.png')
pygame.display.set_icon(icon)

#player
playerimg = pygame.image.load('Pictures/ufo.png')
playerx = 364
playery = 480
playerx_change = 0

#enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
numOfEnemies = 5

for i in range(numOfEnemies):
    enemyimg.append(pygame.image.load('Pictures/coronavirus.png')) 
    enemyx.append(random.randint(0, 735)) 
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(0.3)
    enemyy_change.append(40) 

#vaccine
vaccineimg = pygame.image.load('Pictures/syringe.png')
vaccinex = 0
vacciney = 480
vaccinex_change = 0
vacciney_change = 0.7
vaccine_state = "ready"

#Score
score = 0
font = pygame.font.Font('design.graffiti.comicsansmsgras.ttf', 32)

textX = 600
textY = 10

#Game over text
gOFont = pygame.font.Font('design.graffiti.comicsansmsgras.ttf', 64)

def player(x,y):
    screen.blit(playerimg, (x,y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x,y))

def vaccineShoot(x, y):
    global vaccine_state
    vaccine_state = "shot"
    screen.blit(vaccineimg, (x + 16, y + 10))

def isCollision(vaccinex, vacciney, enemyx, enemyy):
    distance = math.sqrt((math.pow(vaccinex - enemyx, 2)) + (math.pow(vacciney - enemyy, 2)))
    if(distance < 27):
        return True
    else:
        return False

def showScore(x, y):
    scoreString = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scoreString, (x, y))

def gameOver():
    gOString = gOFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gOString, (200, 250))


#game loop
running = True
while running:
    #background
    screen.fill((0, 0, 0))
    screen.blit(backGround, (0, 0))

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
   
   #if keystroke is pressed:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.3
            if event.key == pygame.K_SPACE:
                vaccine_sound = mixer.Sound('Musics/laser.wav')
                vaccine_sound.play()
                if vaccine_state == "ready":
                    vaccinex = playerx
                    vaccineShoot(vaccinex, vacciney)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
            
       

                
    
    #checking boundaries for player
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    #enemy movement
    for i in range(numOfEnemies):

        if enemyy[i] > 440:
            for j in range(numOfEnemies):
                enemyy[j] = 2000
            gameOver()
            pygame.mixer.music.stop()
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.3
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.3
            enemyy[i] += enemyy_change[i]

        #Collision
        collision = isCollision(vaccinex, vacciney, enemyx[i], enemyy[i])
        if collision:
            collision_sound = mixer.Sound('Musics/explosion.wav')
            collision_sound.play()
            vacciney = 480
            vaccine_state = "ready"
            score += 1
            print(score)
            enemyx[i] = random.randint(0, 735)
            enemyy[i] =random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    #vaccine movement
    if vacciney <= 0:
        vacciney = 480
        vaccine_state = "ready"

    if vaccine_state == "shot":
        vaccineShoot(vaccinex, vacciney)
        vacciney -= vacciney_change


    

    player(playerx, playery)
    showScore(textX, textY)
    pygame.display.update()

