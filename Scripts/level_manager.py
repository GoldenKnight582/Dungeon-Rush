import pygame
import Scripts.player as player


class LevelManager():
    def __init__(self, win, state):
        self.win = win
        self.screen_dim = (win.get_width(), win.get_height())
        self.clock = pygame.time.Clock()
        self.state = state
        self.player = player.Player((100, self.screen_dim[1] // 2), None, None, self.win)
        self.combat_encounter = []
        self.font = pygame.font.Font("C:\\Users\\tcobb\\PycharmProjects\\Dungeon-Rush\\Fonts\\Orbitron-Regular.ttf", 30)
        self.combat_options = {1: "Attack", 2: "Special", 3: "Swap"}
        self.menu_selection = None

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

        if self.state == "Runner":
            self.player.handle_running_input(event)
        elif self.state == "Combat":
            self.menu_selection = self.player.handle_combat_input(event)

    def draw(self):
        self.win.fill((0, 0, 0))
        if self.state == "Runner":
            self.draw_level()
        elif self.state == "Combat":
            self.draw_combat_screen(self.combat_encounter, self.combat_options[self.menu_selection])
        pygame.display.flip()

    def draw_level(self):
        self.player.draw()

    def draw_combat_screen(self, enemy_list, selection):
        self.player.draw()
#        enemy_list[0].draw()
        menu_space_color = (176, 166, 156)
        outline_color = (255, 136, 102)
        text_color = (255, 22, 54)
        pygame.draw.rect(self.win, menu_space_color, (0, 421, self.screen_dim[0], self.screen_dim[1] - 421))
        pygame.draw.rect(self.win, outline_color, (0, 421, self.screen_dim[0], self.screen_dim[1] - 422), 5)
        # Menu Text
        temp = self.font.render("Attack", False, text_color, menu_space_color)
        self.win.blit(temp, (100, self.screen_dim[1] * 0.6))
        temp = self.font.render("Special", False, text_color, menu_space_color)
        self.win.blit(temp, (100, self.screen_dim[1] * 0.65))
        temp = self.font.render("Swap", False, text_color, menu_space_color)
        self.win.blit(temp, (100, self.screen_dim[1] * 0.7))
        # Arrow
        if selection == "Attack":
            pygame.draw.polygon(self.win, (0, 0, 0), ((50, 510), (50, 485), (95, 498)))
        if selection == "Special":
            pygame.draw.polygon(self.win, (0, 0, 0), ((50, 550), (50, 525), (95, 538)))
        if selection == "Swap":
            pygame.draw.polygon(self.win, (0, 0, 0), ((50, 593), (50, 568), (95, 581)))

