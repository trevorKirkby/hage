import pygame
pygame.init()

class animation():
	def __init__(self,imageDictionary):
		self.currentImage = None
		# current image is dictionary access actually (stationary image), just forgot how to use dictionaries though
		self.count = 0
		self.action = "stationary"
	def update(self,imageDictionary,action):
		
