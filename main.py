import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

shield_angle = 90 # variable for angle in degreees, 0, 90, 180, 270
center_radius = 20
shield_length = 40 
shield_offset = center_radius + shield_length / 2 + 4  # offset from center point
center_x = WIDTH // 2
center_y = HEIGHT // 2 # These 2 variables divide the screen in half to reach the center point

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #rotate shield with X / C keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                shield_angle = (shield_angle - 90) % 360
            if event.key == pygame.K_x:
                shield_angle = (shield_angle + 90) % 360
    
    screen.fill((0, 0, 0)) # RGB black background

    # draw shield as a line
    dir = pygame.Vector2(1, 0).rotate(shield_angle)  # direction the shield is facing
    shield_center = pygame.Vector2(center_x, center_y) + dir * shield_offset  # move out from center

    # perpendicular to dir, so the line has thickness horizontally across that direction
    perp = dir.rotate(90) * (shield_length / 2)

    start_pos = shield_center - perp
    end_pos = shield_center + perp

    pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 6)
    pygame.draw.circle(screen, (200, 200, 200), (center_x, center_y), center_radius)

    pygame.display.flip()

pygame.quit()
