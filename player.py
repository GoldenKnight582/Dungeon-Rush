import pygame
import math


class Player:
    def __init__(self, start_pos, image, scale, surf):
        self.color = None
        self.x = start_pos[0]
        self.y = start_pos[1]  
#        self.image = pygame.image.load(image)
#        self.width = self.image.get_width()
#        self.height = self.image.get_height()
#        self.scaled_image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
#        self.width *= scale
#        self.height *= scale
        self.radius = 20
        self.jump_power = 0
        self.grav = 90
        self.speed = 150
        self.can_jump = True
        self.surf = surf
        self.rect = pygame.draw.circle(self.surf, (0, 255, 0), (int(self.x), int(self.y)), self.radius)
        self.selection = None
        self.selection_made = False
        self.special_effect = None
        self.defense = 0
        self.abilities = []
        self.ability_cooldowns = [0, 0]
        self.buffs = []
        self.fortify = ["False", 0]
        self.sound = pygame.mixer.Sound("audio\\bouncy.wav")
        self.sound.set_volume(0.5)

    def do_ability(self, opponent, party):
        pass

    def collision_test(self, tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def move_and_collide(self, tiles, dt):
        collision_types = {"bottom": False, "right": False}
#        collisions = self.collision_test(tiles)
#        for tile in collisions:
#            if tile.top <= self.rect.top:
#                self.rect.right = tile.left
#                self.x = self.rect.right - self.radius
#                collision_types["right"] = True
        self.y += self.jump_power * 3 * dt
        self.rect = pygame.draw.circle(self.surf, (0, 255, 0), (int(self.x), int(self.y)), self.radius)
        collisions = self.collision_test(tiles)
        for tile in collisions:
            if self.jump_power > 0:
                self.rect.bottom = tile.top
                self.y = self.rect.bottom - self.radius
                collision_types["bottom"] = True
#            elif self.jump_power < 0:
#                self.rect.top = tile.bottom
#                self.y = self.rect.top += self.rect.top
#                collision_types["top"] = True
        return collision_types

    def update(self, game_state, tiles, dt, enemy_list):
        if game_state == "Runner":
            self.jump_power += (self.grav * dt) ** 2 + 2
            if self.jump_power > 100:
                self.jump_power = 100

            collisions = self.move_and_collide(tiles, dt)
            if collisions["bottom"]:
                self.jump_power = 0.25
                self.can_jump = True

        elif game_state == "Combat":
            # Apply / Remove Fortify buff
            if "Fortify" in self.buffs and self.fortify[0] == "False":
                self.defense *= 1.5
                self.fortify[0] = "True"
                self.fortify[1] = 4
            if self.fortify[1] == 0 and self.fortify[0] == "True":
                self.defense /= 1.5
                self.buffs.remove("Fortify")
                self.fortify[0] = "False"

    def handle_running_input(self, evt):
        cur_class = self.__class__.__name__
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_SPACE:
                if self.can_jump:
                    self.jump_power = -175
                    self.can_jump = False
            if evt.key == pygame.K_q:
                if self.__class__.__name__ == "Warrior":
                    cur_class = "Wizard"
                elif self.__class__.__name__ == "Archer":
                    cur_class = "Warrior"
                else:
                    cur_class = "Archer"
            if evt.key == pygame.K_e:
                if self.__class__.__name__ == "Warrior":
                    cur_class = "Archer"
                elif self.__class__.__name__ == "Archer":
                    cur_class = "Wizard"
                else:
                    cur_class = "Warrior"
        return cur_class

    def handle_combat_input(self, evt, menu):
        if self.selection == None:
            if menu == "Main" or menu == "Abilities":
                self.selection = 1
            if menu == "Swapping":
                if self.__class__.__name__ == "Warrior":
                    self.selection = 2
                if self.__class__.__name__ == "Archer" or self.__class__.__name__ == "Wizard":
                    self.selection = 1
            self.selection_made = False
        if evt.type == pygame.KEYDOWN:
            if not self.selection_made:
                if evt.key == pygame.K_w:
                    self.selection -= 1
                    if menu == "Main":
                        if self.selection < 1:
                            self.selection = 3
                    elif menu == "Abilities":
                        if self.selection < 1:
                            self.selection = len(self.abilities)
                    elif menu == "Swapping":
                        if self.__class__.__name__ == "Warrior":
                            if self.selection < 2:
                                self.selection = 3
                        elif self.__class__.__name__ == "Archer":
                            if self.selection < 1:
                                self.selection = 3
                            elif self.selection == 2:
                                self.selection = 1
                        else:
                            if self.selection < 1:
                                self.selection = 2
                elif evt.key == pygame.K_s:
                    self.selection += 1
                    if menu == "Main":
                        if self.selection > 3:
                            self.selection = 1
                    elif menu == "Abilities":
                        if self.selection > len(self.abilities):
                            self.selection = 1
                    elif menu == "Swapping":
                        if self.__class__.__name__ == "Warrior":
                            if self.selection > 3:
                                self.selection = 2
                        elif self.__class__.__name__ == "Archer":
                            if self.selection > 3:
                                self.selection = 1
                            elif self.selection == 2:
                                self.selection = 3
                        else:
                            if self.selection > 2:
                                self.selection = 1
                elif evt.key == pygame.K_RETURN:
                    self.selection_made = True
            if evt.key == pygame.K_BACKSPACE:
                if menu == "Swapping" or menu == "Abilities":
                    self.selection = 0
                    self.selection_made = True

    def draw(self):
        pygame.draw.circle(self.surf, (self.color), (int(self.x), int(self.y)), self.radius)
        # Collision rect for debug
#        pygame.draw.rect(self.surf, (255, 0, 0), self.rect, 1)

    def draw_portrait(self, x):
        pygame.draw.circle(self.surf, self.color, (int(x), 25), self.radius // 2)


class Warrior(Player):

    def __init__(self, start_pos, image, scale, surf):
        super().__init__(start_pos, image, scale, surf)
        self.color = (0, 255, 0)
        self.health = 250
        self.max_health = self.health
        self.attack = 60
        self.defense = 40
        self.luck = 0.05
        self.dodge = 0.03
        self.runner_moves = {"Strike": [0.0, 0, 1]}
        self.abilities = ["Fortify", "Overwhelm"]
        self.ability_cooldowns = [0, 0, 7, 0]

    def do_ability(self, opponent, party):
        if self.selection == 1 and self.ability_cooldowns[0] == 0:
            for character in party:
                party[character].buffs.append("Fortify")

    def update(self, game_state, tiles, dt, enemy_list):
        super().update(game_state, tiles, dt, enemy_list)
        if self.runner_moves["Strike"][0] > 0:
            self.strike(enemy_list)

    def handle_running_input(self, evt):
        cur_class = super().handle_running_input(evt)
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1 and self.can_jump:
                if self.runner_moves["Strike"][1] <= 0 and self.runner_moves["Strike"][0] <= 0:
                    self.runner_moves["Strike"][0] = 0.5
        return cur_class

    def strike(self, enemies):
        collision_rect = pygame.Rect(self.x + self.radius, self.y - self.radius - 10, 50, 70)
        for e in enemies:
            if collision_rect.colliderect(e.rect):
                e.weapon_collision = True

    def draw(self):
        super().draw()
        if self.runner_moves["Strike"][0] > 0:
            pygame.draw.rect(self.surf, (255, 0, 0), (self.x + self.radius, self.y - self.radius - 10, 60, 70), 1)


class Archer(Player):

    def __init__(self, start_pos, image, scale, surf):
        super().__init__(start_pos, image, scale, surf)
        self.color = (255, 255, 0)
        self.health = 180
        self.max_health = self.health
        self.attack = 45
        self.defense = 20
        self.luck = 0.08
        self.dodge = 0.06
        self.arrow = None
        self.runner_moves = {"Snipe": [0, 0, 2.5]}
        self.abilities = ["Rapidfire", "Take Cover"]
        self.ability_cooldowns = [0, 0, 0, 0]

    def handle_running_input(self, evt):
        cur_class = super().handle_running_input(evt)
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1:
                if self.runner_moves["Snipe"][1] <= 0:
                    self.snipe(evt.pos)
        return cur_class

    def snipe(self, mouse_pos):
        adjacent = mouse_pos[0] - self.x
        opposite = -1 * (mouse_pos[1] - self.y)  # Account for inverted y-axis
        angle = math.atan2(opposite, adjacent)
        start_x = self.x + self.radius
        self.arrow = Arrow(start_x, self.y, self.surf)
        self.arrow.horizontal_speed = self.arrow.speed * math.cos(angle)
        self.arrow.vertical_speed = -self.arrow.speed * math.sin(angle)
        self.runner_moves["Snipe"][1] = self.runner_moves["Snipe"][2]


class Arrow:

    def __init__(self, start_x, start_y, surf):
        self.x = start_x
        self.y = start_y
#       self.image = pygame.image.load(" ")
        self.radius = 5
        self.color = (153, 85, 49)
        self.speed = 700
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.surf = surf
        self.width_edge = surf.get_width()
        self.height_edge = surf.get_height()

    def update(self, dt, enemies):
        # Movement
        self.x += self.horizontal_speed * dt
        self.y += self.vertical_speed * dt

        # Collision with enemies
        collision_rect = pygame.Rect(int(self.x), int(self.y), 15, 5)
        for e in enemies:
            if collision_rect.colliderect(e.rect):
                e.weapon_collision = True
                hit = True
                return hit

        # Boundary check
        if self.y + self.radius > self.height_edge:
            oob = True  # Out of bounds
        elif self.y - self.radius < 0:
            oob = True
        elif self.x - self.radius < 0:
            oob = True
        elif self.x + self.radius > self.width_edge:
            oob = True
        else:
            oob = False
        return oob

    def draw(self):
        pygame.draw.rect(self.surf, self.color, (int(self.x), int(self.y), 15, 5))


class Wizard(Player):

    def __init__(self, start_pos, image, scale, surf):
        super().__init__(start_pos, image, scale, surf)
        self.color = (0, 0, 255)
        self.health = 120
        self.max_health = self.health
        self.attack = 20
        self.defense = 10
        self.luck = 0.1
        self.dodge = 0.1
        self.runner_moves = {"Shield": [0, 0, 10]}
        self.shield_surf = pygame.Surface((self.radius * 2, self.radius * 2))
        self.shield_surf.set_colorkey((0, 0, 0))
        self.shield_surf.set_alpha(150)
        pygame.draw.circle(self.shield_surf, (66, 139, 255), (self.radius, self.radius), self.radius)
        self.abilities = ["Thunderbolt", "Blaze"]
        self.ability_cooldowns = [0, 0, 5, 0]   # First two numbers are current cooldown, second two are corresponding
        # starting cooldowns

    def handle_running_input(self, evt):
        cur_class = super().handle_running_input(evt)
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1:
                if self.runner_moves["Shield"][1] <= 0 and self.runner_moves["Shield"][0] <= 0:
                    self.runner_moves["Shield"][0] = 5
        return cur_class

    def do_ability(self, opponent, party):
        if self.selection == 1:
            return Thunderbolt()


class Thunderbolt:
    def __init__(self):
        self.attack = 60
        self.luck = 0.15
        self.special_effect = "Stun"
        self.effect_chance = 0.8
        bolt_img = pygame.image.load("images\\lightning.png")
        self.image = pygame.transform.scale(bolt_img, (100, 100))

