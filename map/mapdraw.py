import pygame, time
pygame.init()

def setMode(text):
	if text == "w":
		screen = pygame.display.set_mode((0,0))
		return screen
	elif text == "f":
		screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		return screen

screen = setMode(raw_input("start in full screen or window? (f/w): "))
try:
	surface = pygame.Surface((0,0))
	surface.fill((0,65,0))
	#screen.fill(surface)
	pygame.display.update()
	time.sleep(10)
except:
	try:
		screen = setMode(raw_input("please enter f for full screen or w for window: "))
		surface = pygame.Surface((0,0))
		surface.fill((0,65,0))
		#screen.fill(surface)
		pygame.display.update()
		time.sleep(10)
	except:
		print "fine then! program shutting down..."
		raise SystemExit
