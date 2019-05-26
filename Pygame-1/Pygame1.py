#Pygame 1
#This is my first try at building a game

import pygame
from SpriteSheetClass import spriteSheet
from Projectile import projectile
from PlatformClass import platform

pygame.display.init()
pygame.display.set_caption("First Game")
clock = pygame.time.Clock()

fps = 30

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)

platforms = [platform(300,300,80,20,red),
			 platform(200,200,80,20,green),
			 platform(100,100,80,20,blue)]

screenWidth, screenHeight = 500, 500
screenLeftBound, screenRightBound = 50, 450
baseBoundary = 450

projectiles = []
projectileColor = black
projectileRadius = 10
projectileVelocity = 5
projectileDirection = 1

platformContact = False

playerPosition = {"x":100, "y":300}
currentPlayerPosition = {}
playerVelocity = 8
playerIndex = 0
playerStill = [0,8]
playerLeft, playerRight = [1,2,3,2],[9,10,11,10]
playerFall = [16,17,18,19,20,21,22,23,24,25,26,27]
playerJumpLeft, playerJumpRight = 5,13
isFacingLeft, isFacingRight = False, True
isJumping, isFalling = False, True
isMovingLeft, isMovingRight = False, False
jumpCount, fallCount = 10, 0
initJumpCount = jumpCount
walkCount = 0

player = spriteSheet("RainbowIslandsCharacter.png", 7, 4)
background = spriteSheet("bg.jpg",1,1)

window = pygame.display.set_mode((screenWidth,screenHeight))

def isInBound(player,x,direction='left'):
	global screenLeftBound
	global screenRightBound

	if direction == 'left':
		if x >= screenLeftBound:
			return True
		else:
			return False
	
	if direction == 'right':
		if x <= (screenRightBound - player.width):
			return True
		else:
			return False
	

run = True
contact = False
one, two, three = False, False, False
while run:
	#Saving current player position
	currentPlayerPosition['x'] = playerPosition['x']
	currentPlayerPosition['y'] = playerPosition['y']
	
	#Set max frame rate in fps
	clock.tick(fps)

	#Collect all keys pressed into a dictionary
	keys = pygame.key.get_pressed()

	#Exit Loop if close button or escape key pressed
	for event in pygame.event.get():
		if (event.type == pygame.QUIT) or keys[pygame.K_ESCAPE]:
			run = False

	#Checking if left key is pressed
	if keys[pygame.K_LEFT]:
		isFacingLeft, isFacingRight = True, False
		isMovingLeft, isMovingRight = True, False

		if isInBound(player,playerPosition["x"],'left'):
			playerPosition["x"] -= playerVelocity

			walkCount += 1
			if walkCount >= len(playerLeft) * 7:
				walkCount = 0

			playerIndex = playerLeft[walkCount//7]
		else:
			playerIndex = playerStill[0]

	#Checking if right key is pressed
	elif keys[pygame.K_RIGHT]:
		isFacingLeft, isFacingRight = False, True
		isMovingRight, isMovingLeft = True, False

		if isInBound(player,playerPosition["x"],'right'):
			playerPosition["x"] += playerVelocity
			
			walkCount += 1
			if walkCount >= len(playerRight) * 7:
				walkCount = 0

			playerIndex = playerRight[walkCount//7]
		else:
			playerIndex = playerStill[1]

	#If neither left nor right keys are pressed
	else:
		isMovingLeft, isMovingRight = False, False
		if isFacingLeft:
			playerIndex = playerStill[0]

		if isFacingRight:
			playerIndex = playerStill[1]

		walkCount = 0

	#Checking if up key is pressed
	if keys[pygame.K_UP] and not isJumping and not isFalling: 
		isJumping = True
		jumpCount = initJumpCount
		fallCount = 0

	#Checking if jumping, adjusting player's y position and player index
	if isJumping:
		if jumpCount > 0:
			playerPosition["y"] -= (jumpCount ** 2) * 0.5
			
			jumpCount -= 1
		else:
			isJumping, isFalling = False, True

		if isFacingLeft: playerIndex = playerJumpLeft
		if isFacingRight: playerIndex = playerJumpRight

	elif isFalling:

		playerPosition["y"] += (fallCount ** 2) * 0.5

		fallCount += 1

		if isFacingLeft: playerIndex = playerJumpLeft
		if isFacingRight: playerIndex = playerJumpRight

	else:
		fallCount = 0

	#Checking if space key is pressed
	if keys[pygame.K_SPACE]:
		if isFacingRight: projectileDirection = 1
		if isFacingLeft: projectileDirection = -1

		projectiles.append(projectile(playerPosition["x"], playerPosition["y"], projectileDirection, projectileVelocity))


	#!!!DRAW SECTION!!!
	
	#Drawing background
 	background.draw(window,0,0,0)

 	#Drawing platforms, checking if player has contacted platform
	for platform in platforms:
		platform.draw(window)

		if platform.isContact(playerPosition,player):
			platformContact = True

			#Checking if player contacted left side
			if ((currentPlayerPosition['x'] <= (platform.x - player.width)) and 
				((platform.y - player.height) < currentPlayerPosition['y'] < (platform.y + platform.height))):
				
				playerPosition['x'] = (platform.x - player.width)

			#Checking if player contacted right side
			if ((currentPlayerPosition['x'] >= (platform.x + platform.width)) and 
				((platform.y - player.height) < currentPlayerPosition['y'] < (platform.y + platform.height))):
				
				playerPosition['x'] = (platform.x + platform.width)

			#Checking if player contacted bottom side
			if (((platform.x - player.width) < currentPlayerPosition['x'] < (platform.x + platform.width)) and
				(currentPlayerPosition['y'] >= (platform.y + platform.height))):

				playerPosition['y'] = (platform.y + platform.height)

				isJumping,isFalling = False, True

			#Checking if player contacted top side
			if (((platform.x - player.width) < currentPlayerPosition['x'] < (platform.x + platform.width)) and
				(currentPlayerPosition['y'] <= (platform.y - player.height))):

				playerPosition['y'] = (platform.y - player.height)

				isFalling = False

				contact = True

	if playerPosition['y'] >= (baseBoundary - player.height):
		playerPosition['y'] = (baseBoundary - player.height)

		isFalling = False
	elif not platformContact:
		isFalling = True

	platformContact = False


	#Drawing player
	player.draw(window,playerIndex,playerPosition["x"],playerPosition["y"])

	#Drawing projectiles
	for Projectile in projectiles:
			if (Projectile.x < screenWidth) and (Projectile.x > 0):
				Projectile.x += Projectile.velocity * Projectile.direction
				Projectile.draw(window)
			else:
				projectiles.pop(projectiles.index(Projectile))
	
	#Updating display
	pygame.display.update()

pygame.QUIT