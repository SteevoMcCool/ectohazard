import pygame
import pygame_menu

class MainMenu:
    def __init__(self, game_instance):
        self.game = game_instance
        self.menu = pygame_menu.Menu(
            title='Main Menu',
            width=1280,
            height=720,
            theme=pygame_menu.themes.THEME_BLUE
        )

        self.menu.add.button('Play', self._on_play)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.enable()

    def _on_play(self):
        self.game.game_running = True
        self.menu.disable()

class PauseMenu:
    def __init__(self, game_instance):
        self.game = game_instance
        self.menu = pygame_menu.Menu(
            title='Paused',
            width=600,
            height=400,
            theme=pygame_menu.themes.THEME_DARK
        )

        self.menu.add.button('Resume', self._on_resume)
        self.menu.add.button('Main Menu', self._on_return_main)
        self.menu.add.button('Save', self._on_save)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.disable()

    def _on_resume(self):
        self.menu.disable()

    def _on_return_main(self):
        self.menu.disable()
        self.game.game_running = False

        # Re-enable MainMenu so it's ready when we loop back
        self.game.main.menu.enable()

    def _on_save(self):
        # TODO: IMPLEMENT THE SAVE LOGIC
        return


# TODO: IMPLEMENT THE SAVE MENU
class SaveMenu:
    def __init__(self):
        pass