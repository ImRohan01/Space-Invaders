import pygame
import random
import math
from pygame import mixer

#Initializing the pygame module. Mandatory whenenver we create a game.
pygame.init()
#Creating a game screen
screen = pygame.display.set_mode((800,600))
#Setting the icon
icon = pygame.image.load('img/player.png')
pygame.display.set_icon(icon)
#Sets the title for our window
pygame.display.set_caption('Space Invaders')

#Setting background for window
background = pygame.image.load('img/bkg.png').convert()
mixer.music.load("sounds/background.wav")
mixer.music.play(-1)

#Score Manager Code
score = 0
font = pygame.font.Font("Gameplay.ttf",32)
textX = 10
textY = 10

#GameOver Handler
gameOverFont = pygame.font.Font("Gameplay.ttf",64)
gameOverX = 200
gameOverY = 250

#Creating the player
playerImg = pygame.image.load('img/player.png')
playerX = 336
playerY = 480
playerXchange = 0
playerYchange = 0

#Creating the enemy
num_of_enemies = 6
enemyImg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('img/enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyXchange.append(1.8)
    enemyYchange.append(15)

#Creating the bullet
#Ready - Bullet not on screen
#Fire - Bullet on screen
bulletImg = pygame.image.load('img/bullet.png')
bulletX = playerX
bulletY = playerY
bulletXchange = 0
bulletYchange = 10
bulletState = "ready"

#Let's create our functions in this space
def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((enemyX-bulletX)**2 + (enemyY-bulletY)**2)
    if distance<27:
        return True
    return False

def showScore(x,y):
    score_value = font.render("SCORE : " + str(score), True, (255,255,255))
    screen.blit(score_value, (x,y))

def game_over(x,y):
    gameOverValue = gameOverFont.render("GAME OVER", True, (255,255,255))
    screen.blit(gameOverValue, (x,y))

while True:
    #Screen background color
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    #Iterates through all events and if quit is matched then exits the program.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        #Handling movements on pressed key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left key was pressed!")
                playerXchange = -1
            if event.key == pygame.K_RIGHT:
                print("Right key was pressed!")
                playerXchange = 1
            if event.key == pygame.K_SPACE and bulletState is "ready":
                bulletSound = mixer.Sound("sounds/laser.wav")
                bulletSound.play()
                print("Bullet was fired!")
                bulletX = playerX
                fire_bullet(bulletX,bulletY)
        #Handling movements on released key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerXchange = 0
                print("Arrow key is released")
    #Coordinates are updated
    playerX += playerXchange
    playerY += playerYchange
    #Staying within the limits of the window
    if playerX<=0:
        playerX = 0
    if playerX>=736:
        #736 because the size of the image is 64px
        playerX = 736
    #This time for the enemy
    for i in range(num_of_enemies):
        if enemyY[i] > 420:
            for j in range(num_of_enemies):
                enemyX[j] = 2000
            game_over(gameOverX,gameOverY)
            break
        if enemyX[i]<=0:
            enemyX[i] = 0
            enemyXchange[i] = 1.8
            enemyY[i] += enemyYchange[i]
        if enemyX[i]>=736:
            enemyX[i] = 736
            enemyXchange[i] = -1.8
            enemyY[i] += enemyYchange[i]
        #Collision
        if isCollision(enemyX[i],enemyY[i],bulletX,bulletY):
            explosionSound = mixer.Sound("sounds/explosion.wav")
            explosionSound.play()
            bulletY = playerY
            bulletState = "ready"
            score += 1
            print("Score" + str(score))
            #respawn the enemy
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        enemyX[i] += enemyXchange[i]
        enemy(enemyX[i],enemyY[i],i)
    #Firing the bullets
    if bulletY <= 0:
        bulletY = playerY
        bulletState = "ready"
    if bulletState is "fire":
        bulletY -= 2
        fire_bullet(bulletX,bulletY)

    player(playerX,playerY)
    showScore(textX,textY)
    #Update the display. Always at the end of the for loop.
    pygame.display.update()
