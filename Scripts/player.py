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
        self.speed = 100
        self.health = 100
        self.jump_cooldown = 0.33
        self.jump_power = 0
        self.aerial = False
        self.surf = surf

    def update(self, game_state, dt):
        self.jump_cooldown -= dt

        if game_state == "Runner":
            self.x += self.speed * dt
            self.y += self.jump_power * dt
            if self.y < 400:
                self.aerial = True
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
                if self.jump_cooldown <= 0:
                    self.aerial = True
                    self.jump_cooldown = 0.33
                    self.jump_power = -150

    def draw(self):
        pygame.draw.circle(self.surf, (255, 0, 0), (int(self.x), int(self.y)), 20)




