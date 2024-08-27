class GameStatistics:
    def __init__(self, spaceGame):
        self.config = spaceGame.config

        self.shipsLeft = self.config.playerLives - 1

        self.level = 1

        self.score = 0