import pygame
import math  # not used yet, but fine to keep for later
from scripts.rain import create_rain_layers

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Umbrella Game")

center_x = WIDTH // 2
center_y = HEIGHT // 2
player_x = center_x
player_y = center_y

# rain config
RAIN_LAYERS = [
    {"count": 120, "speed": 3, "color": (120, 120, 180, 40)},   # back, faint
    {"count": 30, "speed": 5, "color": (160, 160, 220, 80)},  # mid
    {"count": 20, "speed": 7, "color": (200, 200, 255, 255)},  # front, solid
]

# Separate surface with per-pixel alpha for rain
rain_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Build rain layers from config
rain_layers = create_rain_layers(RAIN_LAYERS, WIDTH, HEIGHT)

clock = pygame.time.Clock()
running = True

PLAYER_SIZE = 50
PLAYER_SPEED = 5

while running:
    dt = clock.tick(60) / 1000.0  # seconds per frame (if you need it later)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_c]:
        player_x += PLAYER_SPEED

    # boundaries
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - PLAYER_SIZE:
        player_x = WIDTH - PLAYER_SIZE

    # update rain
    for layer in rain_layers:
        for drop in layer:
            drop.update()

    screen.fill((10, 10, 20))  # background

    # clear rain surface | fully transparent
    rain_surface.fill((0, 0, 0, 0))

    # draw all rain onto rain_surface
    for layer in rain_layers:
        for drop in layer:
            drop.draw(rain_surface)

    # blit rain to main screen
    screen.blit(rain_surface, (0, 0))

    # draw player square on top
    pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
    pygame.draw.rect(screen, (100, 100, 100), (0, HEIGHT // 1.33, WIDTH, HEIGHT)) # ground

    pygame.display.flip()

pygame.quit()