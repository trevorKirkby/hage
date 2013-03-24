import pygame, time
pygame.init()
thingDir = None

def setMode(text):
	if text == "w":
		screen = pygame.display.set_mode((0,0))
		return screen
	elif text == "f":
		screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		return screen

def draw(screen):
	surface = pygame.Surface((0,0))
	surface.fill((0,65,0))
	surface.getrect
	Surface.blit(surface, screen)
	pygame.display.update()
	thingDirList = arrowInput()
	count = 0
	for boolean in thingDirList:
		if boolean == True:
			if count == 0:
				thingDir == "right"
			if count == 1:
				thingDir == "left"
			if count == 2:
				thingDir == "down"
			if count == 3:
				thingDir == "up"
		count = count + 1
	print thingDir
	return surface

def arrowInput():
	thingRight = False
	thingLeft = False
	thingDown = False
	thingUp = False
	for item in pygame.event.get():
		if item.type == pygame.KEYDOWN and item.key == 275:
			thingRight = True
		if item.type == pygame.KEYUP and item.key == 275:
			thingRight = False
		if item.type == pygame.KEYDOWN and item.key == 273:
			thingUp = True
		if item.type == pygame.KEYUP and item.key == 273:
			thingUp = False
		if item.type == pygame.KEYDOWN and item.key == 274:
			thingDown = True
		if item.type == pygame.KEYUP and item.key == 274:
			thingDown = False
		if item.type == pygame.KEYDOWN and item.key == 276:
			thingLeft = True
		if item.type == pygame.KEYUP and item.key == 276: 
			thingLeft = False
		if item.type == pygame.KEYDOWN and item.key == 113:
			raise SystemExit
		return [thingRight,thingLeft,thingDown,thingUp]

screen = setMode(raw_input("start in full screen or window? (f/w): "))
try:
	surface = draw(screen)
except:
	try:
		screen = setMode(raw_input("please enter f for full screen or w for window: "))
		surface = draw(screen)
	except:
		print "fine then! program shutting down..."
		raise SystemExit
