import pygame, random

class Star(pygame.sprite.Sprite):

	def __init__(self, spaceGame, randomY = False):
		super().__init__()
		self.spaceGame = spaceGame
		self.screen = spaceGame.screen
		self.config = spaceGame.config

		colNum = random.randint(self.config.starColorRange[0], self.config.starColorRange[1])
		self.color = (colNum, colNum, colNum)

		self.x = random.randint(0, self.config.screenWidth - 1)
		if randomY:
			self.y = random.randint(0, self.config.screenHeight - 1)
		else:
			self.y = random.randint(int(-self.spaceGame.ship.forwardSpeed), 0) #random to avoid rows of stars at high forward speeds

		self.diameter = random.randint(self.config.starDiameterRange[0], self.config.starDiameterRange[1])

	def update(self):
		self.y += self.spaceGame.ship.forwardSpeed
		
	def blitme(self):
		pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.diameter/2)