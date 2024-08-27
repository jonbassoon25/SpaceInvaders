import pygame

class Leaderboard:
	def __init__(self, spaceGame, textSize = 24, textColor = (255, 255, 255)):
		self.spaceGame = spaceGame
		self.config = spaceGame.config
		self.screen = spaceGame.screen
		self.leaderboardData = self.spaceGame.leaderboardData

		self.screen = spaceGame.screen

		self.textSize = textSize

		self.textColor = textColor

		self.rect = pygame.Rect(0, 0, self.config.screenWidth / 1.25, self.config.screenHeight / 1.5)
		self.rect.center = self.screen.get_rect().center

		self.font = pygame.font.SysFont("monospace", textSize)

		self.update()
	
	def update(self, newData = {}):
		if not len(newData.keys()) == 0:
			self.leaderboardData = newData
		#set leaderboard data
		self.leaderboardTextImages = []
		i = 0
		for key in self.leaderboardData.keys():
			if i > 10:
				break
			self.leaderboardTextImages.append(
				self.font.render(
						key + 
						" " * max(16 - len(key), 0) +
						" " * 12 + 
						str(self.leaderboardData[key]), 
					True, 
					self.textColor
				)
			)
			i += 1

	def draw(self):
		if len(self.leaderboardTextImages) == 0:
			return
		
		for i in range(len(self.leaderboardTextImages)):
			imgRect = self.leaderboardTextImages[i].get_rect()
			drawRect = pygame.Rect(
				self.rect.left, 
				self.rect.top + i * imgRect.height * 1.25, 
				imgRect.width, 
				imgRect.height
			)

			self.screen.blit(self.leaderboardTextImages[i], drawRect)