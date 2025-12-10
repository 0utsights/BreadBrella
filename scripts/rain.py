import pygame
import random

class Raindrop:
    def __init__(self, layer_cfg, width, height):
        self.width = width
        self.height = height
        self.layer_cfg = layer_cfg
        self.reset(random_y=True)

    def reset(self, random_y=False):
        self.x = random.randint(0, self.width)
        if random_y:
            # spawn somewhere above the top, possibly far up | for initial scatter
            self.y = random.randint(-self.height, 0)
        else:
            # respawn just above the top edge
            self.y = random.randint(-40, -10)

        self.length = random.randint(12, 30)
        base_speed = self.layer_cfg["speed"]
        self.speed = base_speed * random.uniform(0.7, 1.3)
        self.color = self.layer_cfg["color"]

    def update(self):
        self.y += self.speed
        if self.y - self.length > self.height:
            self.reset(random_y=False)

    def draw(self, surface):
        pygame.draw.line(
            surface,
            self.color,
            (self.x, self.y),
            (self.x, self.y + self.length),
            2
        )


def create_rain_layers(RAIN_LAYERS, width, height):
    rain_layers = []
    for layer_cfg in RAIN_LAYERS:
        drops = [
            Raindrop(layer_cfg, width, height)
            for _ in range(layer_cfg["count"])
        ]
        rain_layers.append(drops)
    return rain_layers
