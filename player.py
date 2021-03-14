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
        self.speed = 100
        self.jump_cooldown = 0.33
        self.jump_power = 0
        self.aerial = False
        self.surf = surf
        self.selection = None
        self.selection_made = False

    def update(self, game_state, dt):
        self.jump_cooldown -= dt

        if game_state == "Runner":
            self.x += self.speed * dt
            self.y += self.jump_power * dt
            if self.y < 400:
                self.aerial = True
            else:
                self.aerial = False
            if self.aerial:
                self.jump_power += 200 * dt
            if self.jump_power > 100:
                self.jump_power = 100

        if self.y >= 400:
            if self.aerial:
                self.jump_power = 0
            self.y = 400

    def handle_running_input(self, evt):
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_SPACE:
                if self.jump_cooldown <= 0 and not self.aerial:
                    self.aerial = True
                    self.jump_cooldown = 0.33
                    self.jump_power = -150

    def handle_combat_input(self, evt, menu):
        if self.selection == None:
            if menu == "Main":
                self.selection = 1
            if menu == "Swapping":
                if self.__class__.__name__ == "Warrior":
                    self.selection = 2
                if self.__class__.__name__ == "Archer" or self.__class__.__name__ == "Wizard":
                    self.selection = 1
            self.selection_made = False
        if evt.type == pygame.KEYDOWN:
            if not self.selection_made:
                if evt.key == pygame.K_UP:
                    self.selection -= 1
                    if menu == "Main":
                        if self.selection < 1:
                            self.selection = 3
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
                if evt.key == pygame.K_DOWN:
                    self.selection += 1
                    if menu == "Main":
                        if self.selection > 3:
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
                if menu == "Swapping":
                    self.selection = 0
                    self.selection_made = True

    def draw(self):
        pygame.draw.circle(self.surf, (0, 255, 0), (int(self.x), int(self.y)), self.radius)


class Warrior(Player):

    def __init__(self, start_pos, image, scale, surf):
        super().__init__(start_pos, image, scale, surf)
        self.health = 250
        self.attack = 60
        self.defense = 40
        self.luck = 0.05


class Archer(Player):

    def __init__(self, start_pos, image, scale, surf):
        super().__init__(start_pos, image, scale, surf)
        self.health = 180
        self.attack = 45
        self.defense = 20
        self.luck = 0.08

    def draw(self):
        pygame.draw.circle(self.surf, (255, 255, 0), (int(self.x), int(self.y)), self.radius)


class Wizard(Player):

    def __init__(self, start_pos, image, scale, surf):
        super().__init__(start_pos, image, scale, surf)
        self.health = 120
        self.attack = 20
        self.defense = 10
        self.luck = 0.1

    def draw(self):
        pygame.draw.circle(self.surf, (0, 0, 255), (int(self.x), int(self.y)), self.radius)




