import pygame


class Enemy:

    def __init__(self, start_pos, state):
        self.x = start_pos[0]
        self.y = start_pos[1]
#        self.image = pygame.image.load(image)
#        self.width = self.image.get_width()
#        self.height = self.image.get_height()
#        self.scaled_image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
#        self.width *= scale
#        self.height *= scale
        self.game_state = state
        self.radius = 20
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.speed = 202
        self.enemy_point = 100
        self.weapon_collision = False

    def update(self, dt, player_x, player_y):
        self.x -= self.speed * dt
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        collision = False
        # Collision Check
        if ((self.x - player_x) ** 2 + (self.y - player_y) ** 2) ** 0.5 <= self.radius + 20:
            collision = True
        return collision


class BasicEnemyTypeTest(Enemy):

    def __init__(self, start_pos, state):
        super().__init__(start_pos, state)
        self.health = 100
        self.radius = 20
        self.attack = 30
        self.defense = 10
        self.luck = 0.02

    def draw(self, surf):
        pygame.draw.circle(surf, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
        # Debug Collision
#        pygame.draw.rect(surf, (255, 255, 0), self.rect, 1)

    def draw_portrait(self, surf):
        pygame.draw.circle(surf, (255, 0, 0), (720, 200), self.radius / 2)
