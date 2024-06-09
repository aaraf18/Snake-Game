import pygame
import random

# Initialize Pygame
pygame.init()
mixer = pygame.mixer

# Game constants
WIDTH = 800
HEIGHT = 600
FPS = 10
CELL_SIZE = 20

# Music files
background_music_file = 'duggi-8.wav'
food_eaten_sound_file = 'food_eat.wav'  
game_over_sound_file = 'game_over.wav'  

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
green_active = (20, 186, 20)
RED = (255, 0, 0)
red_active = (199, 20, 20)


# Game objects
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font
font_style = pygame.font.SysFont('times new roman', 30)

def play_music(music_file):
    #Plays background music.
    mixer.init()
    mixer.music.load(music_file)
    mixer.music.play(-1, 0.0)

def play_sound(sound_file):
    #Plays a sound effect once.
    sound = mixer.Sound(sound_file)
    sound.play()

def draw_text(text, x, y):
    #Draws text on the screen.
    text_surface = font_style.render(text, True, RED)
    screen.blit(text_surface, (x, y))

def check_collision(x, y, snake_body):
    #Checks for collisions with walls and the snake's own body.
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True

    for segment in snake_body[:-1]:
        if segment[0] == x and segment[1] == y:
            return True

    return False

def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    #Draws a button with text and handles mouse interaction.
    cursor_pos = pygame.mouse.get_pos()
    button_color = active_color if x < cursor_pos[0] < x + width and y < cursor_pos[1] < y + height else inactive_color
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    text_surface = font_style.render(text, True, BLACK)
    text_x = x + (width - text_surface.get_width()) // 2
    text_y = y + (height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))

    if action and pygame.mouse.get_pressed()[0] and x < cursor_pos[0] < x + width and y < cursor_pos[1] < y + height:
        action()

def reset_game():
    #Resets the game state.
    global snake_body, food_x, food_y, score, snake_direction, game_over
    snake_body = [(WIDTH // 2, HEIGHT // 2)]
    food_x, food_y = generate_food()
    score = 0
    snake_direction = "up"
    game_over = False
    play_music(background_music_file)

def close_game():
    #Closes the game.
    pygame.quit()
    quit()

def generate_food():
    #Generates food at a random location at least 10 pixels away from the borders.
    min_offset = 10  # Minimum offset from the screen edges in pixels
    x = random.randint(min_offset // CELL_SIZE, (WIDTH - min_offset) // CELL_SIZE - 1) * CELL_SIZE
    y = random.randint(min_offset // CELL_SIZE, (HEIGHT - min_offset) // CELL_SIZE - 1) * CELL_SIZE
    return x, y

# Load background image
background_image = pygame.image.load("snakebg.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Initialize snake and food
snake_body = [(WIDTH // 2, HEIGHT // 2)]
snake_direction = "up"
food_x, food_y = generate_food()

# Load snake image
snake_image = pygame.image.load("snake_skin.png")
snake_image = pygame.transform.scale(snake_image, (CELL_SIZE, CELL_SIZE))

running = True
game_over = False
score = 0

# Start background music
play_music(background_music_file)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "down":
                snake_direction = "up"
            elif event.key == pygame.K_DOWN and snake_direction != "up":
                snake_direction = "down"
            elif event.key == pygame.K_LEFT and snake_direction != "right":
                snake_direction = "left"
            elif event.key == pygame.K_RIGHT and snake_direction != "left":
                snake_direction = "right"

    if game_over:
        screen.blit(background_image, (0, 0))
        draw_text("Game Over! Score: " + str(score), WIDTH // 3, HEIGHT // 3)
        draw_button("Play Again", WIDTH // 3, HEIGHT // 2, WIDTH // 3, 50, GREEN, green_active, reset_game)
        draw_button("Close", WIDTH // 3, HEIGHT // 2 + 60, WIDTH // 3, 50, RED, red_active, close_game)
        pygame.display.flip()
        continue

    head_x, head_y = snake_body[0]
    if snake_direction == "up":
        head_y -= CELL_SIZE
    elif snake_direction == "down":
        head_y += CELL_SIZE
    elif snake_direction == "left":
        head_x -= CELL_SIZE
    elif snake_direction == "right":
        head_x += CELL_SIZE

    if check_collision(head_x, head_y, snake_body):
        game_over = True
        mixer.music.stop()
        play_sound(game_over_sound_file)
    else:
        snake_body.insert(0, (head_x, head_y))
        if head_x == food_x and head_y == food_y:
            score += 1
            food_x, food_y = generate_food()
            play_sound(food_eaten_sound_file)
        else:
            snake_body.pop()

    screen.blit(background_image, (0, 0))
    for segment in snake_body:
        screen.blit(snake_image, (segment[0], segment[1]))

    pygame.draw.rect(screen, RED, (food_x, food_y, CELL_SIZE, CELL_SIZE))
    draw_text("Score: " + str(score), 10, 10)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()