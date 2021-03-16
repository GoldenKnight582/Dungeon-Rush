
import pygame
import random
import player
import enemy


class LevelManager():
    def __init__(self, win, state):
        self.win = win
        self.screen_dim = (win.get_width(), win.get_height())
        self.clock = pygame.time.Clock()
        self.state = state
        self.party = {"Warrior": player.Warrior((100, self.screen_dim[1] // 2), None, None, self.win), "Archer":
                      player.Archer((100, self.screen_dim[1] // 2), None, None, self.win), "Wizard":
                      player.Wizard((100, self.screen_dim[1] // 2), None, None, self.win)}
        self.player = self.party["Warrior"]
        self.combat_encounter = [enemy.BasicEnemyTypeTest((self.screen_dim[0] // 2, self.screen_dim[1] // 2), self.state)]
        self.current_opponent = self.combat_encounter[0]
        self.cur_menu = "Main"
        self.font = pygame.font.Font("Fonts\\Orbitron-Regular.ttf", 30)
        self.combat_menu = {"Main": {1: "Attack", 2: "Special", 3: "Swap"}, "Swapping":
                            {1: "Warrior", 2: "Archer", 3: "Wizard"}, "Abilities":
                            self.player.abilities}
        self.attack_delay = 0
        self.turn = "Player"
        self.turn_count = 1

    def generate_chunk(self, x, y):
        pass

    def update(self):
        """
        General updates called every frame
        """
        delta_time = self.clock.tick() / 1000
        for character in self.party:
            self.party[character].update(self.state, delta_time, self.turn_count, self.party)

        if self.state == "Runner":
            # Sync the current jump power for the whole party
            self.sync_party()

        if self.state == "Combat":
            self.attack_delay -= delta_time
            if self.turn == "Player":
                if self.cur_menu == "Main":
                    if self.player.selection_made:
                        if self.player.selection == 1:
                            self.attack(self.player, self.current_opponent)
                            self.change_turn()
                        elif self.player.selection == 2:
                            self.menu_change("Abilities")
                        elif self.player.selection == 3:
                            self.menu_change("Swapping")
                elif self.cur_menu == "Abilities":
                    if self.player.selection_made:
                        if self.player.selection == 0:
                            self.menu_change("Main")
                        else:
                            self.player.do_ability(self.current_opponent, self.party)
                            self.change_turn()
                            self.menu_change("Main")
                elif self.cur_menu == "Swapping":
                    if self.player.selection_made:
                        if self.player.selection == 0:
                            self.menu_change("Main")
                        elif self.player.selection == 1:
                            self.player = self.party["Warrior"]
                            self.menu_change("Main")
                            self.change_turn()
                        elif self.player.selection == 2:
                            self.player = self.party["Archer"]
                            self.menu_change("Main")
                            self.change_turn()
                        elif self.player.selection == 3:
                            self.player = self.party["Wizard"]
                            self.player.selection_made = False
                            self.player.selection = None
                            self.cur_menu = "Main"
                            self.change_turn()
            if self.turn == "Enemy":
                if self.current_opponent:
                    if self.attack_delay <= 0:
                        self.attack(self.current_opponent, self.player)
                        self.change_turn()
                        self.player.selection_made = False
            if self.current_opponent.health <= 0:
                self.combat_encounter.remove(self.current_opponent)
            if not self.combat_encounter:
                self.state = "Runner"

    def attack(self, attackee, attacked):
        damage = attackee.attack - random.randint(attacked.defense - 15, attacked.defense)
        if damage < 0:
            damage = 0
        crit_chance = attackee.luck * 100
        if random.randint(crit_chance, 100) == crit_chance:
            damage *= 2
        attacked.health -= damage

    def menu_change(self, next_menu):
        self.player.selection_made = False
        if self.cur_menu == "Swapping":
            self.player.selection = 3
        elif self.cur_menu == "Abilities":
            self.player.selection = 2
        else:
            self.player.selection = None
        self.cur_menu = next_menu

    def sync_party(self):
        self.party["Warrior"].jump_power = self.player.jump_power
        self.party["Archer"].jump_power = self.player.jump_power
        self.party["Wizard"].jump_power = self.player.jump_power

    def change_turn(self):
        if self.turn == "Player":
            self.turn = "Enemy"
            self.attack_delay = 0.33
        else:
            self.turn = "Player"
        self.turn_count += 1

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
            self.player = self.party[self.player.handle_running_input(event)]
        elif self.state == "Combat":
            self.player.handle_combat_input(event, self.cur_menu)

    def draw(self):
        self.win.fill((0, 0, 0))
        if self.state == "Runner":
            self.draw_level()
        elif self.state == "Combat":
            if self.player.selection is not None:
                self.draw_combat_screen(self.combat_encounter, self.player.selection)
        pygame.display.flip()

    def draw_level(self):
        self.player.draw()

    def draw_combat_screen(self, enemy_list, selection):
        self.player.draw()
        self.current_opponent.draw(self.win)
        # Color Palette
        menu_space_color = (176, 166, 156)
        outline_color = (255, 152, 48)
        text_color = (255, 73, 48)
        # Menu Area
        pygame.draw.rect(self.win, menu_space_color, (0, 421, self.screen_dim[0], self.screen_dim[1] - 421))
        pygame.draw.rect(self.win, outline_color, (0, 421, self.screen_dim[0], self.screen_dim[1] - 421), 5)
        offset = self.player.selection - 1
        # Menu Options
        temp = self.font.render("Attack", False, text_color, menu_space_color)
        self.win.blit(temp, (100, self.screen_dim[1] * 0.6))
        temp = self.font.render("Abilities", False, text_color, menu_space_color)
        self.win.blit(temp, (100, self.screen_dim[1] * 0.65))
        temp = self.font.render("Swap", False, text_color, menu_space_color)
        self.win.blit(temp, (100, self.screen_dim[1] * 0.7))
        # Player Health
        temp = self.font.render(str(self.player.health), False, text_color, (0, 0, 0))
        self.win.blit(temp, (self.player.x - self.player.radius * 1.5, self.player.y - 100))
        # Opponent Health
        temp = self.font.render(str(self.current_opponent.health), False, text_color, (0, 0, 0))
        if self.current_opponent.health >= 100:
            self.win.blit(temp, (self.current_opponent.x - self.current_opponent.radius * 1.5, self.current_opponent.y - 100))
        else:
            self.win.blit(temp, (self.current_opponent.x - self.current_opponent.radius - 5, self.current_opponent.y - 100))
        # Selection Arrow
        if selection != 0:
            if self.combat_menu["Main"][selection] == "Attack" and self.cur_menu == "Main":
                pygame.draw.polygon(self.win, (0, 0, 0), ((50, 485), (50, 515), (95, 500)))
            if self.combat_menu["Main"][selection] == "Special" and self.cur_menu == "Main" or self.cur_menu == "Abilities":
                pygame.draw.polygon(self.win, (0, 0, 0), ((50, 525), (50, 555), (95, 540)))
            if self.combat_menu["Main"][selection] == "Swap" and self.cur_menu == "Main" or self.cur_menu == "Swapping":
                pygame.draw.polygon(self.win, (0, 0, 0), ((50, 565), (50, 595), (95, 580)))
        # Turn Info
        temp = self.font.render(self.turn + " Turn!", False, text_color, menu_space_color)
        self.win.blit(temp, (50, 725))
        if self.cur_menu == "Abilities":
            for i in range(len(self.player.abilities)):
                temp = self.font.render(self.player.abilities[i], False, text_color, menu_space_color)
                self.win.blit(temp, (400, (self.screen_dim[1] * (0.6 + 0.05 * i))))
                # Selection Arrow
                if selection != 0:
                    pygame.draw.polygon(self.win, (0, 0, 0), ((350, 485 + offset * 40), (350, 515 + (offset * 40)),
                                                              (395, 500 + offset * 40)))
        if self.cur_menu == "Swapping":
            if self.player.__class__ == player.Warrior:
                # Menu Options
                temp = self.font.render("Archer", False, text_color, menu_space_color)
                self.win.blit(temp, (400, self.screen_dim[1] * 0.6))
                temp = self.font.render("Wizard", False, text_color, menu_space_color)
                self.win.blit(temp, (400, self.screen_dim[1] * 0.65))
                # Selection Arrow
                if selection != 0:
                    if self.combat_menu["Swapping"][selection] == "Archer":
                        pygame.draw.polygon(self.win, (0, 0, 0), ((350, 485), (350, 515), (395, 500)))
                    if self.combat_menu["Swapping"][selection] == "Wizard":
                        pygame.draw.polygon(self.win, (0, 0, 0), ((350, 525), (350, 555), (395, 540)))
            if self.player.__class__ == player.Archer:
                # Menu Options
                temp = self.font.render("Warrior", False, text_color, menu_space_color)
                self.win.blit(temp, (400, self.screen_dim[1] * 0.6))
                temp = self.font.render("Wizard", False, text_color, menu_space_color)
                self.win.blit(temp, (400, self.screen_dim[1] * 0.65))
                # Selection Arrow
                if selection != 0:
                    if self.combat_menu["Swapping"][selection] == "Warrior":
                        pygame.draw.polygon(self.win, (0, 0, 0), ((350, 485), (350, 515), (395, 500)))
                    if self.combat_menu["Swapping"][selection] == "Wizard":
                        pygame.draw.polygon(self.win, (0, 0, 0), ((350, 525), (350, 555), (395, 540)))
            if self.player.__class__ == player.Wizard:
                # Menu Options
                temp = self.font.render("Warrior", False, text_color, menu_space_color)
                self.win.blit(temp, (400, self.screen_dim[1] * 0.6))
                temp = self.font.render("Archer", False, text_color, menu_space_color)
                self.win.blit(temp, (400, self.screen_dim[1] * 0.65))
                # Selection Arrow
                if selection != 0:
                    if self.combat_menu["Swapping"][selection] == "Warrior":
                        pygame.draw.polygon(self.win, (0, 0, 0), ((350, 485), (350, 515), (395, 500)))
                    if self.combat_menu["Swapping"][selection] == "Archer":
                        pygame.draw.polygon(self.win, (0, 0, 0), ((350, 525), (350, 555), (395, 540)))
