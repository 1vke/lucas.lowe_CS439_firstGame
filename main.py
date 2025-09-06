import enum, pygame, random, simpleGE.simpleGE as simpleGE

SCREEN_SIZE = (1024, 768)
ROUND_TIME_SECONDS = 5
ROUND_COUNT = 5
TARGET_COUNT = 7
BASE_TARGET_SCORE = 100

class GameState(enum.Enum):
    INITIALIZING = 0
    START = 1
    PLAYING = 2
    END = 3

class GUIVisibilityMixin:
    @property
    def visible(self):
        sw, sh = SCREEN_SIZE
        x, y = self.center
        return (0 <= x <= sw) and (0 <= y <= sh)
    
    def show(self):
        if not self.visible:
            super().show()

    def hide(self):
        if self.visible:
            super().hide()

class GUIFontStyleMixin:
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font("assets/TT Octosquares Trial DemiBold.ttf", 20)
        self.clearBack = True
        self.fgColor = ((0xFF, 0xFF, 0xFF))

class TitleLabel(GUIFontStyleMixin, GUIVisibilityMixin, simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Aim Trainer"
        self.center = (512, 150)
        self.size = (700, 100)
        self.font = pygame.font.Font("assets/TT Octosquares Trial DemiBold.ttf", 80)

class StartButton(GUIFontStyleMixin, GUIVisibilityMixin, simpleGE.Button):
    def __init__(self):
        super().__init__()
        self.center = (512, 384)
        self.size = (250, 55)
        self.text = "Start Game"
        self.font = pygame.font.Font("assets/TT Octosquares Trial DemiBold.ttf", 30)

class FinalScoreLabel(GUIFontStyleMixin, GUIVisibilityMixin, simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Last Score: 0"
        self.center = (512, 235)
        self.size = (400, 50)
        self.font = pygame.font.Font(None, 40)

class ScoreLabel(GUIFontStyleMixin, GUIVisibilityMixin, simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (120, 40)

class TimerLabel(GUIFontStyleMixin, GUIVisibilityMixin, simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = f"Time: {ROUND_TIME_SECONDS:.2f}"
        self.center = (850, 40)
        self.size = (250, 30)

class RoundLabel(GUIFontStyleMixin, GUIVisibilityMixin, simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Round: 1"
        self.center = (512, 40)
        self.size = (200, 30)

class Target(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("assets/target.png")
        self.setSize(50, 50)
        self.reset()
        self.setBoundAction(self.CONTINUE)

    def reset(self):
        self.position = (-1000, -1000)

    def spawn(self):
        topPadding = 150
        sizePadding = self.rect.width

        self.position = (
            random.randint(sizePadding, self.screenWidth - sizePadding), 
            random.randint(topPadding, self.screenHeight - sizePadding)
        )

    def process(self):
        if self.clicked:
            mouse_pos = pygame.mouse.get_pos()
            distance = self.distanceTo(mouse_pos)
            
            radius = self.rect.width / 2
            
            normalized_distance = min(distance / radius, 1.0)
            
            multiplier = 1.5 - normalized_distance
            
            score_to_add = int(BASE_TARGET_SCORE * multiplier)
            
            self.scene.score += score_to_add
            self.scene.score_label.text = f"Score: {self.scene.score}"
            self.scene.hit_sound.play()
            self.reset()

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__(SCREEN_SIZE)
        self.setImage("assets/grid_bg.png")

        self.__gamestate = -1
        self.last_score = 0
        self.score = 0
        self.current_round = 0

        # Timers
        self.game_timer = simpleGE.Timer()
        self.game_timer.totalTime = ROUND_TIME_SECONDS

        # Sound
        self.hit_sound = simpleGE.Sound("assets/target_hit.wav")

        # Start Screen UI
        self.title_label = TitleLabel()
        self.start_button = StartButton()
        self.final_score_label = FinalScoreLabel()

        # Gameplay UI
        self.score_label = ScoreLabel()
        self.timer_label = TimerLabel()
        self.round_label = RoundLabel()

        # Sprites
        self.targets = []
        for _ in range(TARGET_COUNT):
            new_target = Target(self)
            self.targets.append(new_target)

        self.sprites = [
            self.title_label, self.start_button, self.final_score_label, self.score_label, 
            self.timer_label, self.round_label, self.targets
        ]

        self.gamestate = GameState.INITIALIZING

    @property
    def gamestate(self):
        return self.__gamestate

    @gamestate.setter
    def gamestate(self, newGamestate):
        if (newGamestate in GameState and newGamestate != self.__gamestate):
            self.__gamestate = newGamestate
            self.__handleGamestateChange()

    def __handleGamestateChange(self):
        match self.__gamestate:
            case GameState.INITIALIZING:
                self.title_label.hide()
                self.score_label.hide()
                self.timer_label.hide()
                self.round_label.hide()
                self.final_score_label.hide()
                self.start_button.hide()
                for target in self.targets:
                    target.hide()

                self.gamestate = GameState.START
            case GameState.START:
                self.title_label.show()
                self.start_button.show()

                if self.last_score > 0:
                    self.final_score_label.text = f"Last Score: {self.last_score}"
                    self.final_score_label.show()
            case GameState.PLAYING:
                self.title_label.hide()
                self.start_button.hide()
                self.final_score_label.hide()
                self.score_label.show()
                self.timer_label.show()
                self.round_label.show()
                
                self.current_round = 1
                self.score = 0
                self.round_label.text = f"Round: {self.current_round}"
                self.score_label.text = "Score: 0"
                self.game_timer.start()
                self.spawn_round_targets()
            case GameState.END:
                self.score_label.hide()
                self.timer_label.hide()
                self.round_label.hide()
                for target in self.targets:
                    target.reset()

                self.final_score_label.show()
                self.start_button.text = "Play Again"
                self.gamestate = GameState.START

    def spawn_round_targets(self):
        for target in self.targets:
            target.spawn()

    def process(self):
        match self.gamestate:
            case GameState.START:
                if self.start_button.clicked:
                    self.gamestate = GameState.PLAYING
            case GameState.PLAYING:
                # Update and check game timer
                time_left = self.game_timer.getTimeLeft()
                self.timer_label.text = f"Time: {max(time_left, 0):.2f}"
                self.round_label.text = f"Round: {self.current_round}"

                if time_left <= 0:
                    if self.current_round < ROUND_COUNT:
                        self.current_round += 1
                        self.game_timer.start()
                        for target in self.targets:
                            target.reset()
                        self.spawn_round_targets()
                    else:
                        self.last_score = self.score
                        self.gamestate = GameState.END

if __name__ == "__main__":
    game = Game()
    game.start()
