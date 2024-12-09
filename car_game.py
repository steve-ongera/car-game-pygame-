import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game")

# Clock to control game frame rate
clock = pygame.time.Clock()

# Load assets
car_width = 50
car_height = 100
car_image = pygame.image.load("car_icon.png")
car_image = pygame.transform.scale(car_image, (car_width, car_height))

opponent_width = 50
opponent_height = 100
opponent_image = pygame.image.load("car_icon.png")
opponent_image = pygame.transform.scale(opponent_image, (opponent_width, opponent_height))

# Fonts
font = pygame.font.SysFont(None, 35)

def draw_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

def game_loop():
    # Car position
    car_x = SCREEN_WIDTH // 4 - car_width // 2  # Start in the leftmost lane
    car_y = SCREEN_HEIGHT - car_height - 20
    target_x = car_x

    # Opponent cars
    opponents = []
    for _ in range(3):
        lane_x = random.choice([
            SCREEN_WIDTH // 4 - car_width // 2,
            SCREEN_WIDTH // 2 - car_width // 2,
            3 * SCREEN_WIDTH // 4 - car_width // 2
        ])
        opponents.append([lane_x, random.randint(-600, -100)])

    # Speed
    car_speed = 5
    lateral_speed = 5
    opponent_speed = 5  # Start speed of opponents

    # Score
    score = 0

    # Game state
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and target_x > 0:
            target_x -= 5  # Fine control for left movement
        if keys[pygame.K_RIGHT] and target_x < SCREEN_WIDTH - car_width:
            target_x += 5  # Fine control for right movement
        if keys[pygame.K_UP] and car_y > 0:
            car_y -= car_speed
        if keys[pygame.K_DOWN] and car_y < SCREEN_HEIGHT - car_height:
            car_y += car_speed

        # Smooth lateral movement
        if car_x < target_x:
            car_x += lateral_speed
            if car_x > target_x:
                car_x = target_x
        elif car_x > target_x:
            car_x -= lateral_speed
            if car_x < target_x:
                car_x = target_x

        # Update opponents
        for opponent in opponents:
            opponent[1] += opponent_speed
            if opponent[1] > SCREEN_HEIGHT:
                opponent[1] = random.randint(-600, -100)
                opponent[0] = random.choice([
                    SCREEN_WIDTH // 4 - car_width // 2,
                    SCREEN_WIDTH // 2 - car_width // 2,
                    3 * SCREEN_WIDTH // 4 - car_width // 2
                ])
                score += 1

        # Increase opponent speed based on score
        opponent_speed = 5 + (score // 10)  # Speed increases every 10 points

        # Check collision
        for opponent in opponents:
            if (
                car_x < opponent[0] + opponent_width
                and car_x + car_width > opponent[0]
                and car_y < opponent[1] + opponent_height
                and car_y + car_height > opponent[1]
            ):
                draw_text("Game Over!", RED, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
                pygame.display.update()
                pygame.time.wait(2000)

                # Restart or quit
                running = False
                return main_menu()

        # Drawing everything
        screen.fill(GRAY)

        # Draw lanes
        for i in range(1, 4):
            pygame.draw.line(screen, WHITE, (i * SCREEN_WIDTH // 4 - SCREEN_WIDTH // 8, 0), (i * SCREEN_WIDTH // 4 - SCREEN_WIDTH // 8, SCREEN_HEIGHT), 5)

        # Draw cars
        screen.blit(car_image, (car_x, car_y))
        for opponent in opponents:
            screen.blit(opponent_image, (opponent[0], opponent[1]))

        # Draw score
        draw_text(f"Score: {score}", BLACK, 10, 10)

        pygame.display.update()
        clock.tick(60)

def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        draw_text("Car Game", BLACK, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3)
        draw_text("Press ENTER to Start", GREEN, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
        draw_text("Press ESC to Quit", RED, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    menu_running = False

    pygame.quit()

# Run the game
main_menu()
