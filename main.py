import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Umbrella Rain")

center_x = WIDTH // 2
center_y = HEIGHT // 2
player_x = center_x
player_y = center_y

# --- RAIN CONFIG ---
RAIN_LAYERS = [
    # (count, speed, color RGBA)
    {"count": 80, "speed": 3, "color": (120, 120, 180, 70)},   # back, faint
    {"count": 60, "speed": 5, "color": (160, 160, 220, 120)},  # mid
    {"count": 40, "speed": 7, "color": (200, 200, 255, 255)},  # front, solid
]

# Separate surface so we can use per-pixel alpha for rain
rain_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


class Raindrop:
    def __init__(self, layer_cfg):
        self.layer_cfg = layer_cfg
        self.reset(random_y=True)

    def reset(self, random_y=False):
        self.x = random.randint(0, WIDTH)
        if random_y:
            self.y = random.randint(-HEIGHT, 0)
        else:
            self.y = random.randint(-40, -10)

        self.length = random.randint(12, 30)
        base_speed = self.layer_cfg["speed"]
        self.speed = base_speed * random.uniform(0.7, 1.3)
        self.color = self.layer_cfg["color"]

    def update(self):
        self.y += self.speed
        if self.y - self.length > HEIGHT:
            self.reset(random_y=False)

    def draw(self, surface):
        # Undertale-ish: thin vertical streaks
        pygame.draw.line(
            surface,
            self.color,
            (self.x, self.y),
            (self.x, self.y + self.length),
            2
        )


# Create rain layers
rain_layers = []
for layer_cfg in RAIN_LAYERS:
    drops = [Raindrop(layer_cfg) for _ in range(layer_cfg["count"])]
    rain_layers.append(drops)

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60) / 1000.0  # not used yet, but handy later

    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- INPUT (HELD KEYS) ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        player_x -= 5
    if keys[pygame.K_x]:
        player_x += 5

    # Optional: keep player on screen
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - 50:
        player_x = WIDTH - 50

    # --- UPDATE RAIN ---
    for layer in rain_layers:
        for drop in layer:
            drop.update()

    # --- DRAW ---
    screen.fill((10, 10, 20))  # dark night sky

    # Clear rain surface (transparent)
    rain_surface.fill((0, 0, 0, 0))

    # Draw all rain onto rain_surface
    for layer in rain_layers:
        for drop in layer:
            drop.draw(rain_surface)

    # Blit rain onto main screen
    screen.blit(rain_surface, (0, 0))

    # Draw player square on top
    pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, 50, 50))

    pygame.display.flip()

pygame.quit()