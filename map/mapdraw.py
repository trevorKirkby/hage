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

class Surface(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.surface = None
	def draw(self,screen):
		self.surface = pygame.Surface((0,0))
		self.surface.fill((0,65,0))
		self.rect = self.surface.get_rect()
		self.rect.topleft = (0,0)
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
screen.blit(blegh,(0,0))
pygame.display.update()
#try:
#blegh = Surface()
#drawable.add(blegh)
while True:
	#screen = blegh.draw(screen)
	#spygame.display.update(drawable.draw(screen))
	arrows = arrowInput()
	time.sleep(.05)
#except:
#	try:
#		screen = setMode(raw_input("please enter f for full screen or w for window: "))
#		surface = draw(screen)
#	except:
#		print "fine then! program shutting down..."
#		raise SystemExit
