#imports
import pygame, sys

from Util import *

from Config import Config
from Background import Background
from Ship import Ship
from Enemy import Enemy
from GameStatistics import GameStatistics
from Button import Button
from Fleet import Fleet
from Scoreboard import Scoreboard
from Leaderboard import Leaderboard
from LoginBox import LoginBox

class SpaceInvaders:
	"""Primary game management class"""

	#class constructor
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Space Inavders")

		self.clock = pygame.time.Clock()
		self.config = Config()
		self.screen = pygame.display.set_mode(
						(self.config.screenWidth, self.config.screenHeight), 
						flags = pygame.SCALED, 
						vsync = 1
					)

		self.startButton = Button(
			self.screen, 
			"Play", 
			self.config.screenWidth/2, 
			self.config.screenHeight/2 - 75, 
			300, 
			100
		)
		
		self.leaderboardButton = Button(
			self.screen,
			"Leaderboard",
			self.config.screenWidth/2,
			self.config.screenHeight/2 + 75,
			300,
			100
		)

		self.leaderboardBackButton = Button(
			self.screen,
			"Back",
			75,
			50,
			100,
			50
		)

		self.loginButton = Button(
			self.screen,
			"Submit",
			self.config.screenWidth * 0.7,
			self.config.screenHeight * 0.6,
			200,
			75
		)

		self.skipButton = Button(
			self.screen,
			"Skip",
			self.config.screenWidth * 0.3,
			self.config.screenHeight * 0.6,
			200,
			75
		)

		self.background = None
		self.ship = None
		self.stats = None
		self.fleets = None
		self.scoreboard = None

		self.loginBox = LoginBox(self)
		self.username = ""

		self.leaderboardData = {}
		with open("leaderboard.txt") as leaderboardFile:
			leaderboard = leaderboardFile.readlines()
			for thing in leaderboard:
				thing = thing.strip().split(" ")
				self.leaderboardData[thing[0]] = int(thing[1])
			
			self.leaderboardData = sortDict(self.leaderboardData)
		
		self.leaderboard = Leaderboard(self)

		self.state = "menu"

	def _checkKeyDown(self, event):
		if event.type == pygame.KEYDOWN:
			if self.state == "login":
				if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
					self.loginBox.removeLetter()
					return
				
				try:
					letter = chr(int(str(event.key)))
				except:
					print("Code " + str(event.key) + " not recognized")
					return
				if len(letter) == 1:
					self.loginBox.addLetter(chr(int(str(event.key))))
				return
			
			if self.state == "game":
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					self.ship.movingRight = True
				elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
					self.ship.movingLeft = True
				elif event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
					self.ship.firing = True
				elif event.key == pygame.K_ESCAPE:
					sys.exit()
	
	def _checkKeyUp(self, event):
		if self.state == "game":
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					self.ship.movingRight = False
				elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
					self.ship.movingLeft = False
				elif event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
					self.ship.firing = False

	def _checkMouseDown(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			mousePos = pygame.mouse.get_pos()
			if self.state == "menu":
				if self.startButton.rect.collidepoint(mousePos):
					if self.username == "":
						self.loginBox = LoginBox(self)
						self.state = "login"
					else:
						self.state = "game"
						self._reset()
					return
				if self.leaderboardButton.rect.collidepoint(mousePos):
					self.leaderboardData = sortDict(self.leaderboardData)
					self.leaderboard.update(self.leaderboardData)
					self.state = "leaderboard"
					return
			elif self.state == "leaderboard":
				if self.leaderboardBackButton.rect.collidepoint(mousePos):
					self.state = "menu"
					return
			elif self.state == "login":
				if self.loginButton.rect.collidepoint(mousePos) and not len(self.loginBox.text) == 0:
					self.username = self.loginBox.text
					if list(self.leaderboardData.keys()).count(self.username) == 0:
						self.leaderboardData[self.username] = 0
					self.state = "game"
					self._reset()
				if self.skipButton.rect.collidepoint(mousePos):
					self.state = "game"
					self._reset()
				return
			elif self.state == "game":
				self.ship.firing = True
	
	def _checkMouseUp(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			if self.state == "game":
				self.ship.firing = False

	def _checkEvents(self):
		for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					sys.exit()
				self._checkKeyDown(event)
				self._checkKeyUp(event)
				self._checkMouseDown(event)
				self._checkMouseUp(event)
	
	def _spawnFleet(self, fleetType = "rows"):
		self.fleets.add(Fleet(self, fleetType))
	
	def _advanceWave(self):
		self.fleets.empty()
		self.ship.projectiles.empty()
		self.stats.level += 1
		self._spawnFleet()

	def _playerHit(self):
		self.stats.shipsLeft -= 1
		if self.stats.shipsLeft < 0:
			self._lose()
	
	def _lose(self):
		if not self.username == "":
			self._saveLeaderboard()
		self.state = "menu"
	
	def _reset(self):
		self.background = Background(self)
		self.ship = Ship(self)
		self.stats = GameStatistics(self)
		self.scoreboard = Scoreboard(self)
		self.fleets = pygame.sprite.Group()

		self._spawnFleet()

	def _saveLeaderboard(self):
		leaderboardText = ""
		for key in self.leaderboardData.keys():
			leaderboardText += key + " " + str(self.leaderboardData[key]) + "\n"
		leaderboardText = leaderboardText.rstrip()
		with open("leaderboard.txt", "w") as LeaderboardFile:
			LeaderboardFile.write(leaderboardText)


	def _updateFleets(self):
		broken = False
		for fleet in self.fleets:
			fleet.checkEdges()
			fleet.update()

			for ship in fleet.ships:
				if ship.rect.bottom >= self.config.screenHeight:
					self._playerHit()
					self._advanceWave()
					broken = True
					break

			if broken:
				break
	
	def _drawFleets(self):
		for fleet in self.fleets:
			fleet.draw()
				
	def _updateProjectiles(self):
		self.ship.updateProjectiles()

	def _drawProjectiles(self):
		for projectile in self.ship.projectiles:
			projectile.draw()
	
	def _drawLives(self):
		for i in range(self.stats.shipsLeft):
			screenRect = self.screen.get_rect()
			shipImg = self.ship.image
			shipImg = pygame.transform.scale(shipImg, (40, 40))
			self.screen.blit(shipImg, pygame.Rect(screenRect.left + 20 + (i * 50), 20, 40, 40))
	
	def _update(self):
		self.background.update()
		self.ship.update()

		self._updateProjectiles()
		self._updateFleets()
		for fleet in self.fleets.copy():
			shipCount = len(fleet.ships)
			pygame.sprite.groupcollide(self.ship.projectiles, fleet.ships, True, True)
			newShipCount = len(fleet.ships)
			if (shipCount != newShipCount):
				self.stats.score += 100 * (shipCount - newShipCount)
				if not self.username == "" and self.leaderboardData[self.username] < self.stats.score:
					self.leaderboardData[self.username] = self.stats.score
				self.scoreboard.update()

			if not fleet.ships:
				self.fleets.remove(fleet)
				break

			if pygame.sprite.spritecollideany(self.ship, fleet.ships):
				self._advanceWave()
				self._playerHit()

		if not self.fleets:
			self._advanceWave()
		
	def _draw(self):
		self.background.draw()

		self._drawProjectiles()
		
		self._drawFleets()

		self._drawLives()
		self.scoreboard.draw()

		self.ship.blitme()

	def runGame(self):
		while True:
			#event loop
			self._checkEvents()
			if self.state == "menu":
				self.screen.fill(self.config.bgColor)
				self.startButton.draw()
				self.leaderboardButton.draw()
			elif self.state == "leaderboard":
				self.screen.fill(self.config.bgColor)
				self.leaderboard.draw()
				self.leaderboardBackButton.draw()
			elif self.state == "game":
				#update objects
				self._update()

				#draw objects
				self._draw()
			elif self.state == "login":
				self.screen.fill(self.config.bgColor)
				self.loginBox.draw()
				self.loginButton.draw()
				self.skipButton.draw()
				

			#advance frame
			pygame.display.flip()
			self.clock.tick(self.config.frameRate)
            
            
if __name__ == '__main__':
	space = SpaceInvaders()
	space.runGame()
	
quit()