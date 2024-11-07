import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Zatura - Defesa da Terra")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

EARTH_POS = (WIDTH // 2, HEIGHT // 2)
PLANET_RADIUS = 30
ORBIT_RADIUS = 200
ship_angle = 0
ship_speed = 0.05
ship_radius = 20
projectiles = []

meteors = []
meteor_speed = 1
meteor_spawn_timer = 2000  
last_meteor_spawn = pygame.time.get_ticks()

score = 0
font = pygame.font.Font(None, 36)
game_active = False

def spawn_meteor():
    angle = random.uniform(0, 2 * math.pi)
    x = EARTH_POS[0] + ORBIT_RADIUS * 1.5 * math.cos(angle)
    y = EARTH_POS[1] + ORBIT_RADIUS * 1.5 * math.sin(angle)
    meteors.append({"pos": [x, y], "angle": angle, "speed": meteor_speed})

def draw_menu():
    screen.fill(BLACK)
    title = font.render("Zatura - Defesa da Terra", True, WHITE)
    instruction = font.render("Pressione ENTER para iniciar", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()

def draw_score():
    score_text = font.render(f"Pontuação: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

clock = pygame.time.Clock()
running = True
while running:
    if not game_active:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    game_active = True
                    score = 0
                    meteors.clear()
                    projectiles.clear()
    else:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    proj_x = EARTH_POS[0] + (ORBIT_RADIUS + ship_radius) * math.cos(ship_angle)
                    proj_y = EARTH_POS[1] + (ORBIT_RADIUS + ship_radius) * math.sin(ship_angle)
                    projectiles.append({"pos": [proj_x, proj_y], "angle": ship_angle, "speed": 5})
                elif event.key == pygame.K_ESCAPE:  
                    game_active = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship_angle -= ship_speed
        if keys[pygame.K_RIGHT]:
            ship_angle += ship_speed

        for projectile in projectiles[:]:
            projectile["pos"][0] += projectile["speed"] * math.cos(projectile["angle"])
            projectile["pos"][1] += projectile["speed"] * math.sin(projectile["angle"])
            if not (0 < projectile["pos"][0] < WIDTH and 0 < projectile["pos"][1] < HEIGHT):
                projectiles.remove(projectile)

        for projectile in projectiles[:]:
            for meteor in meteors[:]:
                dx = projectile["pos"][0] - meteor["pos"][0]
                dy = projectile["pos"][1] - meteor["pos"][1]
                distance = math.sqrt(dx**2 + dy**2)
                if distance < 20:  
                    meteors.remove(meteor)
                    projectiles.remove(projectile)
                    score += 10
                    break

        if pygame.time.get_ticks() - last_meteor_spawn > meteor_spawn_timer:
            spawn_meteor()
            last_meteor_spawn = pygame.time.get_ticks()
            meteor_speed += 0.1  

        for meteor in meteors:
            meteor["pos"][0] -= meteor["speed"] * math.cos(meteor["angle"])
            meteor["pos"][1] -= meteor["speed"] * math.sin(meteor["angle"])
            pygame.draw.circle(screen, RED, (int(meteor["pos"][0]), int(meteor["pos"][1])), 10)

        pygame.draw.circle(screen, BLUE, EARTH_POS, PLANET_RADIUS)

        pygame.draw.circle(screen, BLUE, EARTH_POS, ORBIT_RADIUS, 1)
        ship_x = EARTH_POS[0] + ORBIT_RADIUS * math.cos(ship_angle)
        ship_y = EARTH_POS[1] + ORBIT_RADIUS * math.sin(ship_angle)
        pygame.draw.circle(screen, GREEN, (int(ship_x), int(ship_y)), ship_radius)

        for projectile in projectiles:
            pygame.draw.circle(screen, WHITE, (int(projectile["pos"][0]), int(projectile["pos"][1])), 5)

        draw_score()

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
