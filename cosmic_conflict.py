import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Conflict")

font = pygame.font.Font(None, 32)

player_image = pygame.image.load("player_spaceship.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (96, 96))  
enemy_image = pygame.image.load("enemy_spaceship.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (76, 56))  
enemy_image = pygame.transform.rotate(enemy_image, 180)  

class Projectile:
    def __init__(self, x, y, direction):
        self.image = pygame.Surface((5, 5))
        self.image.fill((0,255,0) if direction == 1 else (255,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 5 * direction

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.speed > 0:
            self.rect.y -= self.speed 
        else:
            self.rect.y -= self.speed 
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.kill()

    def kill(self):
        if self in player.projectiles:
            player.projectiles.remove(self)

           

class Spaceship:
    def __init__(self):
        self.score = 0
        self.health = 10
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.is_shooting = False
        self.projectiles = []
        self.captured_ship = None
        self.just_fired = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for projectile in self.projectiles:
            projectile.draw(screen)
        if self.captured_ship:
            self.captured_ship.draw(screen)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and not self.is_shooting:
            self.is_shooting = True
            self.fire()
        if not keys[pygame.K_SPACE]:
            self.just_fired = False 
        if self.is_shooting:
            self.fire()
        self.is_shooting = False 

        for projectile in self.projectiles:
            projectile.update()
               
        if self.captured_ship:
            self.captured_ship.update()
            self.captured_ship.rect.centerx = self.rect.centerx + 20
            self.captured_ship.rect.centery = self.rect.centery

    def fire(self):
        if not self.just_fired:
            projectile = Projectile(self.rect.centerx, self.rect.top, 1)
            self.projectiles.append(projectile)
            self.just_fired = True

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            score_text = font.render("Final Score: " + str(self.score), True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.fill((0, 0, 0))
            screen.blit(game_over_text, text_rect)
            screen.blit(score_text, score_rect)
            pygame.display.flip()

            pygame.time.delay(25000)

            pygame.quit()

class EnemySpaceship:
    def __init__(self):
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randrange(1, 2)
        self.can_shoot = random.random() < 2
        self.projectiles = []

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for projectile in self.projectiles:
            projectile.draw(screen)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            player.score -= 1 
            self.kill()
        if self.can_shoot:
            if random.random() < 0.05:
                self.fire()
        for projectile in self.projectiles:
            projectile.update()

    def kill(self):
        global enemy_list
        if self in enemy_list:
            enemy_list.remove(self)

    def fire(self):
        projectile = Projectile(self.rect.centerx, self.rect.bottom, -1)
        self.projectiles.append(projectile)
        projectile.update()

player = Spaceship()
running = True
clock = pygame.time.Clock()

enemy_spawn_rate = 1
enemy_list = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if len(enemy_list) < 5 and random.random() < enemy_spawn_rate:
        enemy_list.append(EnemySpaceship())

    player.update()
    for enemy in enemy_list:
        enemy.update()
    for projectile in player.projectiles[::-1]:
        for enemy in enemy_list:
            if projectile.rect.colliderect(enemy.rect):
                player.projectiles.remove(projectile)
                enemy_list.remove(enemy)
                player.score += 1

    for enemy in enemy_list:
        for projectile in enemy.projectiles:
            if projectile.rect.colliderect(player.rect):
                player.hit()
                enemy.projectiles.remove(projectile)

    screen.fill((0, 0, 0))

    player.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    health_text = font.render("Health: " + str(player.health), True, (255, 255, 255))
    screen.blit(health_text, (10, 10))

    score_text = font.render("Score: " + str(player.score), True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 150, 10))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
