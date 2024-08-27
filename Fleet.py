import pygame
from Enemy import Enemy

class Fleet(pygame.sprite.Sprite):

	def __init__(self, spaceGame, fleetType = "rows"):
		super().__init__()
		self.spaceGame = spaceGame
		self.config = spaceGame.config
		self.fleetType = fleetType

		self.ships = pygame.sprite.Group()

		self._createShips()
	
	def _createShips(self):
		if self.fleetType == "rows":
			currentY = self.config.enemyShipSize[1] * 3/2
			for i in range(2):
				currentX = self.config.enemyShipSize[0] * 3/2 + i * self.config.enemyShipSize[0]/2
				currentY = (i + 1) * self.config.enemyShipSize[1]
				for j in range(8 - i):
					enemy = Enemy(self.spaceGame)
					enemy.x = currentX
					enemy.rect.y = currentY
					enemy.targetY = currentY
					self.ships.add(enemy)
					currentX += self.config.enemyShipSize[1]
		else:
			print("No fleet type: " + self.fleetType)

	def changeDirection(self):
		for ship in self.ships.sprites():
			ship.targetY += self.config.enemyFleetDrop * self.config.enemyShipSize[1]
			ship.direction *= -1

	def checkEdges(self):
		for ship in self.ships.sprites():
			if ship.checkEdges():
				self.changeDirection()
				break

	def update(self):
		for ship in self.ships:
			ship.update()

	def draw(self):
		self.ships.draw(self.spaceGame.screen)