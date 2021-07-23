import pygame, sys, time, random

#initial game variables

# Window size
frame_size_x = 720
frame_size_y = 480                                 

#Parameters for Snake
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
direction = 'RIGHT'
change_to = direction

#Parameters for food

food_pos = [360,240]
food_spawn = False

score = 0


# Initialise game window
pygame.init()
pygame.display.set_caption('Snake Eater')
screen=pygame.display.set_mode((frame_size_x,frame_size_y))

status=True

# FPS (frames per second) controller to set the speed of the game
fps_controller = pygame.time.Clock()




def check_for_events():
    """
    This should contain the main for loop (listening for events). You should close the program when
    someone closes the window, update the direction attribute after input from users. You will have to make sure
    snake cannot reverse the direction i.e. if it turned left it cannot move right next.
    """
    global change_to

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
               change_to="RIGHT"
            if event.key==pygame.K_LEFT:
               change_to="LEFT"   
            if event.key==pygame.K_UP:
               change_to="UP"
            if event.key==pygame.K_DOWN:
               change_to="DOWN"        


def show_score(pos, color, font, size,screen,score):
    """
    It takes in the above arguements and shows the score at the given pos according to the color, font and size.
    """
  

    test_font=pygame.font.Font(font,size)
    score_img=test_font.render("Score: "+ str(score),True,color)
    score_img_rect=score_img.get_rect()
    score_img_rect.x=pos[0]
    score_img_rect.y=pos[1]
    screen.blit(score_img,score_img_rect)


def game_over(score,frame_size_x,frame_size_y,screen):
    """ 
    Write the function to call in the end. 
    It should write game over on the screen, show your score, wait for 3 seconds and then exit
    """
    game_over_img=pygame.font.Font(None,48).render("GAME OVER", True, (255,0,0))
    game_over_img_rect=game_over_img.get_rect()
    game_over_img_rect.centerx=frame_size_x/2
    game_over_img_rect.centery=frame_size_y/2
    score_img=pygame.font.Font(None,30).render("Score: "+str(score), True, (255,0,0))
    score_img_rect=score_img.get_rect()
    score_img_rect.centerx=frame_size_x/2
    score_img_rect.bottom=400

    screen.blit(game_over_img,game_over_img_rect)
    screen.blit(score_img,score_img_rect)
    pygame.display.update()
    time.sleep(3)
    sys.exit(0)


def update_snake(change_to,food_pos,frame_size_x,frame_size_y):
    """
     This should contain the code for snake to move, grow, detect walls etc.
     """
    # Code for making the snake head move in the expected direction
    global direction, snake_pos,snake_body, food_spawn, score, status
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10    


    '''inserting the new snake head position in the snake body list in the first position and if eats food the list will increase or we will remove the last 
     item from the list'''

    snake_body.insert(0,list(snake_pos))
    if snake_pos!=food_pos:
        snake_body.pop()
    else:
        food_spawn=True
        score+=1


    # Make the snake's body respond after the head moves. The responses will be different if it eats the food.
    # Note you cannot directly use the functions for detecting collisions 
    # since we have not made snake and food as a specific sprite or surface.
    
    if snake_pos[0]<0 or snake_pos[0]>frame_size_x or snake_pos[1]<0 or snake_pos[1]>frame_size_y:
        status=False
    for body_pos in snake_body[1:]:
        if snake_pos==body_pos:
            status=False




    # End the game if the snake collides with the wall or with itself.            #complete the parameters required
    

def create_food(frame_size_x,frame_size_y):
    """ 
    This function should set coordinates of food if not there on the screen. You can use randrange() to generate
    the location of the food.
    """
    global food_spawn,food_pos
    if food_spawn:
        food_pos=[random.randrange(0,frame_size_x,10),random.randrange(0,frame_size_y,10)]
        food_spawn=False            # food creation

    


def update_screen(screen,food_pos,snake_body,score,frame_size_x,frame_size_y,status):
    """
    Draw the snake, food, background, score on the screen
    """
    if status:
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(*food_pos,10,10))      #drawing the apples on screen
        
        for body_pos in snake_body:
            pygame.draw.rect(screen,(0,255,0),pygame.Rect(*body_pos,10,10))    #drawing the body of snake


        show_score([40,60],(255,255,255),None,20,screen,score)   #Mention pos,color,font,size !!!!!!!!!!!!!!!!!!!!!!!!

    else:
        screen.fill((0,0,0))
        game_over(score,frame_size_x,frame_size_y,screen)



# Main loop
while True:
    # Make appropriate calls to the above functions so that the game could finally run
    
    screen.fill((0,0,0))
    check_for_events()
    update_snake(change_to,food_pos,frame_size_x,frame_size_y)
    create_food(frame_size_x,frame_size_y)               
    
    update_screen(screen,food_pos,snake_body,score,frame_size_x,frame_size_y,status)
    
    pygame.display.update()
    

    # To set the speed of the screen
    fps_controller.tick(15)
