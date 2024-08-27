import pygame

class LoginBox:
    def __init__(self, spaceGame):
        self.screen = spaceGame.screen
        self.color = (150, 150, 150)
        self.borderColor = (255, 255, 0)
        self.borderWidth = 5
        self.text = ""
        self.rect = pygame.Rect(0, 0, 400, 50)
        self.borderRect = pygame.Rect(0, 0, 400 + self.borderWidth * 2, 50 + self.borderWidth * 2)
        self.rect.center = self.screen.get_rect().center
        self.rect.y -= 50
        self.borderRect.center = self.rect.center
        self.textLimit = 16

        self.font = pygame.font.SysFont("monospace", 24)

        self._update()
    
    def addLetter(self, letter):
        if len(self.text) >= 16:
            return
        self.text += letter
        self._update()

    def removeLetter(self):
        self.text = self.text[0:-1]
        self._update()
        

    def _update(self):
        self.msgImg = self.font.render(self.text, True, (0, 0, 0))
        self.msgRect = self.msgImg.get_rect()
        self.msgRect.midleft = self.rect.midleft
        self.msgRect.left += 5
    
    def draw(self):
        self.screen.fill(self.borderColor, self.borderRect)
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.msgImg, self.msgRect)