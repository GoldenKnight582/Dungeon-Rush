import pygame


class Obstacle:

    def __init__(self, start_pos, scroll_speed):
        self.x = start_pos[0]
        self.y = start_pos[1]
#        self.image = pygame.image.load(image)
#        self.width = self.image.get_width()
#        self.height = self.image.get_height()
#        self.scaled_image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
#        self.width *= scale
#        self.height *= scale
        self.rect = None
        self.speed = scroll_speed
        self.clear_points = 100
        self.weapon_collision = False
        self.sound = {"glass": pygame.mixer.Sound("audio\\glass.ogg")}

    def update(self, dt, player_rect):
        self.x -= self.speed * dt
        self.rect.x = self.x
        self.rect.y = self.y
        # Collision Check
        if self.rect.colliderect(player_rect):
            collision = True
            self.sound["glass"].play()
            self.sound["glass"].set_volume(0.1)
            return collision


class Barricade(Obstacle):
    def __init__(self, start_pos, scroll_speed):
        super().__init__(start_pos, scroll_speed)
        self.wall_img = pygame.image.load("images\\wall.png")
        self.width = self.wall_img.get_width()
        self.height = self.wall_img.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, surf):
        surf.blit(self.wall_img, (int(self.x), int(self.y)))
