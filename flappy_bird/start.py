import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface,(floor_x_cor,900))
    screen.blit(floor_surface,(floor_x_cor+576,900))

def create_pipe():
    rand_height = random.choice(pipe_heights)
    new_bottom__pipe = pipe_surface.get_rect(midtop = (650,rand_height))
    new_top_pipe = pipe_surface.get_rect(midtop = (650,rand_height - 900 ))
    return new_bottom__pipe,new_top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    new_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return new_pipes

def remove_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx < -600:
            pipes.remove(pipe)

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            pipe_flipped = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(pipe_flipped, pipe) 

def check_collision(pipes):
    
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    
    if bird_rect.top <= -100 or bird_rect.bottom >=900:
        return False
    
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return new_bird

def flap_animation():
     new_bird = bird_frames[bird_index]
     new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery)) 
     return new_bird,new_bird_rect       
         
def display_score(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score : {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score : {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
        
        high_score_surface = game_font.render(f'High Score : {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,high_score_rect)

def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def update_score():
    global score, score_flag
    if pipe_list:
        for pipe in pipe_list:
            if pipe.centerx < 105 and pipe.centerx > 95 and score_flag:
                score += 1  
                score_sound.play()
                score_flag = False
            if pipe.centerx < 20:
                score_flag = True 

pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)


#Game Variables

#Game_acitve
game_active = True

#movemint variables
gravity = 0.25
bird_movement = 0
score = 0
high_score = 0 
score_flag = True

#Background variables
bg_image = pygame.image.load('assets/background-day.png').convert()
bg_image = pygame.transform.scale2x(bg_image)


#Floor surface variables
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_cor = 0


#Bird variables
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())

#put bird frames in an array
bird_frames = [bird_upflap,bird_midflap,bird_downflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))
#Define birdflap event. set timer
BIRDFLAP = pygame.USEREVENT +1
pygame.time.set_timer(BIRDFLAP, 250)

#pipe variables
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1500)
pipe_heights = [400,600,800]
#game loop

#GAME OVER SCREEN
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())

#SOUNDS
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

SCOREVENT = pygame.USEREVENT +2
pygame.time.set_timer(SCOREVENT,100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = -8
                flap_sound.play()
          
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                score = 0
                
                #restart game
                bird_rect.center = (100,512)
                pipe_list.clear()
                bird_movement = 0
                
        
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = flap_animation()
            
        
                    
            
            
            
    screen.blit(bg_image,(0,0))
    
    if game_active == True:
        bird_movement += gravity 
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_surface)
        
        screen.blit(rotated_bird,bird_rect)
        #collisons
        if check_collision(pipe_list) == False:
             death_sound.play()
        game_active = check_collision(pipe_list)
        
        
        #SCORE
        update_score()
        display_score('main_game')
        high_score = update_high_score(score,high_score)
        
        #pipes
        pipe_list = move_pipes(pipe_list)
        remove_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        #score += 0.01
        
        
    if game_active == False:
        display_score('game_over')
        game_over_rect = game_over_surface.get_rect(center = (288,512))
        screen.blit(game_over_surface,game_over_rect)
        pipe_list.clear()
          
    
    
    
    floor_x_cor += -1
    draw_floor()
    if floor_x_cor < -576:
        floor_x_cor = 0
             
            
    pygame.display.update()
    clock.tick(60)