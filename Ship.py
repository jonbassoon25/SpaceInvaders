import pygame

from Projectile import Projectile

class Ship:
	def __init__(self, spaceGame):
		self.spaceGame = spaceGame
		self.screen = spaceGame.screen
		self.config = spaceGame.config
		self.screenRect = spaceGame.screen.get_rect()
		
		self.image = pygame.image.load(self.config.playerShipPath)
		self.image = pygame.transform.scale(self.image, self.config.playerShipSize) #50, 49.514 - 720, 713

		self.rect = self.image.get_rect()
		self.rect.midbottom = self.screenRect.midbottom
		self.rect.y -= 10 #displace from bottom of screen

		self.x = float(self.rect.x)

		self.fireCooldown = self.config.playerFireCooldown * self.config.frameRate
		self.currentFireCooldown = 0

		self.movingLeft = False
		self.movingRight = False
		self.firing = False

		self.maxForwardSpeed = self.config.playerShipForwardSpeed
		self.maxStrafeSpeed = self.config.playerShipStrafeSpeed
		self.forwardSpeed = 0
		self.strafeSpeed = 0

		self.strafeAcceleration = self.maxStrafeSpeed/self.config.playerShipStrafeAcceleration/self.config.frameRate #px/frame^2
		self.forwardAcceleration = self.maxForwardSpeed/self.config.playerShipForwardAcceleration/self.config.frameRate #px/frame^2



		self.projectiles = pygame.sprite.Group()

	def fire(self):
		newProjectile = Projectile(self.spaceGame)
		self.projectiles.add(newProjectile)
	
	def blitme(self):
		self.screen.blit(self.image, self.rect)
	
	def updateProjectiles(self):
		for projectile in self.projectiles.copy():
			projectile.update()
			if projectile.rect.bottom <= 0:
				self.projectiles.remove(projectile)

	def update(self):
		#Strafe movement
		if self.movingRight and self.strafeSpeed < self.maxStrafeSpeed:
			self.strafeSpeed += self.strafeAcceleration
		if self.movingLeft and self.strafeSpeed > -self.maxStrafeSpeed:
			self.strafeSpeed -= self.strafeAcceleration

		#direction change checks
		if self.movingLeft and self.strafeSpeed > 0:
			self.strafeSpeed -= self.config.playerShipStrafeAcceleration
		elif self.movingRight and self.strafeSpeed < 0:
			self.strafeSpeed += self.config.playerShipStrafeAcceleration
		elif not (self.movingRight or self.movingLeft):
			self.strafeSpeed = 0

		#stop ship from strafing faster than max strafe speed
		if abs(self.strafeSpeed) > self.maxStrafeSpeed:
			self.strafeSpeed = self.maxStrafeSpeed * (self.strafeSpeed/abs(self.strafeSpeed))
		
		#keep ship inside screen bounds
		if not ((self.movingLeft and self.rect.left <= 0) or (self.movingRight and self.rect.right >= self.config.screenWidth)):
			self.x += self.strafeSpeed
			
		self.rect.x = int(self.x)


		#Forward movement
		if self.forwardSpeed < self.maxForwardSpeed:
			self.forwardSpeed += self.forwardAcceleration
		elif self.forwardSpeed > self.maxForwardSpeed:
			self.forwardSpeed = self.maxForwardSpeed
		
		#Fire Checks
		if self.firing and self.currentFireCooldown <= 0:
			self.fire()
			self.currentFireCooldown = self.fireCooldown
		elif self.currentFireCooldown > 0:
			self.currentFireCooldown -= 1
		elif self.currentFireCooldown < 0:
			self.currentFireCooldown = 0