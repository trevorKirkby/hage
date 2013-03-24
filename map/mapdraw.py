import pygame, time
pygame.init()
thingDir = None
drawable = pygame.sprite.RenderUpdates()

def setMode(text):
	if text == "w":
		screen = pygame.display.set_mode((0,0))
		return screen
	elif text == "f":
		screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		return screen

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
		return (thingRight,thingLeft,thingDown,thingUp)

screen = setMode(raw_input("start in full screen or window? (f/w): "))
blegh = pygame.Surface(screen.get_size())
blegh.fill((0,100,0))
pygame.draw.polygon(blegh,(100,0,100),[(100,100),(400,400),(100,400)], 0)
screen.blit(blegh,(0,0))
pygame.display.update()
while True:
	arrows = arrowInput()
	time.sleep(.05)
