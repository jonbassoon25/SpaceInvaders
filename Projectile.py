import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, spaceGame):
        super().__init__()
        
        self.screen = spaceGame.screen
        self.config = spaceGame.config

        self.color = self.config.projectileColor
        self.rect = pygame.Rect(0, 0, self.config.projectileWidth, self.config.projectileHeight)
        self.rect.midtop = spaceGame.ship.rect.midtop

        self.y = float(self.rect.y)

        

    def update(self):
        self.y -= self.config.projectileSpeed

        self.rect.y = int(self.y)
    
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)