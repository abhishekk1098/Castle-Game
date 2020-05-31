# Import Library ------------------>
import SoundEffects as sounds      # User Defined File
import pygame
import math
import random
from pygame.locals import *
# --------------------------------->

# Initialize the game ------------->
pygame.init()
infoObject = pygame.display.Info()
width,height = infoObject.current_w,infoObject.current_h
print(width)
screen = pygame.display.set_mode((width-100,height-200))
pygame.display.set_caption('DEFEND THE CASTLE')
# --------------------------------->


# Initialize Warrior Position ------->
keys = [False, False, False, False]
warriorpos=[180,200]
# ----------------------------------->

# Initialize Arrow Array ------------>
acc = [0,0]
arrows = []
# ----------------------------------->

# Initialize Enemies ---------------->
badtimer  = 100
badtimer1 = 0
enemy = [[width - 100 , 100]]
healthvalue = 194
# ----------------------------------->


# Load Images ----------------------->
## 1 - Warrior
warrior = pygame.image.load("resources/images/warrior1.png")
warrior = pygame.transform.scale(warrior, (120, 160))
## 2 - Grass
grass   = pygame.image.load("resources/images/grass.png")
## 3 - Castle
castle  = pygame.image.load("resources/images/castle1.png")
castle  = pygame.transform.scale(castle, (150, 120))
## 4 - Arrow
arrow = pygame.image.load("resources/images/bullet.png")
## 5 - Enemy
enemy1img = pygame.image.load("resources/images/enemy.png")
enemy1img = pygame.transform.scale(enemy1img, (60, 60))
enemyimg  = enemy1img
## 6 - HealthBar
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
## 7 - Win Background
youwin = pygame.image.load("resources/images/youwin.png")
youwin = pygame.transform.scale(youwin,(width-100,height-200))
## 8 - Lose Background
gameover = pygame.image.load("resources/images/gameover.png")
gameover = pygame.transform.scale(gameover,(width-100,height-200))
# # ----------------------------------->

# Dispay Text on Screen --------------->

## Castle Health
pygame.font.init()
font = pygame.font.Font(None, 24)
castleHealth = font.render("Castle Health : ", True, (0,0,0))
castleHealthRect = castleHealth.get_rect()
castleHealthRect.x=935
castleHealthRect.y=10

## Remaining Time
pygame.font.init()
font = pygame.font.Font(None, 24)
clk = font.render("Time Left : ", True, (0,0,0))
clkRect = clk.get_rect()
clkRect.x=970
clkRect.y=40

# ------------------------------------->


# ADD EVENT HANDLERS ---------------->
## KEYDOWN
def keyDown():
    if event.key==K_w:
        keys[0]=True
    elif event.key==K_a:
        keys[1]=True
    elif event.key==K_s:
        keys[2]=True
    elif event.key==K_d:
        keys[3]=True

## KEYUP
def keyUp():
    if event.key==pygame.K_w:
        keys[0]=False
    elif event.key==pygame.K_a:
        keys[1]=False
    elif event.key==pygame.K_s:
        keys[2]=False
    elif event.key==pygame.K_d:
        keys[3]=False

## MOUSECLICK
def onClick():
    sounds.shoot.play()
    position=pygame.mouse.get_pos()
    acc[1]+=1
    arrows.append([math.atan2(position[1]-(warriorpos1[1]+66),position[0]-(warriorpos1[0]+66)),warriorpos1[0]+60,warriorpos1[1]+60])
# # ----------------------------------->


# ALL FUNCTIONS ----------------------->

## Function to draw Elements on Screen
def drawElements():
    # Draw Grass in Background
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))
    
    # Draw Four Castle
    screen.blit(castle,(0,30))
    screen.blit(castle,(0,160))
    screen.blit(castle,(0,290))
    screen.blit(castle,(0,420))

## Function to Set Position of Warrior
def warriorPosition():
    global warriorpos1         ## We have made it global coz we are using inside onClick() function

    # Set Warrior Position and Rotation based on mouse movement
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(warriorpos[1]-38),position[0]-(warriorpos[0]-32))
    warriorrot = pygame.transform.rotate(warrior, 360-angle*57.29)
    warriorpos1 = (warriorpos[0]-warriorrot.get_rect().width//2, warriorpos[1]-warriorrot.get_rect().height//2)

    # Draw Warrior
    screen.blit(warriorrot, warriorpos1)

## Function to Shoot Arrows
def shootArrow():
    for bullet in arrows:
        index=0
        # The vely and velx values are calculated using basic trigonometry. 10 is the speed of the arrows.
        velx=math.cos(bullet[0])*20
        vely=math.sin(bullet[0])*20
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>(width - 100) or bullet[2]<-64 or bullet[2]>(height - 200):
            arrows.pop(index)
        index+=1
        # Trajectory of Arrows
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))

## Function to Add Enemies and "Kill" Enemies
def plotEnemy():
    global badtimer,badtimer1,healthvalue
    if badtimer==0:
        # Add Random Position of Enemies
        enemy.append([width - 100, random.randint(80,height - 250)])
        badtimer=100-(badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
    index=0
    for badguy in enemy:
        if badguy[0]<-64:
            enemy.pop(index)
        badguy[0]-=5

        # Reduce health of Castle if Enemy Attack
        badrect=pygame.Rect(enemyimg.get_rect())
        badrect.top=badguy[1]
        badrect.left=badguy[0]
        if badrect.left<64:
            sounds.hit.play()
            healthvalue -= random.randint(5,20)
            enemy.pop(index)

        # Kill Enemy (if shot by arrow)
        index1=0
        for bullet in arrows:
            bullrect=pygame.Rect(arrow.get_rect())
            bullrect.left=bullet[1]
            bullrect.top=bullet[2]
            # Inbuilt pygame function "badrect.colliderect" that checks for intersection
            if badrect.colliderect(bullrect):
                sounds.enemy.play()
                acc[0]+=1
                enemy.pop(index)
                arrows.pop(index1)
            index1+=1

        # Next Enemy
        index+=1

    # Build Enemy on Screen
    for badguy in enemy:
        screen.blit(enemyimg, badguy)

## Function to create Clock
def clock():
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(str((90000-pygame.time.get_ticks())//60000)+":"+str((90000-pygame.time.get_ticks())//1000%60).zfill(2), True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright=[1094,40]
    screen.blit(survivedtext, textRect)

## Function to Create Health Bar
def healthBar():
    screen.blit(healthbar, (1060,8))
    for health1 in range(healthvalue):
        screen.blit(health, (health1+1063,11))

# ----------------------------------->

# Setup The Gameplay----------------->
running = 1
exitcode = 0
while running:
    # Each Time the badtimer is reduced
    badtimer-=1

    # clear screen on start(each time we start game)
    background_color = (0,0,0)
    screen.fill(background_color)

    # Draw Elements on Screen
    drawElements()

    # Set Warrior Position
    warriorPosition()

    # Draw Arrows
    shootArrow()

    # Plot Enemies and Kill Enemy
    plotEnemy()

    # Generate Timer to be displayed on the Screen
    screen.blit(clk, clkRect)
    clock()

    # Create Health Bar and display Text
    screen.blit(castleHealth, castleHealthRect)
    healthBar()

    # Update the screen
    pygame.display.flip()

    # Looping Through Events
    for event in pygame.event.get():
        # close window
        if event.type == pygame.QUIT:
            running = 0
            pygame.quit()
            exit(0)
        
        if event.type == pygame.KEYDOWN:
            keyDown()

        if event.type == pygame.KEYUP:
            keyUp()

        if event.type == pygame.MOUSEBUTTONDOWN:
            onClick()
    
    # Move player
    if keys[0]:
        warriorpos[1]-=5
    elif keys[2]:
        warriorpos[1]+=5
    if keys[1]:
        warriorpos[0]-=5
    elif keys[3]:
        warriorpos[0]+=5

    # Win/Lose check
    if pygame.time.get_ticks() >= 90000:
        running  = 0
        exitcode = 1
    if healthvalue<=0:
        running  = 0
        exitcode = 0
    if acc[1] != 0:
        accuracy = acc[0] / acc[1]
    else:
        accuracy = 0

# ----------------------------------->

# Display Win/Lose Display Screen --->

## Win Condition
if exitcode == 0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: {:.2f}%".format(accuracy*100), True, (0,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)

## Lose Condition
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: {:.2f}%".format(accuracy*100), True, (0,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)

# Exit Condition Check
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()

