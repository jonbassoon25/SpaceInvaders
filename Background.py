import pygame

from Star import Star

class Background:

	def __init__(self, spaceGame):
		self.spaceGame = spaceGame
		self.screen = spaceGame.screen
		self.config = spaceGame.config

		self.color = self.config.bgColor
		self.totalStars = int((self.config.screenWidth * self.config.screenHeight) / self.config.starDensity)

		self.stars = pygame.sprite.Group()
		self._populateBackground()
	
	def _populateBackground(self):
		for i in range(self.totalStars):
			newStar = Star(self.spaceGame, True)
			self.stars.add(newStar)
	
	def _spawnNewStars(self):
		for i in range(self.totalStars - len(self.stars)):
			newStar = Star(self.spaceGame)
			self.stars.add(newStar)

	def update(self):
		for star in self.stars.copy():
			star.update()
			if star.y - star.diameter/2 >= self.config.screenHeight:
				self.stars.remove(star)
		
		self._spawnNewStars()

	def draw(self):
		self.screen.fill(self.color)
		for star in self.stars:
			star.blitme()