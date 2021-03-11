import pygame
import player


class LevelManager():
    def __init__(self, win):
        self.win = win
        self.screen_dim = (win.get_width(), win.get_height())
        self.clock = pygame.time.Clock()
        self.state = "Runner"
        self.player = player.Player((100, self.screen_dim[1] // 2), None, None, self.win)

    def generate_chunk(self):
        pass

    def update(self):
        """
        General updates called every frame
        """
        print(self.player.jump_power)
        delta_time = self.clock.tick() / 1000
        self.player.update(self.state, delta_time)

    def handle_input(self):
        """
        Handles input between the player and UI / game objects
        :return: True if the player is exiting the game
        """
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True

        self.player.handle_running_input(event)

    def draw(self):
        self.win.fill((0, 0, 0))
        self.player.draw()
        pygame.display.flip()

    def draw_level(self):
        pass