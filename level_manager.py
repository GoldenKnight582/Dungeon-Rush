import pygame
import random
import player
import enemy
import noise


class LevelManager():
    def __init__(self, win, state):
        self.win = win
        self.screen_dim = (win.get_width(), win.get_height())
        self.clock = pygame.time.Clock()
        self.state = state
        self.party = {"Warrior": player.Warrior((200, self.screen_dim[1] // 2 - 20), None, None, self.win), "Archer":
                      player.Archer((200, self.screen_dim[1] // 2 - 20), None, None, self.win), "Wizard":
                      player.Wizard((200, self.screen_dim[1] // 2 - 20), None, None, self.win)}
        self.player = self.party["Warrior"]
        self.arrow = self.party["Archer"].arrow
        self.combat_encounter = []
        self.current_opponent = None
        self.cur_menu = "Main"

        # UI
        self.runner_abilities = {"Warrior": ["Strike", "idk"], "Archer": ["Shot", "Leap"], "Wizard": ["Shield", "Shrink"]}

        # Font
        self.title = pygame.font.Font("Fonts\\Orbitron-Regular.ttf", 45)
        self.header = pygame.font.Font("Fonts\\Orbitron-Regular.ttf", 30)
        self.normal = pygame.font.Font("Fonts\\Orbitron-Regular.ttf", 20)

        # Combat Stuff
        self.combat_menu = {"Main": {1: "Attack", 2: "Abilities", 3: "Swap"}, "Swapping":
                            {1: "Warrior", 2: "Archer", 3: "Wizard"}, "Abilities":
                            self.player.abilities}
        self.attack_delay = 0
        self.turn = "Player"
        self.turn_count = 1

        # World Generation and Scrolling data
        self.true_scroll = [0, 0]
        self.CHUNK_SIZE = 16
        self.game_map = {}
        self.grass_img = pygame.image.load('images\\cobblestone.jpg')
        self.dirt_img = pygame.image.load('images\\rock.png')
        self.plant_img = pygame.image.load('images\\plant.png').convert()
        self.plant_img.set_colorkey((255, 255, 255))
        self.tile_index = {1: self.grass_img, 2: self.dirt_img, 3: self.plant_img}
        self.tile_rects = []
        self.cave_img = pygame.image.load('Images\\cave.png')
        # credits for cave img = http://pixeljoint.com/forum/forum_posts.asp?TID=15971&PD=0
        self.cave_scroll_x = 0
        self.score = -56
        self.distance = -56

        # Title Screen
        self.start_rect = None
        self.start_hover = False
        self.quit_rect = None
        self.quit_hover = False
        self.logo = pygame.image.load("Images\\logo.png")

        # Music by AlexisOrtizSofield from Pixabay
        pygame.mixer.music.load("audio\\music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Obstacle Spawn Data
        self.onscreen_enemies = []
        self.spawn_range = (1.7, 3.2)
        self.enemy_spawn_timer = random.uniform(self.spawn_range[0], self.spawn_range[1])

        # spawning of attacks
        self.warrior_attack_img = pygame.image.load("Images\\sword.png")
        self.warrior_attack_img_resize = pygame.transform.scale(self.warrior_attack_img, (100,100))
        self.thunderbolt_image = pygame.image.load("Images\\lightning.png")
        self.effect_images = self.warrior_attack_img_resize
        self.cur_effect_img = self.effect_images
        self.effect_speed = 10
        self.effect_origin = 225

    def generate_chunk(self, x, y):
        cal = self.screen_dim[1] / 2 / self.CHUNK_SIZE
        chunk_data = []
        for y_pos in range(self.CHUNK_SIZE):
            for x_pos in range(self.CHUNK_SIZE):
                target_x = x * self.CHUNK_SIZE + x_pos
                target_y = y * self.CHUNK_SIZE + y_pos
                tile_type = 0 # nothing
                height = int(noise.pnoise1(target_x * 0.1, repeat=100000) * 2)
                if target_y > cal - height * 6:
                    tile_type = 2 # dirt
                elif target_y == cal - height * 6:
                    tile_type = 1 # grass
                if tile_type != 0:
                    chunk_data.append([[target_x,target_y],tile_type])
        return chunk_data

    def update(self):
        """
        General updates called every frame
        """
        global mid_attack
        delta_time = self.clock.tick() / 1000

        # Title Screen Updates
        if self.state == "Title" or self.state == "Resume":
            mouse_pos = pygame.mouse.get_pos()
            if self.start_rect:
                if self.start_rect[0] - 5 < mouse_pos[0] < self.start_rect[0] + self.start_rect[2] + 5 and \
                        self.start_rect[1] - 5 < mouse_pos[1] < self.start_rect[1] + self.start_rect[3] + 5:
                    self.start_hover = True
                else:
                    self.start_hover = False
            if self.quit_rect:
                if self.quit_rect[0] - 5 < mouse_pos[0] < self.quit_rect[0] + self.quit_rect[2] + 5 and \
                        self.quit_rect[1] - 5 < mouse_pos[1] < self.quit_rect[1] + self.quit_rect[3] + 5:
                    self.quit_hover = True
                else:
                    self.quit_hover = False

        if self.state == "Runner":
            self.runner_cooldowns(delta_time)
            self.player.update(self.state, self.tile_rects, delta_time, self.turn_count, self.party, self.onscreen_enemies)
            self.arrow = self.party["Archer"].arrow
            if self.arrow is not None:
                result = self.arrow.update(delta_time, self.onscreen_enemies)
                if result:
                    self.arrow = None
                    self.party["Archer"].arrow = None
            self.cave_scroll_x -= 3
            for e in self.onscreen_enemies:
                if e.x <= self.distance:
                    self.score += e.enemy_point
                    e.enemy_point = 0
            # Sync the current jump power for the whole party
            self.sync_party()
            # Spawn timer
            self.enemy_spawn_timer -= delta_time
            # Enemy Collision and Combat Generation
            for e in self.onscreen_enemies:
                if e.weapon_collision:
                    self.onscreen_enemies.remove(e)
                    self.score += 150
                    break
                hit = e.update(delta_time, self.player.x, self.player.y)
                if hit and self.party["Wizard"].runner_moves["Shield"][0] <= 0:
                    self.combat_encounter = [e]
                    for i in range(random.randint(1, 2)):
                        new_enemy = enemy.BasicEnemyTypeTest((self.screen_dim[0] // 2, self.screen_dim[1] // 2 - 20), self.state, self.player.speed)
                        self.combat_encounter.append(new_enemy)
                    self.onscreen_enemies.remove(e)
                    for ec in self.combat_encounter:
                        ec.x = 600
                        ec.y = 380
                    for character in self.party:
                        self.party[character].y = 380
                    self.attack_delay = 0
                    mid_attack = False
                    self.state = "Combat"
            # Despawn offscreen enemies
            for e in self.onscreen_enemies:
                if e.x + e.radius <= 0:
                    self.onscreen_enemies.remove(e)

        if self.state == "Combat":
            self.attack_delay -= delta_time
            self.current_opponent = self.combat_encounter[0]
            if self.turn == "Player":
                if self.attack_delay > 0:
                    self.effect_origin += delta_time + self.effect_speed
                if self.cur_menu == "Main":
                    if self.player.selection_made:
                        if self.player.selection == 1:
                            if self.attack_delay <= 0 and not mid_attack:
                                self.attack_delay = 0.25
                                self.effect_origin = 215
                                if self.player.__class__ == player.Warrior:
                                    self.cur_effect_img = self.warrior_attack_img_resize
                                elif self.player.__class__ == player.Archer:
                                    self.cur_effect_img = self.warrior_attack_img_resize    # Swap with arrow image
                                else:
                                    self.cur_effect_img = self.warrior_attack_img_resize    # Swap with something else?
                                mid_attack = True
                            if self.attack_delay <= 0 and mid_attack:
                                self.attack(self.player, self.current_opponent)
                                mid_attack = False
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
                if self.attack_delay > 0:
                    self.effect_origin -= delta_time + self.effect_speed
                if self.current_opponent:
                    if self.attack_delay <= 0:
                        self.effect_origin = 500
                        self.cur_effect_img = self.warrior_attack_img_resize
                        self.attack(self.current_opponent, self.player)
                        self.player.selection_made = False
            if self.current_opponent.health <= 0:
                self.score += 50
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
        self.change_turn()

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
        for character in self.party:
            self.party[character].x = self.player.x
            self.party[character].y = self.player.y
            self.party[character].jump_power = self.player.jump_power

    def runner_cooldowns(self, dt):
        for character in self.party:
            for ability in self.party[character].runner_moves:
                if self.party[character].runner_moves[ability][0] > 0:
                    self.party[character].runner_moves[ability][0] -= dt
                    if self.party[character].runner_moves[ability][0] <= 0:
                        self.party[character].runner_moves[ability][1] = self.party[character].runner_moves[ability][2]
                elif self.party[character].runner_moves[ability][1] > 0:
                    self.party[character].runner_moves[ability][1] -= dt

    def change_turn(self):
        if self.turn == "Player":
            self.turn = "Enemy"
            self.attack_delay = 0.25
        else:
            self.turn = "Player"
        self.turn_count += 1

    def handle_input(self):
        """
        Handles input between the player and UI / game objects
        :return: True if the player is exiting the game
        """
        event = pygame.event.poll()

        if self.state == "Runner":
            self.player = self.party[self.player.handle_running_input(event)]
        elif self.state == "Combat":
            self.player.handle_combat_input(event, self.cur_menu)

        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == "Title" or self.state == "Resume":
                    return True
                else:
                    self.state = "Resume"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.start_hover:
                if self.state == "Title" or self.state == "Resume":
                    self.state = "Runner"
            if event.button == 1 and self.quit_hover:
                return True

    def draw(self):
        self.win.blit(self.cave_img, (self.cave_scroll_x, 0))
        self.win.blit(self.cave_img, (self.cave_scroll_x + self.cave_img.get_width(), 0))
        if self.state == "Runner" or self.state == "Combat":
            score = self.header.render("Score: " + str(int(self.score)), False, (255, 255, 0))
            pygame.draw.rect(self.win, (0, 0, 0), (0, 0, self.win.get_width(), 50))
            self.win.blit(score, (self.win.get_width() - score.get_width() - 15, 5))
        if self.cave_scroll_x <= -self.cave_img.get_width():
            self.cave_scroll_x = 0
        if self.state == "Title" or self.state == "Resume":
            self.draw_title_screen(self.start_hover, self.quit_hover)
        elif self.state == "Runner":
            self.draw_level()
        elif self.state == "Combat":
            if self.player.selection is not None:
                self.draw_combat_screen(self.combat_encounter, self.player.selection)
                if self.attack_delay > 0:
                    self.win.blit(self.cur_effect_img, (self.effect_origin, 325))
        pygame.display.flip()

    def draw_level(self):
        self.player.draw()
        if self.party["Wizard"].runner_moves["Shield"][0] > 0:
            self.win.blit(self.party["Wizard"].shield_surf,
                          (int(self.player.x - self.player.radius), int(self.player.y - self.player.radius)))
        if self.arrow is not None:
            self.arrow.draw()
        self.true_scroll[0] += self.player.speed
        # self.true_scroll[1] += (self.player.y-self.true_scroll[1]-106)/20
        # self.true_scroll[0] += 0
        self.true_scroll[1] += 0
        scroll = self.true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        
        self.tile_rects = []
        for y in range(7):
            for x in range(8):
                target_x = x - 1 + int(round(scroll[0]/(self.CHUNK_SIZE*16)))
                target_y = y - 1 + int(round(scroll[1]/(self.CHUNK_SIZE*16)))
                target_chunk = str(target_x) + ';' + str(target_y)
                if target_chunk not in self.game_map:
                    self.game_map[target_chunk] = self.generate_chunk(target_x,target_y)
                    for tile in self.game_map[target_chunk]:
                        if tile[1] == 1 and self.enemy_spawn_timer <= 0:
                            # Spawn enemies
                            self.onscreen_enemies.append(enemy.BasicEnemyTypeTest((tile[0][0] * 16 - scroll[0] + 20, tile[0][1] * 16 - scroll[1] - 20), "Runner", self.player.speed))
                            self.enemy_spawn_timer = random.uniform(self.spawn_range[0], self.spawn_range[1])
                    self.score += 1
                    self.distance += 1
                for tile in self.game_map[target_chunk]:
                    self.win.blit(self.tile_index[tile[1]], (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]))
                    if tile[1] in [1, 2]:
                        self.tile_rects.append(pygame.Rect(tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1], 16, 16))
        for e in self.onscreen_enemies:
            e.draw(self.win)
        n = 0
        for ability in self.player.runner_moves:
            n += 1
            size = 40
            halfsize = 20
            rect = pygame.Rect(self.screen_dim[0] // 2 - halfsize - (n * (size + 5)), 5, size, size)
            pygame.draw.rect(self.win, (255, 255, 255), rect, 1)
            if self.player.runner_moves[ability][1] > 0:
                y_calc = (1 - (self.player.runner_moves[ability][1] / self.player.runner_moves[ability][2])) / 2.5 * 100
                pygame.draw.line(self.win, (179, 0, 119), (rect.left, rect.top + int(y_calc)), (rect.right, rect.top + int(y_calc)))

    def draw_combat_screen(self, enemy_list, selection):
        # Color Palette
        menu_space_color = (176, 166, 156)
        text_color = (255, 73, 48)
        offset = self.player.selection - 1
        self.player.draw()
        if self.current_opponent:
            self.current_opponent.draw(self.win)
        if len(self.combat_encounter) > 1:
            # Show Upcoming Enemy
            temp = self.normal.render("Next Enemy:", False, text_color)
            pygame.draw.rect(self.win, (20, 20, 20), (645, 140, temp.get_width() + 15, temp.get_height() + 60))
            pygame.draw.rect(self.win, (230, 60, 0), (645, 140, temp.get_width() + 15, temp.get_height() + 60), 5)
            self.win.blit(temp, (650, 150))
            self.combat_encounter[1].draw_portrait(self.win)
        # Menu Options
        for i in range(len(self.combat_menu["Main"])):
            temp = self.header.render(self.combat_menu["Main"][i + 1], False, text_color)
            self.win.blit(temp, (100, (self.screen_dim[1] * (0.6 + 0.05 * i))))
        # Selection Arrow
        if selection != 0:
            if self.cur_menu == "Abilities":
                pygame.draw.polygon(self.win, (0, 0, 0), ((50, 525), (50, 555),
                                                          (95, 540)))
            elif self.cur_menu == "Swapping":
                pygame.draw.polygon(self.win, (0, 0, 0), ((50, 565), (50, 595),
                                                          (95, 580)))
            else:
                pygame.draw.polygon(self.win, (0, 0, 0), ((50, 485 + offset * 40), (50, 515 + (offset * 40)),
                                                          (95, 500 + offset * 40)))
        # Player Health
        temp = self.header.render(str(self.player.health), False, text_color)
        self.win.blit(temp, (self.player.x - temp.get_width() // 2, self.player.y - 100))
        # Opponent Health
        temp = self.header.render(str(self.current_opponent.health), False, text_color)
        self.win.blit(temp, (self.current_opponent.x - temp.get_width() // 2, self.current_opponent.y - 100))
        # Turn Info
        temp = self.header.render(self.turn + " Turn!", False, text_color, menu_space_color)
        self.win.blit(temp, (50, 725))
        # Ability Submenu
        if self.cur_menu == "Abilities":
            for i in range(len(self.player.abilities)):
                temp = self.header.render(self.player.abilities[i], False, text_color)
                self.win.blit(temp, (400, (self.screen_dim[1] * (0.6 + 0.05 * i))))
            # Selection Arrow
            if selection != 0:
                pygame.draw.polygon(self.win, (0, 0, 0), ((350, 485 + offset * 40), (350, 515 + offset * 40),
                                                          (395, 500 + offset * 40)))
        elif self.cur_menu == "Swapping":
            # Menu Options
            align = 0
            for i in self.combat_menu["Swapping"]:
                if self.combat_menu["Swapping"][i] != self.player.__class__.__name__:
                    temp = self.header.render(self.combat_menu["Swapping"][i], False, text_color)
                    align = 0
                    if self.player.__class__ == player.Warrior:
                        align = 1
                    elif self.player.__class__ == player.Archer and i == 3:
                        align = 1
                    self.win.blit(temp, (400, self.screen_dim[1] * (0.6 + 0.05 * (i - 1 - align))))
            # Selection Arrow
            if selection != 0:
                if self.player.__class__ == player.Archer and selection == 1:
                    align = 0
                pygame.draw.polygon(self.win, (0, 0, 0), ((350, 485 + (offset - align) * 40), (350, 515 + (offset - align) * 40),
                                                          (395, 500 + (offset - align) * 40)))

    def draw_title_screen(self, start_highlight=False, quit_highlight=False):
        bg_color = (150, 150, 150)
        title_color = (255, 0, 51)
        highlight_color = (0, 170, 200)
        self.win.fill(bg_color)
        self.win.blit(self.logo, (self.screen_dim[0] // 2 - self.logo.get_width() // 2, int(self.screen_dim[1] * 0.1)))
        temp = self.title.render("Dungeon Rush", False, title_color, bg_color)
        self.win.blit(temp, (self.screen_dim[0] // 2 - temp.get_width() // 2, self.screen_dim[1] // 3 - temp.get_height() // 2))
        temp = self.header.render("By Tyler Cobb and Chase Minor", False, (0, 0, 0), bg_color)
        self.win.blit(temp, (self.screen_dim[0] // 2 - temp.get_width() // 2, self.screen_dim[1] * 0.37))

        if not start_highlight:
            if self.state == "Title":
                temp = self.header.render("Start Game", False, title_color, bg_color)
            elif self.state == "Resume":
                temp = self.header.render("Resume Game", False, title_color, bg_color)
        else:
            if self.state == "Title":
                temp = self.header.render("Start Game", False, highlight_color, bg_color)
            elif self.state == "Resume":
                temp = self.header.render("Resume Game", False, highlight_color, bg_color)
        self.start_rect = temp.get_rect()
        self.start_rect[0] = self.screen_dim[0] // 2 - temp.get_width() // 2
        self.start_rect[1] = int(self.screen_dim[1] * 0.55)
        self.win.blit(temp, (self.screen_dim[0] // 2 - temp.get_width() // 2, int(self.screen_dim[1] * 0.55)))
        if not quit_highlight:
            temp = self.header.render("Quit Game", False, title_color, bg_color)
        else:
            temp = self.header.render("Quit Game", False, highlight_color, bg_color)
        self.quit_rect = temp.get_rect()
        self.quit_rect[0] = self.screen_dim[0] // 2 - temp.get_width() // 2
        self.quit_rect[1] = int(self.screen_dim[1] * 0.6)
        self.win.blit(temp, (self.screen_dim[0] // 2 - temp.get_width() // 2, int(self.screen_dim[1] * 0.63)))
        if self.state == "Resume":
            temp = self.title.render("Score: " + str(self.score), False, title_color, bg_color)
            self.win.blit(temp, (self.screen_dim[0] // 2 - temp.get_width() // 2, int(self.screen_dim[1] * 0.75)))
