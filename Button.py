import pygame.font

class Button:
	def __init__(self, screen, message, x, y, width, height, textSize = 48, bgColor = (144, 0, 0), textColor = (255, 255, 255)):
		self.screen = screen
		self.screenRect = self.screen.get_rect()

		self.rect = pygame.Rect(x - width/2, y - height/2, width, height)

		self.bgColor = bgColor
		self.textColor = textColor

		self.font = pygame.font.SysFont(None, textSize)

		self._prepMessage(message)

	def _prepMessage(self, message):
		self.msgImg = self.font.render(message, True, self.textColor, self.bgColor)
		self.msgImgRect = self.msgImg.get_rect()
		self.msgImgRect.center = self.rect.center

	def draw(self):
		self.screen.fill(self.bgColor, self.rect)
		self.screen.blit(self.msgImg, self.msgImgRect)
		

