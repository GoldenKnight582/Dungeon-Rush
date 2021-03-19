import pygame


class Player:
    def __init__(self, start_pos, image, scale, surf):
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
        self.speed = 9
        self.surf = surf
        self.rect = pygame.draw.circle(self.surf, (0, 255, 0), (int(self.x), int(self.y)), self.radius)
        self.selection = None
        self.selection_made = False
        self.abilities = []
        self.fortify_on = False
        self.fortify_track = None
        self.fortify_turn = None
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

    def move_and_collide(self, tiles):
        collision_types = {"bottom": False, "right": False}
#        collisions = self.collision_test(tiles)
#        for tile in collisions:
#            if tile.top <= self.rect.top:
#                self.rect.right = tile.left
#                self.x = self.rect.right - self.radius
#                collision_types["right"] = True
        self.y += self.jump_power
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

    def update(self, game_state, tiles, dt, cur_turn, party):
        if game_state == "Runner":
            self.jump_power += 1.5
            if self.jump_power > 15:
                self.jump_power = 15

            collisions = self.move_and_collide(tiles)
            if collisions["bottom"]:
                self.jump_power = 0.25

        if game_state == "Combat":
            # Fortify Check
            if self.fortify_on:
                if self.fortify_track == None:
                    self.fortify_turn = cur_turn - 1
                    # - 1 because this code executes a frame AFTER the ability is activated
                    self.fortify_track = 0
                if cur_turn != self.fortify_turn and cur_turn % 2 == 1:
                    self.fortify_track = (cur_turn - self.fortify_turn) // 2
                if self.fortify_track == 3:
                    self.fortify_turn = 0
                    self.fortify_track = 0
                    self.fortify_on = False
                    for character in party:
                        party[character].defense -= 20

    def handle_running_input(self, evt):
        cur_class = self.__class__.__name__
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_SPACE:
                self.jump_power = -20
            elif evt.key == pygame.K_q:
                if self.__class__.__name__ == "Warrior":
                    cur_class = "Wizard"
                elif self.__class__.__name__ == "Archer":
                    cur_class = "Warrior"
                else:
                    cur_class = "Archer"
            elif evt.key == pygame.K_e:
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
                if evt.key == pygame.K_s:
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
                if evt.key == pygame.K_RETURN:
                    self.selection_made = True
            if evt.key == pygame.K_BACKSPACE:
                if menu == "Swapping" or menu == "Abilities":
                    self.selection = 0
                    self.selection_made = True

    def draw(self):
        pygame.draw.circle(self.surf, (0, 255, 0), (int(self.x), int(self.y)), self.radius)
        # Collision rect for debug
#        pygame.draw.rect(self.surf, (255, 0, 0), self.rect, 1)


class Warrior(Player):

    def __init__(self, start_pos, image, scale, surf):
        super().__init__(start_pos, image, scale, surf)
        self.health = 250
        self.attack = 60
        self.defense = 40
        self.luck = 0.05
        self.abilities = ["Fortify", "Overwhelm"]

    def do_ability(self, opponent, party):
        if self.selection == 1:
            for character in party:
                party[character].fortify_on = True
                party[character].defense += 20

    def update(self, game_state, tiles, dt, cur_turn, party):
        super().update(game_state, tiles, dt, cur_turn, party)



class Archer(Player):

    def __init__(self, start_pos, image, scale, surf):
        super().__init__(start_pos, image, scale, surf)
        self.health = 180
        self.attack = 45
        self.defense = 20
        self.luck = 0.08
        self.abilities = ["Rapidfire", "Take Cover"]

    def draw(self):
        pygame.draw.circle(self.surf, (255, 255, 0), (int(self.x), int(self.y)), self.radius)


class Wizard(Player):

    def __init__(self, start_pos, image, scale, surf):
        super().__init__(start_pos, image, scale, surf)
        self.health = 120
        self.attack = 20
        self.defense = 10
        self.luck = 0.1
        self.abilities = ["Thunderbolt", "Blaze"]

    def draw(self):
        pygame.draw.circle(self.surf, (0, 0, 255), (int(self.x), int(self.y)), self.radius)




