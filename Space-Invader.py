import pygame
import pygame_gui
import math
import random
import time
from pygame import mixer


# note: player speed and enemy speed depends on you

pygame.init()

# create screen and font for texts
screen = pygame.display.set_mode((800,600))
Font = pygame.font.Font('freesansbold.ttf', 80)

# create a name-input bar
CLOCK = pygame.time.Clock()
MANAGER = pygame_gui.UIManager((800,600))
TEXT_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((200, 100),(400, 50)), manager = MANAGER, object_id = "#main_text_entry")

# create button
class Button():
    # assigns datas into constructor
    def __init__(self, image, pos, textInput, font, color, hoveringColor):
        self.image = image
        self.xPos = pos[0]
        self.yPos = pos[1]
        self.font = font
        self.color = color
        self.hoveringColor = hoveringColor
        self.textInput = textInput
        self.text = self.font.render(self.textInput, True, self.color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center = (self.xPos, self.yPos))
        self.textRect = self.text.get_rect(center = (self.xPos, self.yPos))

    # update text or image
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)

    # check position of mouse with position of button    
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    # formatting color of buttons
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.textInput, True, self.hoveringColor)
        else:
            self.text = self.font.render(self.textInput, True, self.color)



# background
background = pygame.image.load('background.jpg')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# caption and icon
pygame.display.set_caption('Space Inavder')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# display text
def displayText(text,size,x,y):
    texts = pygame.font.Font("freesansbold.ttf",size).render(text, True, "White")
    screen.blit(texts, (x,y))
    
# display player
def player(x,y):
    playerShip = pygame.image.load('Player.png')
    screen.blit(playerShip,(x,y))

# display enemy
def enemy(x,y,enemyShip):
    screen.blit(enemyShip,(x,y))

# display bullet
def fireBullet(x,y):
    bullet = pygame.image.load('bullet.png')
    screen.blit(bullet, (x+16,y+10))

def enemyKilled(x,y):
    explosion = pygame.image.load('explosion.png')
    screen.blit(explosion, (x,y))

# check if a bullet hits an enemy
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27:
        enemyKilled(enemyX,enemyY)
        return True
    else:
        return False

# play the game
def play(username):
    username = username
    score = 0

    # player
    playerX = 370
    playerY = 520
    playerX_change = 0

    # enemy
    numEnemies = 5
    enemyShip = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    # create multiple enemies
    for i in range(numEnemies):
        enemyShip.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(40,720))
        enemyY.append(random.randint(40,120))
        enemyX_change.append(1)

    # bullet 
    bulletX = 0
    bulletY = 480
    bulletState = "Ready"

    run = True
    while run:
        screen.fill("Black")
        screen.blit(background,(0,0))
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -1
                if event.key == pygame.K_RIGHT:
                    playerX_change = 1
                if event.key == pygame.K_SPACE:
                    if bulletState == "Ready":
                        bulletSound = mixer.Sound('laser.wav')
                        bulletSound.play()
                        bulletX = playerX
                        fireBullet(bulletX,bulletY)
                        bulletState = "Fire"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
    
        # player movement
        playerX += playerX_change
        if playerX < 0:
            playerX = 0
        elif playerX > 730:
            playerX = 730

        # bullet movement
        if bulletState == "Fire":
                fireBullet(bulletX,bulletY)
                bulletY -= 3
        if bulletY <= 0:
            bulletY = 480
            bulletState = "Ready"

        # enemy movement
        for i in range(numEnemies):

            # gameover
            if enemyY[i] > 460:
                for j in range(numEnemies):
                    enemyY[j] = 2000
                    playerY = 2000
                    run = showGameOver(score, username)
                    if run == False:
                        return True
                    else:
                        return False

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 1
                enemyY[i] += 40
            elif enemyX[i] >= 780:
                enemyY[i] += 40
                enemyX_change[i] = -1

        #collision
            if bulletState == "Fire": 
                collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
                if collision:
                    enemyKilled(enemyX[i],enemyY[i])
                    time.sleep(0.02)
                    explosionSound = mixer.Sound('explosion.wav')
                    explosionSound.play()
                    bulletY = 480
                    bulletState = "Ready" 
                    score += 1
                    enemyX[i] = random.randint(40,720)
                    enemyY[i] = random.randint(40,120)
            enemy(enemyX[i],enemyY[i],enemyShip[i])
            

        player(playerX,playerY)
        displayText(text = "Score:" + str(score),size = 32, x = 10, y = 10)
        pygame.display.update()

def showScoreList():
    run = True
    while run:
        menuMousePos = pygame.mouse.get_pos() 
        screen.fill("black")
        screen.blit(background,(0,0))

        # read usernames and scores from file
        scoreList = open("scorelist.txt", "r")
        Lines = scoreList.readlines()
        count = 0
        lineY = 150

        # making a leaderboard
        # Strips the newline character
        displayText(text = "LEADERBOARD", size = 32, x = 100, y = 100)
        for line in Lines:
            count +=1 
            L = (format(line.strip()))
            displayText(text = L, size = 32, x = 100, y = lineY)
            lineY += 40
            if count == 10:
                break

        scoreList.close()

        # create a return-menu button
        backButton = Button(image = None, pos = (400, 550), textInput = "BACK", font = Font, color = "White", hoveringColor = "Blue")
        for button in [backButton]:
            button.changeColor(menuMousePos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.checkForInput(menuMousePos):
                    return True
        pygame.display.update()

def showGameOver(score, username):
    
    #store username and score into file
    username = username
    scoreList = open("scorelist.txt", "a")
    scoreList.write(username + " : "+ str(score) + "\n")
    scoreList.close()

    run = True
    while run:
        menuMousePos = pygame.mouse.get_pos()
        screen.fill("black") 
        screen.blit(background,(0,0))

        # display Game-Over text
        displayText(text = "GAME OVER!", size = 64, x = 200, y = 200)

        # create retry and return-menu buttons
        retryButton = Button(image = None, pos = (400, 400), textInput = "RETRY", font = Font, color = "White", hoveringColor = "Blue")
        backButton = Button(image = None, pos = (400, 500), textInput = "BACK", font = Font, color = "White", hoveringColor = "Blue")
        for button in [retryButton,backButton]:
            button.changeColor(menuMousePos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retryButton.checkForInput(menuMousePos):
                    play(username)
                if backButton.checkForInput(menuMousePos):
                    return False
        pygame.display.update()

nameInput = False
username = "empty"

running = True
while running:
        menuMousePos = pygame.mouse.get_pos()
        screen.fill("Grey")
        screen.blit(background, (0,0))
        rate = CLOCK.tick(60)/1000

        # create play, score and quit buttons
        playButton = Button(image = None, pos = (400, 250), textInput = "PLAY", font = Font, color = "White", hoveringColor = "Blue")
        scoreButton = Button(image = None, pos = (400, 350), textInput = "SCORE", font = Font, color = "White", hoveringColor = "Blue")
        quitButton = Button(image = None, pos = (400, 450), textInput = "QUIT", font = Font, color = "White", hoveringColor = "Blue")
        for button in [playButton,scoreButton,quitButton]:
            button.changeColor(menuMousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.checkForInput(menuMousePos):

                    # check if player enter a name or not
                    # if not, set default name for player to Unknown
                    if nameInput == False:
                        username = "Unknown"
                    running = play(username)
                if scoreButton.checkForInput(menuMousePos):
                    running = showScoreList() 
                if quitButton.checkForInput(menuMousePos):
                    running = False

            # name-input bar        
            if username == "empty":
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                    username = event.text
                    nameInput = True
                    MANAGER = False
                    
        if username == "empty":
            MANAGER.process_events(event)
            MANAGER.update(rate)
            MANAGER.draw_ui(screen)

        # display player name
        if nameInput == True:
            displayText(text = username, size = 32, x = 200, y = 100)
        pygame.display.update()




    