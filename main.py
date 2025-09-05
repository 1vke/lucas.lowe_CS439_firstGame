import enum, simpleGE.simpleGE as simpleGE

class GameState(enum.Enum):
    START = 0
    PLAYING = 1

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__((1024, 768))

        self.__gamestate = -1
        self.sprites = []

        self.gamestate = GameState.START

    @property
    def gamestate(self):
        return self.__gamestate
    
    @gamestate.setter
    def gamestate(self, newGamestate):
        if (newGamestate in GameState and newGamestate != self.__gamestate):
            self.__gamestate = newGamestate
            self.handleGamestateChange(newGamestate)

    def handleGamestateChange(self, newGamestate):
        match newGamestate:
            case GameState.START:
                print("start game state")
            case GameState.PLAYING:
                print("playing game state")

if __name__ == "__main__":
    game = Game()
    game.start()
