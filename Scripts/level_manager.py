import pygame
import random
import Scripts.player as player


class LevelManager():
    def __init__(self, win, state):
        self.win = win
        self.screen_dim = (win.get_width(), win.get_height())
        self.clock = pygame.time.Clock()
        self.state = state
        self.player = player.Player((100, self.screen_dim[1] // 2), None, None, self.win)
        self.combat_encounter = []
        self.font = pygame.font.Font("C:\\Users\\tcobb\\PycharmProjects\\Dungeon-Rush\\Fonts\\Orbitron-Regular.ttf", 15)

    def generate_chunk(self,x,y):
        pass

                

    def update(self):
        """
        General updates called every frame
        """
        #print(self.player.jump_power)
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
        if self.state == "Runner":
            self.draw_level()
        elif self.state == "Combat":
            self.draw_combat_screen(self.combat_encounter)
        pygame.display.flip()

    def draw_level(self):
        self.player.draw()

    def draw_combat_screen(self, enemy_list):
        self.player.draw()
#        enemy_list[0].draw()
        menu_space_color = (176, 166, 156)
        pygame.draw.rect(self.win, menu_space_color, (0, 421, self.screen_dim[0], self.screen_dim[1] - 421))

