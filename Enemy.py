import pygame, math

class Enemy(pygame.sprite.Sprite):

	def __init__(self, spaceGame):
		super().__init__()

		self.screen = spaceGame.screen
		self.config = spaceGame.config
		self.spaceGame = spaceGame

		self.image = pygame.image.load(self.config.enemyShipPath)
		self.image = pygame.transform.scale(self.image, self.config.enemyShipSize)

		self.rect = self.image.get_rect()

		self.direction = 1 #1 right, -1 left

		self.x = float(self.rect.x)
		self.targetY = self.rect.y
	
	def checkEdges(self):
		"""Returns True if this enemy is off the screen"""
		if self.rect.right >= self.config.screenWidth or self.rect.left <= 0:
			return True
	
	def update(self):
		self.x += self.config.enemyShipStrafeSpeed * self.direction * math.pow(1.1, self.spaceGame.stats.level)
		self.rect.x = int(self.x)

		if self.rect.y > self.targetY:
			self.rect.y -= self.config.enemyDropSpeed
			if self.rect.y < self.targetY:
				self.rect.y = self.targetY
		elif self.rect.y < self.targetY:
			self.rect.y += self.config.enemyDropSpeed
			if self.rect.y > self.targetY:
				self.rect.y = self.targetY