import pygame


class LevelManager():
    def __init__(self, win):
        self.win = win
        self.screen_dim = (win.get_width(), win.get_height())
        self.clock = pygame.time.Clock()
        self.state = ""
        self.delta = 0.0

    def generate_chunk(self):
        pass

    def update(self):
        """
        General updates called every frame
        """
        self.delta = self.clock.tick() / 1000

    def handle_input(self):
        """
        Handles input between the player and UI / game objects
        :return: True if the player is exiting the game
        """
        pass

    def draw_level(self):
        pass