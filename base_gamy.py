
import pygame
import random

# Start Pygame
pygame.init()

# Set up the window
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Stars")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 40)

# Colours
BACKGROUND = (20, 25, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 50)
GREEN = (80, 200, 120)
RED = (255, 0, 0)

# Player
player = pygame.Rect(270, 350, 60, 20)
player_speed = 8

# Star
star = pygame.Rect(
    random.randint(0, WIDTH - 20), 0, 20, 20
)
star_speed = 3

# bomb
bomb = pygame.Rect(
    random.randint(0, WIDTH - 20), 0, 20, 20
)
bomb_speed = 3

# Score and lives
score = 0
misses = 0

running = True

while running:
    if misses >= 3:
        screen.fill(BACKGROUND)
        game_over_text = font.render(
            "Game Over! Press R to Restart", True, WHITE
        )
        screen.blit(
            game_over_text,
            (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 20),
        )
        pygame.display.flip()

        # Wait for the player to restart the game
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_restart = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    # Reset the game state
                    score = 0
                    misses = 0
                    star.x = random.randint(0, WIDTH - star.width)
                    star.y = 0
                    star_speed = 3
                    bomb.x = random.randint(0, WIDTH - bomb.width)
                    bomb.y = 0
                    bomb_speed = 1
                    waiting_for_restart = False

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read keyboard input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= player_speed

    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # Keep the player inside the window
    player.x = max(0, min(player.x, WIDTH - player.width))

    # Move the star & bomb down the screen
    star.y += star_speed
    bomb.y += bomb_speed

    # Check if the player catches the star
    if player.colliderect(star):
        score += 1
        star.x = random.randint(0, WIDTH - star.width)
        star.y = 0
        star_speed += 1

    if player.colliderect(bomb):
        misses += 1
        bomb.x = random.randint(0, WIDTH - bomb.width)
        bomb.y = 0

    # Check if the star reaches the bottom
    if star.y > HEIGHT:
        misses += 1
        star.x = random.randint(0, WIDTH - star.width)
        star.y = 0

    if bomb.y > HEIGHT:
        bomb.x = random.randint(0, WIDTH - bomb.width)
        bomb.y = 0
    # Draw everything
    screen.fill(BACKGROUND)

    pygame.draw.rect(screen, GREEN, player)
    pygame.draw.ellipse(screen, YELLOW, star)
    pygame.draw.ellipse(screen, RED, bomb)

    score_text = font.render(
        f"Score: {score}", True, WHITE
    )
    misses_text = font.render(
        f"Misses: {misses}/3", True, WHITE
    )

    screen.blit(score_text, (10, 10))
    screen.blit(misses_text, (WIDTH - 150, 10))

    pygame.display.flip()

    # Limit the game to 60 frames per second
    clock.tick(60)

pygame.quit()
