#!/usr/bin/env python

import pygame, unitImage
pygame.init()

collisionObjects = pygame.sprite.RenderUpdates()

class Unit(pygame.sprite.Sprite):
	def __init__(self,pos,CanBuildBool,CanMineBool,RangedWeaponBool,PersonalityBool,LearnBool,Ravenbool,AttackRadius,Attack,Health,Speed,Stamina,getStuck,UnitBonuses,ResearchList,imageLibrary,WaterBool,name,elevation):
		pygame.sprite.Sprite.__init__(self)
		#all images required are as follows: imageStationaryList, imageSideMoveList, imageUpMoveList, imageDownMoveList, imageSideAttackList, imageUpAttackList, imageDownAttackList, imageMiningPitList, imageMiningCaveList, imageMiningQuarryList, imageChoppingList, imageSawingList, imageHuntingList, imageGatheringList, imageFishingList, imageWellList, imageJugList, imageFarmingList, imageCarryingList, buildingStageOneList, buildingStageTwoList, buildingStageThreeList, and imageDead. These are categorized into mining, combat,movement, and building lists. Move is imagesList[0],stationary MovementLists[0], animationStart is StationaryList[0](goes 0-3 for stationary animations)
		self.reinit(pos,CanBuildBool,CanMineBool,RangedWeaponBool,PersonalityBool,LearnBool,Ravenbool,AttackRadius,Attack,Health,Speed,Stamina,getStuck,UnitBonuses,ResearchList,imageLibrary,WaterBool,name,elevation)
	def reinit(self,pos,CanBuildBool,CanMineBool,RangedWeaponBool,PersonalityBool,LearnBool,Ravenbool,AttackRadius,Attack,Health,Speed,Stamina,getStuck,UnitBonuses,ResearchList,imageLibrary,WaterBool,name,elevation):
		self.count = 0
		self.image = unitImage.load("stationary",self.count)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.builder = CanBuildBool
		self.buildings = None
		self.currentElevation = elevation
		if self.builder == True:
			self.buildings = ["town center","mining camp 1","lumber stockpile","hunting post","fishing dock","stockpile","grainary","water store","home","watchpost"]
			#all of these can store amounts of resource. TC can hold some of each, mining camp can hold ore and salt, lumber stockpile can hold wood, mill can hold some grains, hunting post can hold some meat, fishing dock can hold some meat and build small fishing ships and transport barges, markets establish currency, stockpile holds mineralsand wood, grainery holds meats and grains, well holds water. All types of holding will slowly diminish despite you not using it(but the process can be slowed and does not happen to stone or salt, and happens quickly to meat), and will be either destroyrd or stolen when a stockpile is taken over. While it is stored, you will have immediate acess to it. Later can mine sea salt, develop non barter currency, and build traveler lodges and outposts, as well as cave mines and slab mines.
		self.miner = CanMineBool
		if self.miner == True:
			self.canMine = ["small stone mine","small salt mine","small forest tree","deer corpse","boar corpse","sheep corpse","turkey corpse","small fish","berries","roots","bird corpse","rabbit corpse","cow corpse","water spring","fresh river"]
			self.carrying = None
		self.archer = RangedWeaponBool
		if PersonalityBool == True:
			self.independance = random.choice(range(20))
			#independance and loyalty affect who follows orders, independance affects leadership as well
			self.loyalty = random.choice(range(20))
			self.navigation = random.choice(range(10))
			self.AI = random.choice(range(7))
			if self.archer == True:
				self.accuracy = random.choice(range(6))
			else:
				self.accuracy = None
			self.temper = random.choice(range(20))
			self.courage = random.choice(range(20))
			self.health = random.choice(range(20)) + Health
			self.attack = random.choice(range(8)) + Attack
			self.speed = random.choice(range(2)) + Speed
			self.stamina = random.choice(range(25)) + Stamina
		else:
			self.independance = 4
			self.loyalty = 9
			self.navigation = 2
			self.AI = random.choice(range(3))
			if self.archer == True:
				self.accuracy = 2
			else:
				self.accuracy = None
			self.temper = 9
			self.courage = 8
			self.health = Health
			self.attack = Attack
			self.speed = Speed
			self.stamina = Stamina
			self.fullhealth = self.health
			self.fullstamina = self.stamina
			
		self.learn = None
		self.exp = None
		if LearnBool == True:
			self.learn = True
			self.exp = 0
		else:
			self.learn = False
		self.report = RavenBool
		self.attackradius = AttackRadius
		self.wheels = getStuck
			if self.wheels == True:
				self.stuck == False
		if UnitBonuses[0] == True:
			self.unitBonus = UnitBonuses
		else:
			pass
		self.ship = waterBool

	def move(self,dx,dy,elevation,weather,footing,temperature):
		#footing refers to the difference between thorny undergrowth and paved road
		screen.fill((150,150,200),self.rect)
		collisions = pygame.sprite.spritecollide(self, everything, False)
		for other in collisions:
			if other != self:
				(awayDx,awayDy) = self.moveRelative(other,-1)
				dx = dx + 4*(awayDx)
				dy = dy + 4*(awayDy)
		if elevation > self.currentElevation:
			dx = dx - (elevation - self.currentElevation)
			dy = dy - (elevation - self.currentElevation)
		if elevation < self.currentElevation:
			dx = dx + ((self.currentElevation - elevation)-1)
			dy = dy + ((self.currentElevation - elevation)-1)
		self.currentElevation = elevation
		if weather == "rainy":
			if self.wheels == True:
				if random.choice(range(1000)) == 1:
					footing = footing + 50
					self.stuck == True
		if weather == "stormy":
			#weather can be rainy, stormy, snowing, ocean storm,blizzard, sunny, cloudy, hail, foggy, and hurricane.
			footing = footing + 3
			self.stamina = self.stamina - 1
		if weather == "blizzard":
			footing = footing + 7
			self.stamina = self.stamina - 7
		if weather == "ocean storm":
			footing = footing + 7
			self.stamina = self.stamina - 2
		if weather == "snowing":
			footing = footing + 3
			self.stamina = self.stamina - 1
		if weather == "hail":
			footing = footing + 3
			self.stamina = self.stamina - 1
			self.health = self.health - float(0.02)
			# both speed and stamina are pretty big numbers that only are tangibly seen as a few classifying words. Health is also seen as classyifying words(and yes your people can fake more or less severe injuries) and is a smaller number better inclined towards simple subtractions than complicated and numerous detractions from dx and dy
		if weather == "hurricane":
			footing = footing + 8
			self.stamina = self.stamina - 5
		if self.stamina/self.fullstamina < float(0.6):
			dx = dx - 1
			dy = dy - 1
			if self.stamina/self.fullstamina < float(0.4):
				dx = dx - 1
				dy = dy - 1
				if self.stamina/self.fullstamina < float(0.2):
					dx = dx - 1
					dy = dy - 1
		if self.stamina < 0:
			#self.remove(everything) basically kill unit
			pass
		if footing > 0:
			#0 means 0 resistance of path
			dx = dx - int(footing/self.navigation)
			dy = dy - int(footing/self.navigation)
			self.stamina = self.stamina - float(0.25)
		self.stamina = self.stamina - float(0.5)
		self.rect.move_ip(dx,dy)
"""
	def LOS(self,coordinates,elevation,weather,time):
		if self.ravenOwner == True:
			pygame.display.update(self.losRect)
		self.vulnerable = pygame.rect.inflate(self.rect,250,250)
		self.vulnerable.move_ip(coordinates)
		#notes: any unit los(which increases with elevation and light, and decreases with fog and dark) starts out uniform. Only raven owners report their los to you, so everything else is shrouded in fog of war. And ravens are quite expensive, require some basic research, and aren't 100 percent loyal. So be careful. To make up for lack of ravens, rumors often print through f4om the sidelines. Most of it is useless, motivating you to ignore it, but heeding it always tells you useful stuff sometimes. You will always hear about large enemy forces, however, if you have spies, which make the flow of rumor information much more useful, and will inform you on your map of big events. Also emphasizing strategy, time has a habit of slowing down whenever something important is going on, allowing orders to be relayed faster. However this time slow can sometimes just be random, so if your not aware of what is happening, you may not be about to be attacked. Because if you spend some resources on research and bribes, and kill a few spy units(who can't own ravens), you can mount a stealth attack, especially if you do it soon after raising your army, or by raising the army gradually, and marching with no forewarnment. Similarly, assassin units can sneak in if the gaurds aren't smart and the assassins are, so it's a good idea to always gaurd your leaders. However, seeing as assassination can be a suicide task, suitable stealth military units are very costly and require a lot of loyalty to accept dangerous work. All units are like that. They need to be brave, loyal, and less independant to accept such tasks, but independance is a must for such tasks.
	def moveRelative(self,other):
		dx = other.rect.x - self.rect.x
		dy = other.rect.y - self.rect.y
		if abs(dx) > abs(dy):
			# other is farther away in x than in y
			if dx > 0:
				return (+self.speed,0)
			else:
				return (-self.speed,0)
		else:
			if dy > 0:
				return (0,+self.speed)
			else:
				return (0,-self.speed)
	def movePerpendicular(self,other,speed):
		dx = other.rect.x - self.rect.x
		dy = other.rect.y - self.rect.y
		if abs(dx) > abs(dy):
			# this is to dodge a projectile
			if dy > 0:
				if dx > 0:
					return (+speed/2,+speed)
				else:
					return (-speed/2,+speed)
			else:
				if dx > 0:
					return (+speed/2,-speed)
				else:
					return (-speed/2,-speed)
		else:
			if dx > 0:
				if dy > 0:
					return (+speed,+speed/2)
				else:
					return (+speed,-speed/2)
			else:
				if dy > 0:
					return (-speed,+speed/2)
				else:
					return (-speed,-speed/2)
	def rangeTo(self,other):
		dx = other.rect.x - self.rect.x
		dy = other.rect.y - self.rect.y
		return math.sqrt(dx*dx + dy*dy)
"""
