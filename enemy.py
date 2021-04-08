import pygame


class Enemy:

    def __init__(self, start_pos, state, scroll_speed):
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
        #self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.rect = None
        self.speed = scroll_speed
        self.enemy_point = 100
        self.weapon_collision = False
        self.special_effect = None
        self.debuffs = []
        self.defense = 0
        self.stunned = ["False", 0]
        self.burned = ["False", 0]
        self.pierced = ["False", 0]

    def update(self, dt, player_rect, state):
        if state == "Runner":
            self.x -= self.speed * dt
            self.rect.x = self.x
            self.rect.y = self.y
            collision = False
            # Collision Check
            if self.rect.colliderect(player_rect):
                return collision
        elif state == "Combat":
            # Add / Remove Debuffs
            if "Stun" in self.debuffs and self.stunned[0] == "False":
                self.stunned[0] = "True"
                self.stunned[1] = 3
            if self.stunned[1] == 0 and self.stunned[0] == "True":
                self.debuffs.remove("Stun")
                self.stunned[0] = "False"
            if "Burn" in self.debuffs and self.burned[0] == "False":
                self.burned[0] = "True"
                self.burned[1] = 2
            if self.burned[1] == 0 and self.burned[0] == "True":
                self.debuffs.remove("Burn")
                self.burned[0] = "False"
            if "Pierce" in self.debuffs and self.pierced[0] == "False":
                self.pierced[0] = "True"
                self.defense /= 2
                self.pierced[1] = 2
            if self.pierced[1] == 0 and self.pierced[0] == "True":
                self.debuffs.remove("Pierce")
                self.defense *= 2
                self.pierced[0] = "False"


class BasicEnemy(Enemy):

    def __init__(self, start_pos, state, scroll_speed):
        super().__init__(start_pos, state, scroll_speed)
        self.health = 100
        self.radius = 20
        self.attack = 30
        self.defense = 10
        self.luck = 0.02
        self.dodge = 0.02

    def draw(self, surf):
        pygame.draw.circle(surf, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
        # Debug Collision
#        pygame.draw.rect(surf, (255, 255, 0), self.rect, 1)

    def draw_portrait(self, surf):
        pygame.draw.circle(surf, (255, 0, 0), (720, 200), self.radius // 2)


class SecondEnemy(Enemy):

    def __init__(self, start_pos, state, scroll_speed):
        super().__init__(start_pos, state, scroll_speed)
        self.health = 60
        self.radius = 10
        self.attack = 20
        self.defense = 5
        self.luck = 0.02
        self.dodge = 0.02
        self.wolf_img = pygame.image.load("images\\wolf.png")
        self.wolf_img_flip = pygame.transform.flip(self.wolf_img, True, False)
        self.rect = pygame.Rect(int(self.x + 25),int(self.y - self.wolf_img_flip.get_height() / 2), int(self.wolf_img_flip.get_width() - 25) ,int(self.wolf_img_flip.get_height()) - 25)





    def draw(self, surf):
        surf.blit(self.wolf_img_flip, (int(self.x), (int(self.y - 80))))
        pygame.draw.rect(surf, (255,0,0), self.rect, 1)
        # Debug Collision
#        pygame.draw.rect(surf, (255, 255, 0), self.rect, 1)

    def draw_portrait(self, surf):
        pygame.draw.circle(surf, (100, 100, 0), (720, 200), self.radius // 2)


class BasicBoss(Enemy):
    def __init__(self, start_pos, state, scroll_speed):
        super().__init__(start_pos, state, scroll_speed)
        self.health = 315
        self.radius = 50
        self.attack = 70
        self.defense = 30
        self.luck = 0
        self.dodge = 0

    def draw(self, surf):
        pygame.draw.circle(surf, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
