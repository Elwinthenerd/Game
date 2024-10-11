import pygame
import sys

# Initialize Pygame modules
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scrolling Platformer with Lava and Multiple Levels")

# Clock to control the frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors (RGB format)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 150, 100)

# Player properties
player_width = 50
player_height = 50
player_speed = 5
jump_speed = 15
gravity = 0.4

# Scroll variables
scroll_x = 0

# Lava zone (entire bottom of the screen)
lava_rect = pygame.Rect(500, HEIGHT - 50, WIDTH * 5, 50)  # Wide lava covering bottom of screen
floor_rect = pygame.Rect(0, HEIGHT - 30, 500, 30)  # Floor at the bottom

# Game states
current_level = 5
game_complete = False

# Function to reset player position and velocity
def reset_player():
    global player_x, player_y, player_vel_x, player_vel_y
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 100  # Adjusted to start above the lava
    player_vel_x = 0
    player_vel_y = 0

# Function to load level-specific platforms, spikes, and portals
def load_level(level):
    global platforms, spikes, portal
    reset_player()  # Reset player position when loading a new level

    if level == 1:
        platforms = [
            pygame.Rect(200, HEIGHT - 150, 200, 20),
            pygame.Rect(500, HEIGHT - 300, 200, 20),
            pygame.Rect(800, HEIGHT - 450, 200, 20),
            pygame.Rect(1200, HEIGHT - 200, 200, 20),
            pygame.Rect(1600, HEIGHT - 300, 200, 20),
            pygame.Rect(2000, HEIGHT - 400, 200, 20)
        ]
        spikes = [
            pygame.Rect(600, HEIGHT - 320, 50, 20),
            pygame.Rect(1700, HEIGHT - 320, 50, 20)
        ]
        portal = pygame.Rect(2400, HEIGHT - 70, 50, 50)

    elif level == 2:
        platforms = [
            pygame.Rect(100, HEIGHT - 100, 150, 20),
            pygame.Rect(400, HEIGHT - 250, 150, 20),
            pygame.Rect(700, HEIGHT - 400, 150, 20),
            pygame.Rect(1000, HEIGHT - 150, 150, 20),
            pygame.Rect(1400, HEIGHT - 300, 150, 20),
            pygame.Rect(1800, HEIGHT - 450, 150, 20)
        ]
        spikes = [
            pygame.Rect(400, HEIGHT - 270, 50, 20),
            pygame.Rect(800, HEIGHT - 420, 50, 20),
            pygame.Rect(1500, HEIGHT - 320, 50, 20)
        ]
        portal = pygame.Rect(2200, HEIGHT - 70, 50, 50)

    elif level == 3:
        platforms = [
            pygame.Rect(50, HEIGHT - 150, 100, 20),
            pygame.Rect(300, HEIGHT - 300, 100, 20),
            pygame.Rect(600, HEIGHT - 450, 100, 20),
            pygame.Rect(900, HEIGHT - 150, 100, 20),
            pygame.Rect(1300, HEIGHT - 200, 100, 20),
            pygame.Rect(1700, HEIGHT - 300, 100, 20),
            pygame.Rect(2100, HEIGHT - 450, 100, 20)
        ]
        spikes = [
            pygame.Rect(325, HEIGHT - 320, 50, 20),
            pygame.Rect(675, HEIGHT - 470, 50, 20),
            pygame.Rect(1500, HEIGHT - 220, 50, 20),
        ]
        portal = pygame.Rect(2400, HEIGHT - 70, 50, 50)

    elif level == 4:
        platforms = [
            pygame.Rect(50, HEIGHT - 100, 100, 20),
            pygame.Rect(300, HEIGHT - 200, 100, 20),
            pygame.Rect(600, HEIGHT - 350, 100, 20),
            pygame.Rect(900, HEIGHT - 500, 100, 20),
            pygame.Rect(1300, HEIGHT - 400, 100, 20),
            pygame.Rect(1700, HEIGHT - 300, 100, 20),
            pygame.Rect(2100, HEIGHT - 150, 100, 20)
        ]
        spikes = [
            pygame.Rect(625, HEIGHT - 370, 50, 20),
            pygame.Rect(850, HEIGHT - 520, 50, 20),
            pygame.Rect(1600, HEIGHT - 320, 50, 20)
        ]
        portal = pygame.Rect(2300, HEIGHT - 70, 50, 50)

    elif level == 5:
        platforms = [
            pygame.Rect(100, HEIGHT - 100, 150, 20),
            pygame.Rect(400, HEIGHT - 250, 150, 20),
            pygame.Rect(700, HEIGHT - 400, 150, 20),
            pygame.Rect(1000, HEIGHT - 150, 150, 20),
            pygame.Rect(1400, HEIGHT - 300, 150, 20),
            pygame.Rect(1800, HEIGHT - 400, 150, 20)
        ]
        spikes = [
            pygame.Rect(200, HEIGHT - 120, 50, 20),
            pygame.Rect(1025, HEIGHT - 170, 50, 20),
            pygame.Rect(1700, HEIGHT - 320, 50, 20)
        ]
        portal = pygame.Rect(2200, HEIGHT - 70, 50, 50)

# Function to show "Game Complete" screen
def show_game_complete():
    global game_complete
    game_complete = True
    SCREEN.fill(WHITE)
    font = pygame.font.SysFont(None, 75)
    text = font.render('Game Complete!', True, BLACK)
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(100000)

# Load the first level
load_level(current_level)

# Main game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_complete:
        continue  # Stop game logic when the game is complete

    # Apply gravity
    player_vel_y += gravity
    player_x += player_vel_x
    player_y += player_vel_y

    on_ground_or_platform = False

    # Collision detection with lava
    if player_y + player_height >= HEIGHT - lava_rect.height + 19:
        player_y = HEIGHT - lava_rect.height - player_height + 19  # Position above lava
        player_vel_y = 0
        on_ground_or_platform = True

    # Collision detection with platforms
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for platform in platforms:
        if player_rect.colliderect(platform):
            if player_vel_y >= 0:  # Falling
                player_y = platform.y - player_height
                player_vel_y = 0
                on_ground_or_platform = True

    # Collision with spikes (reset player)
    for spike in spikes:
        if player_rect.colliderect(spike):
            reset_player()

    # Collision with lava (reset player)
    if player_rect.colliderect(lava_rect):
        reset_player()

    # Collision with portal (advance to next level)
    if player_rect.colliderect(portal):
        current_level += 1
        if current_level > 5:
            show_game_complete()
        else:
            load_level(current_level)

    # Key states for player input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_vel_x = -player_speed
    elif keys[pygame.K_RIGHT]:
        player_vel_x = player_speed
    else:
        player_vel_x = 0

    if keys[pygame.K_SPACE]:
        if on_ground_or_platform:
            player_vel_y = -jump_speed

    # Scrolling effect
    if player_x > WIDTH / 2:
        scroll_x = player_x - WIDTH / 2
    else:
        scroll_x = 0

    # Clear the screen
    SCREEN.fill(WHITE)

    # Draw the lava
    pygame.draw.rect(SCREEN, RED, (lava_rect.x - scroll_x, lava_rect.y, lava_rect.width, lava_rect.height))
    pygame.draw.rect(SCREEN, BLACK, (floor_rect.x - scroll_x, floor_rect.y, floor_rect.width, floor_rect.height))

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(SCREEN, BLACK, (platform.x - scroll_x, platform.y, platform.width, platform.height))

    # Draw spikes
    for spike in spikes:
        pygame.draw.rect(SCREEN, RED, (spike.x - scroll_x, spike.y, spike.width, spike.height))

    # Draw the portal
    pygame.draw.rect(SCREEN, GREEN, (portal.x - scroll_x, portal.y, portal.width, portal.height))

    # Draw the player
    pygame.draw.rect(SCREEN, YELLOW, (player_x - scroll_x, player_y, player_width, player_height))

    # Update the display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
sys.exit()
