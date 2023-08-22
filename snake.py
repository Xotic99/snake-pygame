import pygame
import random
import os

# Initialize pygame
pygame.init()

# Set up the game screen
width, height = 400, 400
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

# Snake position and movement
x, y = 200, 200
delta_x, delta_y = 0, 0

# Food position
food_x, food_y = random.randrange(0, width) // 10 * 10, random.randrange(0, height) // 10 * 10

# Snake body
body_list = [(x, y)]

# Game variables
clock = pygame.time.Clock()
game_over = False
score = 0
high_score = 0
username = ""

# Font for displaying text
font = pygame.font.SysFont("bahnschrift", 25)

# Function to update the high score
def update_high_score():
    global high_score
    if score > high_score:
        high_score = score

# Function to save the high score to a hardware-specific file
def save_high_score():
    folder_name = "Python Snake Game Save"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filename = f"{folder_name}/high_score_{username}_{os.getlogin()}.txt"
    with open(filename, "w") as file:
        file.write(str(high_score))

# Function to load the high score from the hardware-specific file
def load_high_score():
    global high_score
    folder_name = "Python Snake Game Save"
    filename = f"{folder_name}/high_score_{username}_{os.getlogin()}.txt"
    try:
        with open(filename, "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        high_score = 0

# Function to enter the username
def enter_username():
    global username
    game_screen.fill((0, 0, 0))
    username_text = font.render("Enter your username:", True, (255, 255, 255))
    game_screen.blit(username_text, [width // 3, height // 3])
    pygame.display.update()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    return  # Exit the loop and start the game

                if event.unicode.isalnum():  # Only accept alphanumeric characters
                    username += event.unicode

        game_screen.fill((0, 0, 0))
        username_text = font.render("Enter your username:", True, (255, 255, 255))
        input_text = font.render(username, True, (255, 255, 255))
        game_screen.blit(username_text, [width // 3, height // 3])
        game_screen.blit(input_text, [width // 3, height // 2])
        pygame.display.update()

# Function to update the snake position and check for collisions
def update_snake():
    global x, y, food_x, food_y, game_over, score

    # Update snake position
    x = (x + delta_x) % width
    y = (y + delta_y) % height

    # Check for self-collision
    if (x, y) in body_list[1:]:
        game_over = True
        update_high_score()
        save_high_score()
        return

    # Add new segment to the snake body
    body_list.append((x, y))

    # Check if snake has eaten the food
    if food_x == x and food_y == y:
        while (food_x, food_y) in body_list:
            food_x, food_y = (
                random.randrange(0, width) // 10 * 10,
                random.randrange(0, height) // 10 * 10,
            )
        score += 1
    else:
        del body_list[0]

    # Draw the game screen
    game_screen.fill((0, 0, 0))
    pygame.draw.rect(game_screen, (255, 0, 0), [food_x, food_y, 10, 10])
    for (i, j) in body_list:
        pygame.draw.rect(game_screen, (255, 255, 255), [i, j, 10, 10])

    # Display the score and high score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    game_screen.blit(score_text, [10, 10])
    game_screen.blit(high_score_text, [width - high_score_text.get_width() - 10, 10])

    # Update the game screen
    pygame.display.update()

# Function to display the options when the game ends
def display_options():
    options_text = font.render("Press R to restart or Q to quit", True, (255, 255, 255))
    game_screen.blit(options_text, [width // 3, height // 2])
    pygame.display.update()

# Main game loop
def game_loop():
    global delta_x, delta_y, game_over, score

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                update_high_score()
                save_high_score()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and delta_y != 10:
                    delta_x, delta_y = 0, -10
                elif event.key == pygame.K_DOWN and delta_y != -10:
                    delta_x, delta_y = 0, 10
                elif event.key == pygame.K_LEFT and delta_x != 10:
                    delta_x, delta_y = -10, 0
                elif event.key == pygame.K_RIGHT and delta_x != -10:
                    delta_x, delta_y = 10, 0

        update_snake()
        clock.tick(15)

    # Display game over message and options
    game_screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    game_screen.blit(game_over_text, [width // 3, height // 3])
    display_options()

    # Wait for user input to restart or quit
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    game_over = False
                    score = 0
                    body_list.clear()
                    x, y = 200, 200
                    delta_x, delta_y = 0, 0
                    body_list.append((x, y))
                    food_x, food_y = random.randrange(0, width) // 10 * 10, random.randrange(0, height) // 10 * 10
                    game_loop()
                elif event.key == pygame.K_q:
                    # Quit the game
                    pygame.quit()
                    quit()

        pygame.display.update()

    # Display game over message
    game_screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    game_screen.blit(game_over_text, [width // 3, height // 3])
    pygame.display.update()
    pygame.time.wait(2000)

# Start the game
enter_username()
load_high_score()
game_loop()

# Quit the game
pygame.quit()
quit()