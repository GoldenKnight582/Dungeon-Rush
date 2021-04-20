import pygame
import math


class Player:
    def __init__(self, start_pos, sprite_sheet, scale, surf):
        self.color = None
        self.x = start_pos[0]
        self.y = start_pos[1]  
        ogsheet = sprite_sheet
        self.ssheet = pygame.transform.scale(ogsheet, (int(ogsheet.get_width() * scale), int(ogsheet.get_height() * scale)))
        self.width = self.ssheet.get_width() // 3
        self.half_width = self.width // 2
        self.height = self.ssheet.get_height()
        self.portrait_image = ogsheet
        self.portrait_width = ogsheet.get_width() // 3
        self.portrait_height = ogsheet.get_height()
        self.jump_power = 0
        self.grav = 90
        self.speed = 300
        self.can_jump = True
        self.surf = surf
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.selection = None
        self.selection_made = False
        self.special_effect = None
        self.cur_frame = 0
        self.anim_timer = 0.1
        self.defense = 0
        self.dodge = 0
        self.base_dodge = 0
        self.abilities = []
        self.ability_cooldowns = [0, 0]
        self.buffs = []
        self.fortify = ["False", 0]
        self.cover = ["False", 0]
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
        self.rect.y = self.y
        collisions = self.collision_test(tiles)
        for tile in collisions:
            if self.jump_power > 0:
                self.rect.bottom = tile.top
                self.y = self.rect.top
                collision_types["bottom"] = True
#            elif self.jump_power < 0:
#                self.rect.top = tile.bottom
#                self.y = self.rect.top += self.rect.top
#                collision_types["top"] = True
        return collision_types

    def update(self, game_state, tiles, dt, enemy_list, hazard_list):
        if game_state == "Runner":
            self.anim_timer -= dt
            if self.anim_timer <= 0:
                self.cur_frame += 1
                self.anim_timer = 0.1
                if self.cur_frame >= 3:
                    self.cur_frame = 0
            self.jump_power += (self.grav * dt) ** 2 + 2
            if self.jump_power > 100:
                self.jump_power = 100
            if not self.can_jump:
                self.cur_frame = 1

            collisions = self.move_and_collide(tiles, dt)
            if collisions["bottom"]:
                self.jump_power = 0.25
                self.can_jump = True
            if self.y >= 410:
                self.can_jump = False

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
            # Apply / Remove Cover buff
            if "Cover" in self.buffs and self.cover[0] == "False":
                self.dodge = 0.33
                self.cover[0] = "True"
                self.cover[1] = 5
            if self.cover[1] == 0 and self.cover[0] == "True":
                self.dodge = self.base_dodge
                self.buffs.remove("Cover")
                self.cover[0] = "False"

    def handle_running_input(self, evt):
        cur_class = self.__class__.__name__
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_SPACE:
                if self.can_jump:
                    self.jump_power = -125
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
        self.surf.blit(self.ssheet, (int(self.x), int(self.y)), (self.width * self.cur_frame, 0, self.width, self.width))
        # Collision rect for debug
#        pygame.draw.rect(self.surf, (255, 0, 0), self.rect, 1)

    def draw_portrait(self, x):
        self.surf.blit(self.portrait_image, (int(x), 5), (self.portrait_width, 0, self.portrait_width, self.portrait_height))


class Warrior(Player):

    def __init__(self, start_pos, sprite_sheet, scale, surf):
        super().__init__(start_pos, sprite_sheet, scale, surf)
        self.color = (0, 255, 0)
        self.health = 250
        self.max_health = self.health
        self.attack = 60
        self.defense = 35
        self.luck = 0.05
        self.dodge = 0.03
        self.base_dodge = 0.03
        self.runner_moves = {"Strike": [0.0, 0, 1]}
        self.abilities = ["Fortify", "Overwhelm"]
        self.ability_cooldowns = [0, 0, 7, 9]
        self.sword = pygame.image.load("images\\sword.png")

    def do_ability(self, opponent, party):
        if self.selection == 1 and self.ability_cooldowns[0] == 0:
            for character in party:
                party[character].buffs.append("Fortify")
        elif self.selection == 2:
            return Overwhelm()

    def update(self, game_state, tiles, dt, enemy_list, hazard_list):
        super().update(game_state, tiles, dt, enemy_list, hazard_list)
        if self.runner_moves["Strike"][0] > 0:
            self.strike(enemy_list, hazard_list)
        if game_state == "Combat":
            self.runner_moves["Strike"][0] = 0

    def handle_running_input(self, evt):
        cur_class = super().handle_running_input(evt)
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1 and self.can_jump:
                if self.runner_moves["Strike"][1] <= 0 and self.runner_moves["Strike"][0] <= 0:
                    self.runner_moves["Strike"][0] = 0.5
        return cur_class

    def strike(self, enemies, hazards):
        collision_rect = pygame.Rect(self.x + self.width, self.y + 5, 50, 70)
        for e in enemies:
            if collision_rect.colliderect(e.rect):
                e.weapon_collision = True
        for h in hazards:
            if collision_rect.colliderect(h.rect):
                h.weapon_collision = True

    def draw(self):
        super().draw()
        if self.runner_moves["Strike"][0] > 0:
            self.surf.blit(self.sword, (self.x + self.width, self.y - self.half_width))


class Overwhelm:
    def __init__(self):
        self.attack = 100
        self.luck = 0.15
        self.special_effect = None
        self.effect_chance = None
        sword_img = pygame.image.load("images\\sword.png")
        self.image = pygame.transform.scale(sword_img, (100, 100))


class Archer(Player):

    def __init__(self, start_pos, sprite_sheet, scale, surf):
        super().__init__(start_pos, sprite_sheet, scale, surf)
        self.color = (255, 255, 0)
        self.health = 180
        self.max_health = self.health
        self.attack = 50
        self.defense = 20
        self.luck = 0.08
        self.dodge = 0.1
        self.base_dodge = 0.1
        self.arrow = None
        self.runner_moves = {"Snipe": [0, 0, 2.5], "Dash": [0, 0, 2]}
        self.abilities = ["Rapidfire", "Take Cover"]
        self.ability_cooldowns = [0, 0, 6, 7]
        self.sound = {"arrow": pygame.mixer.Sound("audio\\arrow.ogg")}

    def handle_running_input(self, evt):
        cur_class = super().handle_running_input(evt)
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1:
                if self.runner_moves["Snipe"][1] <= 0:
                    self.snipe(evt.pos)
            elif evt.button == 3:
                if self.runner_moves["Dash"][1] <= 0:
                    self.runner_moves["Dash"][0] = 0.2
        return cur_class

    def snipe(self, mouse_pos):
        adjacent = mouse_pos[0] - self.x
        opposite = -1 * (mouse_pos[1] - self.y)  # Account for inverted y-axis
        angle = math.atan2(opposite, adjacent)
        start_x = self.x + self.width
        self.arrow = Arrow(start_x, self.y, self.surf)
        self.arrow.horizontal_speed = self.arrow.speed * math.cos(angle)
        self.arrow.vertical_speed = -self.arrow.speed * math.sin(angle)
        self.runner_moves["Snipe"][1] = self.runner_moves["Snipe"][2]
        self.sound["arrow"].play()
        self.sound["arrow"].set_volume(0.3)

    def do_ability(self, opponent, party):
        if self.selection == 1:
            return Rapidfire()
        if self.selection == 2 and self.ability_cooldowns[1] == 0:
            for character in party:
                party[character].buffs.append("Cover")


class Rapidfire:
    def __init__(self):
        self.attack = 95
        self.luck = 0.4
        self.special_effect = "Pierce"
        self.effect_chance = 0.8
        arrow_img = pygame.image.load("images\\unnamed.png")
        self.image = pygame.transform.scale(arrow_img, (arrow_img.get_width() // 4, arrow_img.get_height() // 4))


class Arrow:

    def __init__(self, start_x, start_y, surf):
        self.x = start_x
        self.y = start_y
        arrow_img = pygame.image.load("images\\unnamed.png")
        self.image = pygame.transform.scale(arrow_img, (arrow_img.get_width() // 10, arrow_img.get_height() // 10))
        self.color = (153, 85, 49)
        self.speed = 700
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.surf = surf
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.width_edge = surf.get_width()
        self.height_edge = surf.get_height()
        self.sound = {"arrow": pygame.mixer.Sound("audio\\arrow_hit.ogg")}

    def update(self, dt, enemies):
        # Movement
        self.x += self.horizontal_speed * dt
        self.y += self.vertical_speed * dt



        # Collision with enemies
        collision_rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        for e in enemies:
            if collision_rect.colliderect(e.rect):
                e.weapon_collision = True
                hit = True
                self.sound["arrow"].play()
                self.sound["arrow"].set_volume(0.3)
                return hit

        # Boundary check
        if self.y + self.height > self.height_edge:
            oob = True  # Out of bounds
        elif self.y  < 0:
            oob = True
        elif self.x < 0:
            oob = True
        elif self.x + self.width > self.width_edge:
            oob = True
        else:
            oob = False
        return oob

    def draw(self):
        self.surf.blit(self.image, (int(self.x), int(self.y)))


class Wizard(Player):

    def __init__(self, start_pos, sprite_sheet, scale, surf):
        super().__init__(start_pos, sprite_sheet, scale, surf)
        self.color = (0, 0, 255)
        self.health = 120
        self.max_health = self.health
        self.attack = 20
        self.defense = 10
        self.luck = 0.1
        self.dodge = 0.06
        self.base_dodge = 0.06
        self.runner_moves = {"Shield": [0, 0, 10]}
        self.shield_surf = pygame.Surface((self.width, self.width))
        self.shield_surf.set_colorkey((0, 0, 0))
        self.shield_surf.set_alpha(150)
        pygame.draw.circle(self.shield_surf, (66, 139, 255), (self.half_width, self.half_width), self.half_width)
        self.abilities = ["Thunderbolt", "Blaze"]
        self.ability_cooldowns = [0, 0, 5, 7]   # First two numbers are current cooldown, second two are corresponding
        self.sound = {"fire": pygame.mixer.Sound("audio\\fire.ogg"),"thunder": pygame.mixer.Sound("audio\\thunder.ogg")}

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
            self.sound["thunder"].play()
            self.sound["thunder"].set_volume(0.3)
            return Thunderbolt()
        if self.selection == 2:
            self.sound["fire"].play()
            self.sound["fire"].set_volume(0.3)
            return Blaze()




class Thunderbolt:
    def __init__(self):
        self.attack = 60
        self.luck = 0.15
        self.special_effect = "Stun"
        self.effect_chance = 0.8
        bolt_img = pygame.image.load("images\\lightning.png")
        self.image = pygame.transform.scale(bolt_img, (100, 100))


class Blaze:
    def __init__(self):
        self.attack = 80
        self.luck = 0.1
        self.special_effect = "Burn"
        self.effect_chance = 0.6
        blaze_img = pygame.image.load("images\\blaze.png")
        self.image = pygame.transform.scale(blaze_img, (100, 100))

