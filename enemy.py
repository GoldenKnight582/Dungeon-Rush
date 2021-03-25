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
        self.radius = None
        self.speed = 232
        self.enemy_point = 100

    def update(self, dt, player_x, player_y):
        self.x -= self.speed * dt
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

    def draw(self, surf, scroll_x):
        pygame.draw.circle(surf, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
