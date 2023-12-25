import pygame
import os
import random
pygame.font.init()


WIDTH, HEIGHT = 600,900
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")

FPS = 100
WHITE = (255,255,255)
BLACK = (0,0,0)

BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets','background1.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE,(600,750))

FLOOR_IMAGE = pygame.image.load(os.path.join('Assets','floor.png'))
FLOOR = pygame.transform.scale(FLOOR_IMAGE,(650,251))

GAME_OVER_IMAGE = pygame.image.load(os.path.join('Assets','gameover4.png'))
GAME_OVER = pygame.transform.scale(GAME_OVER_IMAGE,(750,400)).convert_alpha()
GAME_OVER_RECT = GAME_OVER.get_rect(center = (300,250))

PIPE_IMAGE = pygame.image.load(os.path.join('Assets','pipe1.png'))
PIPE_HEIGHT = [250,400,600]

SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE,1200)

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

BIRDS = [BIRD1,BIRD2,BIRD3]


def draw_window(GROUND_SCROLL,BIRD_SURFACE,BIRD_RECT,PIPES,SCORE):   
    WIN.blit(BACKGROUND,(0,0))
    draw_pipes(PIPES) 
    WIN.blit(FLOOR,(GROUND_SCROLL,749))
    WIN.blit(BIRD_SURFACE,BIRD_RECT)
    draw_score(SCORE)   
       
def pipe_movment (PIPES):
    for pipe in PIPES:
        pipe.x -= 3
    return PIPES
    
def draw_pipes(PIPES):
     for pipe in PIPES:
        if pipe.bottom >= 650 :
            WIN.blit(PIPE_IMAGE,pipe)
        else:
            FLIP_PIPE = pygame.transform.flip(PIPE_IMAGE,False,True)
            WIN.blit(FLIP_PIPE,pipe)

def check_collision(BIRD_RECT,PIPES):
    for pipe in PIPES:
        if BIRD_RECT.colliderect(pipe):
            return False
    if BIRD_RECT.bottom >= 735 :
        return False
    return True

def create_pipe():
    RANDOM_PIPE_POS = random.choice(PIPE_HEIGHT)
    TOP_PIPE = PIPE_IMAGE.get_rect(midbottom = (650,RANDOM_PIPE_POS-220))
    BOTOOM_PIPE = PIPE_IMAGE.get_rect(midtop = (650,RANDOM_PIPE_POS))
    return BOTOOM_PIPE ,TOP_PIPE

def draw_score(SCORE):
    SCORE_FONT = pygame.font.SysFont('comicsans', 50)
    SCORE_SURFACE = SCORE_FONT.render("Score :" + str(SCORE//2), 1 , WHITE)
    SCORE_RECT = SCORE_SURFACE.get_rect(center=(WIDTH // 2, 50))
    WIN.blit(SCORE_SURFACE, SCORE_RECT)

def game_end(HIGH_SCORE):
    GAME_END_FONT = pygame.font.SysFont('freesansbold.ttf', 42)
    GAME_END_SURFACE = GAME_END_FONT.render('TO RESTART THE GAME PRESS "R"', 1 , BLACK)
    GAME_END_RECT = GAME_END_SURFACE.get_rect(center=(WIDTH//2, HEIGHT//2-50))
    WIN.blit(GAME_END_SURFACE, GAME_END_RECT)
    HIGH_SCORE_FONT = pygame.font.SysFont('comicsans', 40)
    HIGH_SCORE_SURFACE = HIGH_SCORE_FONT.render("Best Score is: " + str(HIGH_SCORE), 1 , WHITE)
    HIGH_SCORE_RECT = HIGH_SCORE_SURFACE.get_rect(center=(WIDTH // 2, HEIGHT//2+55))
    WIN.blit(HIGH_SCORE_SURFACE, HIGH_SCORE_RECT)

def start_game():
    START_GAME_FONT = pygame.font.SysFont('freesansbold.ttf', 43)
    START_GAME_SURFACE = START_GAME_FONT.render('TO START THE GAME PRESS "ENTER"', 1 , BLACK)
    START_GAME_RECT = START_GAME_SURFACE.get_rect(center=(WIDTH//2, HEIGHT//2-150))
    WIN.blit(START_GAME_SURFACE, START_GAME_RECT)

def score(BIRD_RECT, PIPES, SCORE):
    BIRD_CENTER_X = BIRD_RECT.centerx
    for pipe in PIPES:
        pipe_center_x = pipe.centerx
        if BIRD_CENTER_X == pipe_center_x:
            SCORE += 1    
    return SCORE

def main():
    
    GROUND_SCROLL = -10
    SCROLL_SPEED = 3

    BIRD_INDEX = 0
    BIRD_SURFACE = BIRDS[BIRD_INDEX]

    FLOOR_RECT = FLOOR.get_rect(topleft = (-10,749))

    BIRD_RECT = BIRD_SURFACE.get_rect(topleft = ((130,400)))

    PIPES = []
    
    GRAVITY = 0.1
    BIRD_MOVEMENT = 0
    BIRD_Y = 400
    JUMP = -13.5

    SCORE = 0
    HIGH_SCORE = 0
    LAST_PASSED_PIPE = False
    STOP_SCORE = False

    clock = pygame.time.Clock()
    run = True
    FLYING = False
    GAME_ACTIVE = True
       
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN and FLYING == False and GAME_ACTIVE:
                    FLYING = True
                    BIRD_MOVEMENT = JUMP
                    BIRD_RECT.topleft = (130,400)
                if event.key == pygame.K_SPACE and GAME_ACTIVE:
                    BIRD_MOVEMENT = JUMP
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
  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    BIRD_MOVEMENT = JUMP
            if event.type == SPAWN_PIPE and GAME_ACTIVE and FLYING:
                PIPES.extend(create_pipe())
            
        GAME_ACTIVE = check_collision(BIRD_RECT,PIPES)
                
        if BIRD_Y >= HEIGHT+66 - FLOOR.get_height():
            BIRD_Y = HEIGHT+66 - FLOOR.get_height()
        if BIRD_Y <= 0:
            BIRD_Y = 0

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

        GROUND_SCROLL -= SCROLL_SPEED
        if abs(GROUND_SCROLL) > 50:
            GROUND_SCROLL = -10

        if FLYING:
            if GAME_ACTIVE:                
                BIRD_MOVEMENT +=0.5             
                BIRD_MOVEMENT += GRAVITY
                BIRD_Y += BIRD_MOVEMENT            
                PIPES = pipe_movment(PIPES)
                SCORE = score(BIRD_RECT, PIPES, SCORE)
                if SCORE > HIGH_SCORE:
                    HIGH_SCORE = SCORE//2
            else:
                WIN.blit(GAME_OVER,GAME_OVER_RECT)
                game_end(HIGH_SCORE)
        else:
            start_game()

        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main() 