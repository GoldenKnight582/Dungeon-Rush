import pygame


class Obstacle:

    def __init__(self, start_pos, scroll_speed):
        self.x = start_pos[0]
        self.y = start_pos[1]
#        self.image = pygame.image.load(image)
#        self.width = self.image.get_width()
#        self.height = self.image.get_height()
        self.width = 0
        self.height = 0
#        self.scaled_image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
#        self.width *= scale
#        self.height *= scale
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = scroll_speed
        self.clear_points = 100
        self.weapon_collision = False

    def update(self, dt, player_rect):
        self.x -= self.speed * dt
        self.rect.x = self.x
        self.rect.y = self.y
        # Collision Check
        if self.rect.colliderect(player_rect):
            collision = True
            return collision


class Barricade(Obstacle):
    def __init__(self, start_pos, scroll_speed):
        super().__init__(start_pos, scroll_speed)
        self.width = 30
        self.height = 150
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, surf):
        pygame.draw.rect(surf, (255, 0, 0), self.rect)
