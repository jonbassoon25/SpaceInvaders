import pygame.font

class Scoreboard:

	def __init__(self, spaceGame, textSize = 28, textColor = (255, 255, 255)):
		self.spaceGame = spaceGame
		self.screen = spaceGame.screen

		self.textSize = textSize

		self.textColor = textColor

		self.font = pygame.font.SysFont(None, textSize)

		self.update()

	def update(self):
		screenRect = self.screen.get_rect()

		self.scoreImg = self.font.render(str(self.spaceGame.stats.score), True, self.textColor)
		self.rect = self.scoreImg.get_rect()
		self.rect.right = screenRect.right - 20
		self.rect.top = 20

		if self.spaceGame.username == "":
			return
		
		self.highScoreImg = self.font.render("Highscore: " + str(self.spaceGame.leaderboardData[self.spaceGame.username]), True, self.textColor)
		self.highScoreRect = self.highScoreImg.get_rect()
		self.highScoreRect.right = screenRect.right - 20
		self.highScoreRect.top = self.rect.bottom + 5

	def draw(self):
		self.screen.blit(self.scoreImg, self.rect)
		if not self.spaceGame.username == "":
			self.screen.blit(self.highScoreImg, self.highScoreRect)