import pygame
import os
import random

# Initialize fonts for pygame
pygame.font.init()

# Window dimensions
WIDTH, HEIGHT = 600,900

# Set up the main window
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Frames per second
FPS = 100

# Colors (in RGB format)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Load background image and scale it
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets','background1.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE,(600,750))

# Load floor image and scale it
FLOOR_IMAGE = pygame.image.load(os.path.join('Assets','floor.png'))
FLOOR = pygame.transform.scale(FLOOR_IMAGE,(650,251))

# Load game over image, scale it, and get its rect for positioning
GAME_OVER_IMAGE = pygame.image.load(os.path.join('Assets','gameover4.png'))
GAME_OVER = pygame.transform.scale(GAME_OVER_IMAGE,(750,400)).convert_alpha()
GAME_OVER_RECT = GAME_OVER.get_rect(center = (300,250))

# Load pipe image, define possible heights for pipe placement
PIPE_IMAGE = pygame.image.load(os.path.join('Assets','pipe1.png'))
PIPE_HEIGHT = [250,400,600]

# Create a custom event for spawning pipes periodically
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE,1200)# Spawn a pipe every 1.2 seconds

# Load bird images (three variations) and create rotated versions for up/down tilt
BIRD1_IMAGE = pygame.image.load(os.path.join('Assets','bird1.png'))
BIRD1 = pygame.transform.scale(BIRD1_IMAGE,(45,35))
BIRD1_UP = pygame.transform.rotate(pygame.transform.scale(BIRD1_IMAGE,(45,35)),45)
BIRD1_DOWN = pygame.transform.rotate(pygame.transform.scale(BIRD1_IMAGE,(45,35)),-45)

BIRD2_IMAGE = pygame.image.load(os.path.join('Assets','bird2.png'))
BIRD2 = pygame.transform.scale(BIRD2_IMAGE,(45,35))
BIRD2_UP = pygame.transform.rotate(pygame.transform.scale(BIRD2_IMAGE,(45,35)),45)
BIRD2_DOWN = pygame.transform.rotate(pygame.transform.scale(BIRD2_IMAGE,(45,35)),-45)


BIRD3_IMAGE = pygame.image.load(os.path.join('Assets','bird3.png'))
BIRD3 = pygame.transform.scale(BIRD3_IMAGE,(45,35))
BIRD3_UP = pygame.transform.rotate(pygame.transform.scale(BIRD3_IMAGE,(45,35)),45)
BIRD3_DOWN = pygame.transform.rotate(pygame.transform.scale(BIRD3_IMAGE,(45,35)),-45)

# Store all bird images in a list for animation
BIRDS = [BIRD1,BIRD2,BIRD3]

"""
Draws the main game elements on the screen: background, pipes, floor, bird, and score.
"""
def draw_window(GROUND_SCROLL,BIRD_SURFACE,BIRD_RECT,PIPES,SCORE): 
   # Draw the background
    WIN.blit(BACKGROUND,(0,0))

    # Draw the pipes
    draw_pipes(PIPES) 

    # Draw the floor based on current scroll position
    WIN.blit(FLOOR,(GROUND_SCROLL,749))

    # Draw the bird
    WIN.blit(BIRD_SURFACE,BIRD_RECT)

    # Draw the score
    draw_score(SCORE)   

"""
Moves each pipe to the left by a fixed amount. Returns the updated list of pipe rects.
"""
def pipe_movment (PIPES):
    for pipe in PIPES:
        pipe.x -= 3 # Move pipe left
    return PIPES


"""
Draws each pipe in the PIPES list. Pipes above the screen are flipped vertically.
"""
def draw_pipes(PIPES):
     # If the pipe's bottom is below a certain point, draw the pipe normally
     for pipe in PIPES:
        if pipe.bottom >= 650 :
            WIN.blit(PIPE_IMAGE,pipe)
        else:
            # Otherwise flip the pipe to simulate the upper pipe
            FLIP_PIPE = pygame.transform.flip(PIPE_IMAGE,False,True)
            WIN.blit(FLIP_PIPE,pipe)

"""
Checks for collision between the bird and any pipe, or if the bird hits the ground.
Returns False if a collision occurs, otherwise True.
"""
def check_collision(BIRD_RECT,PIPES):
    # Check collision with pipes
    for pipe in PIPES:
        if BIRD_RECT.colliderect(pipe):
            return False

    # Check if the bird hits the floor
    if BIRD_RECT.bottom >= 735 :
        return False
    return True


"""
Creates and returns two new pipe rects (bottom and top).
Randomly selects a vertical position from PIPE_HEIGHT for variation.
"""
def create_pipe():
    RANDOM_PIPE_POS = random.choice(PIPE_HEIGHT)
    # Top pipe is placed slightly above the chosen position
    TOP_PIPE = PIPE_IMAGE.get_rect(midbottom = (650,RANDOM_PIPE_POS-220))
    # Bottom pipe is placed starting at the chosen position
    BOTOOM_PIPE = PIPE_IMAGE.get_rect(midtop = (650,RANDOM_PIPE_POS))
    return BOTOOM_PIPE ,TOP_PIPE

"""
Draws the current score at the top center of the screen.
Note: Score is divided by 2 for display to slow down scoring speed.
"""
def draw_score(SCORE):
    SCORE_FONT = pygame.font.SysFont('comicsans', 50)
    SCORE_SURFACE = SCORE_FONT.render("Score :" + str(SCORE//2), 1 , WHITE)
    SCORE_RECT = SCORE_SURFACE.get_rect(center=(WIDTH // 2, 50))
    WIN.blit(SCORE_SURFACE, SCORE_RECT)


"""
Displays the 'Game Over' instructions and the highest recorded score.
"""
def game_end(HIGH_SCORE):
    GAME_END_FONT = pygame.font.SysFont('freesansbold.ttf', 42)
    GAME_END_SURFACE = GAME_END_FONT.render('TO RESTART THE GAME PRESS "R"', 1 , BLACK)
    GAME_END_RECT = GAME_END_SURFACE.get_rect(center=(WIDTH//2, HEIGHT//2-50))
    WIN.blit(GAME_END_SURFACE, GAME_END_RECT)
    HIGH_SCORE_FONT = pygame.font.SysFont('comicsans', 40)
    HIGH_SCORE_SURFACE = HIGH_SCORE_FONT.render("Best Score is: " + str(HIGH_SCORE), 1 , WHITE)
    HIGH_SCORE_RECT = HIGH_SCORE_SURFACE.get_rect(center=(WIDTH // 2, HEIGHT//2+55))
    WIN.blit(HIGH_SCORE_SURFACE, HIGH_SCORE_RECT)


"""
Draws instructions on how to start the game.
"""
def start_game():
    START_GAME_FONT = pygame.font.SysFont('freesansbold.ttf', 43)
    START_GAME_SURFACE = START_GAME_FONT.render('TO START THE GAME PRESS "ENTER"', 1 , BLACK)
    START_GAME_RECT = START_GAME_SURFACE.get_rect(center=(WIDTH//2, HEIGHT//2-150))
    WIN.blit(START_GAME_SURFACE, START_GAME_RECT)


"""
Increments the score when the bird's x-position matches the center of a pipe.
Returns the updated score.
"""
def score(BIRD_RECT, PIPES, SCORE):
    BIRD_CENTER_X = BIRD_RECT.centerx
    for pipe in PIPES:
        pipe_center_x = pipe.centerx
        if BIRD_CENTER_X == pipe_center_x:
            SCORE += 1    
    return SCORE


"""
Main function that runs the game loop. Handles events, updates game state,
and draws each frame.
"""
def main():
    # Initial floor scroll position
    GROUND_SCROLL = -10
    SCROLL_SPEED = 3

    # Bird animation index and initial bird surface
    BIRD_INDEX = 0
    BIRD_SURFACE = BIRDS[BIRD_INDEX]

    # Get the floor rect for collision/reference
    FLOOR_RECT = FLOOR.get_rect(topleft = (-10,749))

    # Bird rect to handle position and collision
    BIRD_RECT = BIRD_SURFACE.get_rect(topleft = ((130,400)))

    # List to hold pipe rects on screen
    PIPES = []

    # Physics-related variables
    GRAVITY = 0.1
    BIRD_MOVEMENT = 0
    BIRD_Y = 400
    JUMP = -13.5  # Upward speed when player jumps

    # Score tracking
    SCORE = 0
    HIGH_SCORE = 0

    # Some flags to control state
    LAST_PASSED_PIPE = False
    STOP_SCORE = False

    clock = pygame.time.Clock()
    run = True
    FLYING = False # Whether the bird has started flying
    GAME_ACTIVE = True # Whether the game is currently active (not game over)
       
    while run:
        # Control the loop speed
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # Exit the game
                
            # Keypress events    
            if event.type == pygame.KEYDOWN: 
                # Start the game on ENTER if not already flying
                if event.key == pygame.K_RETURN and FLYING == False and GAME_ACTIVE:
                    FLYING = True
                    BIRD_MOVEMENT = JUMP
                    BIRD_RECT.topleft = (130,400)

                # Bird flaps on SPACE
                if event.key == pygame.K_SPACE and GAME_ACTIVE:
                    BIRD_MOVEMENT = JUMP

                # Restart game on 'R' after game over
                if event.key == pygame.K_r and GAME_ACTIVE == False:
                    BIRD_Y = 400  
                    BIRD_MOVEMENT = 0
                    PIPES.clear()
                    SCORE = 0
                    GAME_ACTIVE = True
                    FLYING = False
                    BIRD_RECT.topleft = (130, BIRD_Y)
                    WIN.blit(BACKGROUND, (0, 0))
                    draw_score(SCORE)

            # Mouse click also makes the bird flap
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    BIRD_MOVEMENT = JUMP

            # Spawn pipe event
            if event.type == SPAWN_PIPE and GAME_ACTIVE and FLYING:
                PIPES.extend(create_pipe())
                
        # Check collision for the current frame     
        GAME_ACTIVE = check_collision(BIRD_RECT,PIPES)

        # Prevent the bird from going off-screen below the floor
        if BIRD_Y >= HEIGHT+66 - FLOOR.get_height():
            BIRD_Y = HEIGHT+66 - FLOOR.get_height()

        # Prevent the bird from going off-screen above the top
        if BIRD_Y <= 0:
            BIRD_Y = 0

        # Bird animation cycle
        if BIRD_INDEX <len(BIRDS)-0.1:
            BIRD_INDEX +=0.1
            BIRD_SURFACE = BIRDS[int(BIRD_INDEX)] 
            BIRD_RECT.y = BIRD_Y
            draw_window(GROUND_SCROLL,BIRD_SURFACE,BIRD_RECT,PIPES,SCORE)
        else:
            BIRD_INDEX = 0
            BIRD_SURFACE = BIRDS[int(BIRD_INDEX)]
            BIRD_RECT.y = BIRD_Y
            draw_window(GROUND_SCROLL,BIRD_SURFACE,BIRD_RECT,PIPES,SCORE)

        # Move the floor background for a scrolling effect
        GROUND_SCROLL -= SCROLL_SPEED
        if abs(GROUND_SCROLL) > 50:
            GROUND_SCROLL = -10

        # If the bird has taken flight
        if FLYING:
            # If the game is still active (no collisions)
            if GAME_ACTIVE:   
                # Apply gravity and movement
                BIRD_MOVEMENT +=0.5             
                BIRD_MOVEMENT += GRAVITY
                BIRD_Y += BIRD_MOVEMENT 

                # Move pipes to the left
                PIPES = pipe_movment(PIPES)
                
                # Update the score if the bird passes through pipes
                SCORE = score(BIRD_RECT, PIPES, SCORE)

                # Update high score if current score surpasses it
                if SCORE > HIGH_SCORE:
                    HIGH_SCORE = SCORE//2
            else:
                # If the game is not active, display the Game Over assets
                WIN.blit(GAME_OVER,GAME_OVER_RECT)
                game_end(HIGH_SCORE)
        else:
            # If not flying, display the "start game" message
            start_game()

        pygame.display.update()
        
    pygame.quit()
    
# Run the game if this file is executed directly
if __name__ == "__main__":
    main() 
