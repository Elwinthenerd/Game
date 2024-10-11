import pygame
import sys

# Initialize Pygame modules
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scrolling Platformer with Multiple Levels")

# Clock to control the frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors (RGB format)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 150, 100)
JUMP_PAD_COLOR = (255, 255, 0)

# Player properties
player_width = 50
player_height = 50
player_speed = 5
jump_speed = 15
jump_pad_boost = 25  # Higher jump for jump pads
gravity = 0.5

# Scroll variables
scroll_x = 0

# Lava zone (entire bottom of the screen)
lava_rect = pygame.Rect(500, HEIGHT - 50, WIDTH * 5, 50)  # Wide lava covering bottom of screen
floor_rect = pygame.Rect(0, HEIGHT - 30, 500, 30)  # Floor at the bottom

# Game states
current_level = 1
game_complete = False
start_time = pygame.time.get_ticks()  # Timer starts once, no reset

# Fade variables
FADE_SPEED = 5
fade_alpha = 0
fading_in = False
fading_out = False

# Function to reset player position and velocity
def reset_player():
    global player_x, player_y, player_vel_x, player_vel_y
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 100  # Adjusted to start above the lava
    player_vel_x = 0
    player_vel_y = 0

# Function to handle fade-in and fade-out animation
def fade_in():
    global fade_alpha, fading_in
    fade_alpha = 255
    fading_in = True

def fade_out():
    global fade_alpha, fading_out
    fade_alpha = 0
    fading_out = True

def apply_fade():
    global fade_alpha, fading_in, fading_out
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(WHITE)
    fade_surface.set_alpha(fade_alpha)
    SCREEN.blit(fade_surface, (0, 0))

    if fading_in:
        fade_alpha -= FADE_SPEED
        if fade_alpha <= 0:
            fading_in = False
            fade_alpha = 0
    elif fading_out:
        fade_alpha += FADE_SPEED
        if fade_alpha >= 255:
            fading_out = False
            fade_alpha = 255
            # Load the new level after the fade-out completes
            load_level(current_level)

# Function to load level-specific platforms, spikes, and portals
def load_level(level):
    global platforms, spikes, triangular_spikes, portal, jump_pads
    reset_player()  # Reset player position when loading a new level
    fade_in()  # Apply fade-in effect on new level

    if level == 1:
        platforms = [
            pygame.Rect(200, HEIGHT - 150, 200, 20),
            pygame.Rect(500, HEIGHT - 300, 200, 20),
            pygame.Rect(800, HEIGHT - 150, 200, 20),
            pygame.Rect(1200, HEIGHT - 200, 200, 20),
            pygame.Rect(1600, HEIGHT - 300, 200, 20),
            pygame.Rect(2000, HEIGHT - 400, 200, 20)
        ]
        triangular_spikes = [
            [(500, HEIGHT - 300), (525, HEIGHT - 350), (550, HEIGHT - 300)],  # On platform 2
            [(1200, HEIGHT - 200), (1225, HEIGHT - 250), (1250, HEIGHT - 200)],  # On platform 4
            [(850, HEIGHT - 550), (875, HEIGHT - 500), (900, HEIGHT - 550)]
        ]
        portal = pygame.Rect(2400, HEIGHT - 70, 50, 50)
        jump_pads = [
            pygame.Rect(250, HEIGHT - 150 - 10, 50, 10),  # On platform 1
            pygame.Rect(850, HEIGHT - 150 - 10, 50, 10)  # On platform 3
        ]

    elif level == 2:
        platforms = [
            pygame.Rect(100, HEIGHT - 100, 150, 20),
            pygame.Rect(400, HEIGHT - 250, 150, 20),
            pygame.Rect(700, HEIGHT - 400, 150, 20),
            pygame.Rect(1000, HEIGHT - 150, 150, 20),
            pygame.Rect(1400, HEIGHT - 300, 150, 20),
            pygame.Rect(1800, HEIGHT - 450, 150, 20)
        ]
        triangular_spikes = [
            [(400, HEIGHT - 250), (425, HEIGHT - 300), (450, HEIGHT - 250)],  # On platform 2
            [(1000, HEIGHT - 150), (1025, HEIGHT - 200), (1050, HEIGHT - 150)]  # On platform 4
        ]
        portal = pygame.Rect(2200, HEIGHT - 70, 50, 50)
        jump_pads = [
            pygame.Rect(150, HEIGHT - 100 - 10, 50, 10),  # On platform 1
            pygame.Rect(750, HEIGHT - 400 - 10, 50, 10),  # On platform 3
            pygame.Rect(1450, HEIGHT - 300 - 10, 50, 10)  # On platform 5
        ]

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
        triangular_spikes = [
            [(300, HEIGHT - 300), (325, HEIGHT - 350), (350, HEIGHT - 300)],  # On platform 2
            [(900, HEIGHT - 150), (925, HEIGHT - 200), (950, HEIGHT - 150)]  # On platform 4
        ]
        portal = pygame.Rect(2400, HEIGHT - 70, 50, 50)
        jump_pads = [
            pygame.Rect(50, HEIGHT - 150 - 10, 50, 10),  # On platform 1
            pygame.Rect(650, HEIGHT - 450 - 10, 50, 10),  # On platform 3
            pygame.Rect(1750, HEIGHT - 300 - 10, 50, 10)  # On platform 6
        ]

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
        triangular_spikes = [
            [(650, HEIGHT - 350), (675, HEIGHT - 400), (700, HEIGHT - 350)],  # On platform 3
            [(1300, HEIGHT - 400), (1325, HEIGHT - 450), (1350, HEIGHT - 400)],  # On platform 5
            [(300, HEIGHT - 200), (325, HEIGHT - 250), (350, HEIGHT - 200)],
            [(350, HEIGHT - 200), (375, HEIGHT - 250), (400, HEIGHT - 200)]
        ]
        portal = pygame.Rect(2300, HEIGHT - 70, 50, 50)
        jump_pads = [
            pygame.Rect(100, HEIGHT - 100 - 10, 50, 10),  # On platform 1
            pygame.Rect(900, HEIGHT - 500 - 10, 50, 10),  # On platform 4
            pygame.Rect(1750, HEIGHT - 300 - 10, 50, 10)  # On platform 6
        ]

    elif level == 5:
        platforms = [
            pygame.Rect(100, HEIGHT - 100, 150, 20),
            pygame.Rect(400, HEIGHT - 250, 150, 20),
            pygame.Rect(700, HEIGHT - 400, 150, 20),
            pygame.Rect(1000, HEIGHT - 150, 150, 20),
            pygame.Rect(1400, HEIGHT - 300, 150, 20),
            pygame.Rect(1800, HEIGHT - 400, 150, 20)
        ]
        triangular_spikes = [
            [(400, HEIGHT - 250), (425, HEIGHT - 300), (450, HEIGHT - 250)],  # On platform 2
            [(700, HEIGHT - 400), (725, HEIGHT - 450), (750, HEIGHT - 400)]  # On platform 3
        ]
        portal = pygame.Rect(2200, HEIGHT - 70, 50, 50)
        jump_pads = [
            pygame.Rect(150, HEIGHT - 100 - 10, 50, 10),  # On platform 1
            pygame.Rect(1050, HEIGHT - 150 - 10, 50, 10),  # On platform 4
            pygame.Rect(1850, HEIGHT - 400 - 10, 50, 10)  # On platform 6
        ]

    # Check for game completion
    if level > 5:
        show_game_complete()

# Function to display game complete message
def show_game_complete():
    global game_complete
    game_complete = True
    SCREEN.fill(WHITE)
    font = pygame.font.SysFont(None, 75)
    text = font.render('Game Complete!', True, BLACK)
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    print("Game Complete! Your time: ", (pygame.time.get_ticks() - start_time) // 1000, "seconds.")
    pygame.time.wait(100000)

# Initial player position and velocity
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 100
player_vel_x = 0
player_vel_y = 0

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

    # Collision with triangular spikes (reset player)
    for tri_spike in triangular_spikes:
        spike_rect = pygame.Rect(min(tri_spike[0][0], tri_spike[2][0]), tri_spike[0][1], 50, 50)
        if player_rect.colliderect(spike_rect):
            reset_player()

    # Collision with lava (reset player)
    if player_rect.colliderect(lava_rect):
        reset_player()

    # Collision with portal (advance to next level)
    if player_rect.colliderect(portal):
        fade_out()  # Start fade-out effect before level transition
        current_level += 1
        if current_level > 5:
            show_game_complete()

    # Collision with jump pads
    for jump_pad in jump_pads:
        if player_rect.colliderect(jump_pad):
            player_vel_y = -jump_pad_boost

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

    # Clear the screen only if not fading out
    if not fading_out:
        SCREEN.fill(WHITE)

        # Draw the lava
        pygame.draw.rect(SCREEN, RED, (lava_rect.x - scroll_x, lava_rect.y, lava_rect.width, lava_rect.height))
        pygame.draw.rect(SCREEN, BLACK, (floor_rect.x - scroll_x, floor_rect.y, floor_rect.width, floor_rect.height))

        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(SCREEN, BLACK, (platform.x - scroll_x, platform.y, platform.width, platform.height))

        # Draw triangular spikes
        for tri_spike in triangular_spikes:
            pygame.draw.polygon(SCREEN, RED, [(x - scroll_x, y) for x, y in tri_spike])

        # Draw jump pads
        for jump_pad in jump_pads:
            pygame.draw.rect(SCREEN, JUMP_PAD_COLOR, (jump_pad.x - scroll_x, jump_pad.y, jump_pad.width, jump_pad.height))

        # Draw the portal
        pygame.draw.rect(SCREEN, GREEN, (portal.x - scroll_x, portal.y, portal.width, portal.height))

        # Draw the player
        pygame.draw.rect(SCREEN, YELLOW, (player_x - scroll_x, player_y, player_width, player_height))

        # Display the timer (no reset between levels)
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Time in seconds
        font = pygame.font.SysFont(None, 36)
        timer_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
        SCREEN.blit(timer_text, (20, 20))

    # Apply fade effect if fading in/out
    apply_fade()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
