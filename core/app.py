from time import sleep_ms, ticks_ms

from core import Display, Input, Sound


class PiconApp:
    running = True
    current_ms = 0


    def __init__(self, display: Display, input: Input, sound: Sound):
        self.display = display
        self.input = input
        self.sound = sound


    def inputs(self):
        raise NotImplementedError(
            f"{type(self).__name__}.inputs() must be implemented."
        )


    def update(self):
        raise NotImplementedError(
            f"{type(self).__name__}.update() must be implemented."
        )


    def render(self):
        raise NotImplementedError(
            f"{type(self).__name__}.render() must be implemented."
        )


    def __render(self):
        self.display.fill(0)
        self.render()
        self.display.show()


    def run(self):
        while self.running:
            self.update_ms()

            # Input
            if self.input.is_ready(self.current_ms):
                self.inputs()

            # Update
            self.update()

            # Render
            self.__render()

        self.sound.stop()
        self.input.restore_debounce()


    def update_ms(self):
        self.current_ms = ticks_ms()


    def quit(self):
        self.running = False


class PiconGame(PiconApp):
    RUNNING_STATE = 0
    WINNER_STATE = 1
    GAME_OVER_STATE = 2

    game_state = -1


    def __init__(self, display, input, sound):
        super().__init__(display, input, sound)
        self.game_state = PiconGame.RUNNING_STATE


    def __render(self):
        self.display.fill(0)
        self.render()

        if self.game_state == PiconGame.WINNER_STATE:
            self.display.center_text("WINNER", True)
            self.display.show()
            sleep_ms(1000)
            self.quit()
        elif self.game_state == PiconGame.GAME_OVER_STATE:
            self.display.center_text("GAME OVER", True)
            self.display.show()
            sleep_ms(1000)
            self.quit()
        else:
            self.display.show()


    def winner(self):
        self.game_state = PiconGame.WINNER_STATE


    def game_over(self):
        self.game_state = PiconGame.GAME_OVER_STATE
