class Config:
	def __init__(self):
		#Screen
		self.screenWidth = 600
		self.screenHeight = 800
		self.frameRate = 60

		#Background
		self.bgColor = (0, 0, 20)
		self.starDensity = 400 #pixels per star (a star spawns for every x px)
		self.starDiameterRange = [1, 3] #diameter range of stars, in px [low, high]
		self.starColorRange = [100, 255] #chooses 3 of the same number for each rgb value, provides grey color

		#Player
		self.playerShipPath = "./textures/playerShip.png"
		self.playerShipSize = (75, 75) #720, 714

		self.playerShipForwardSpeed = 5 #px/frame
		self.playerShipForwardAcceleration = 5 #seconds / playerShipStrafeSpeed (px/frame)

		self.playerShipStrafeSpeed = 4 #px/frame
		self.playerShipStrafeAcceleration = 0.25 #seconds / playerShipStrafeSpeed (px/frame)
		
		self.playerFireCooldown = 0.2 #in seconds

		self.playerLives = 4

		#Enemies
		self.enemyShipPath = "./textures/enemyShip.png"
		self.enemyShipSize = (60, 60) #1200, 1200

		self.enemyShipStrafeSpeed = 2 #px/frame
		self.enemyDropSpeed = 3 #px/frame

		self.enemyFleetDrop = 1 #in enemy ship size

		#Projectiles
		self.projectileColor = (180, 0, 0)

		self.projectileWidth = 3
		self.projectileHeight = 15

		self.projectileSpeed = 8 #px/frame


		#Correct px/frame values to reflect new frame rate
		correction = 60/self.frameRate

		self.playerShipForwardSpeed *= correction
		self.playerShipStrafeSpeed *= correction
		self.enemyShipStrafeSpeed *= correction
		self.enemyDropSpeed *= correction
		self.projectileSpeed *= correction