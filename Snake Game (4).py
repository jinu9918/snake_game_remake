"""
Snake Eater
Made with PyGame
"""

from math import fabs
import pygame, sys, time, random

obstacle_pos=[]
is_true=True
# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
#화면 크기를 지정하는 전역변수 선언
frame_size_x = 720
frame_size_y = 480
block_size=[0,710,0,470]

# Checks for errors encountered
check_errors = pygame.init()#pygame 모듈 사용을 위해 초기화
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors

if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')#게임 초기화 중 실패
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')#게임 초기화 성공


# Initialise game window
#display 타이틀바의 이름 설정
pygame.display.set_caption('Snake Eater')
#[frame_size_x, frame_size_y]크기의 display 생성
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
#게임에서 사용되는 color 전역변수 선언
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()#해당 변수를 통해 FPS 즉 화면을 초당 몇 번 출력하는가를 설정할 수 있다.


# Game variables
#snake 생성
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

#snake가 먹을 food(점수)를 display내 random으로 생성
food_pos = [random.randrange(30, (frame_size_x-30)//10) * 10, random.randrange(30, (frame_size_y-30)//10)*10]
food_spawn = True

direction = 'RIGHT'
change_to = direction
score = 0 
sboard=[0,0,0,0,0]
def difficultyC():
    pygame.init()
    global difficulty
    dif_window = pygame.display.set_mode((frame_size_x, frame_size_y))
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(260, 400, 100, 32)
    #clock = pygame.time.Clock()
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                        done = True


        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        dif_window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        
        pygame.draw.rect(dif_window, color, input_box, 2)
        pygame.display.flip()
        #clock.tick(30)
        df_font=pygame.font.SysFont('times',15)
        df_surface1=df_font.render('Choose the difficulty level to play.',True, white)
        df_surface2=df_font.render('(1)Easy',True,white)
        df_surface3=df_font.render('(2)Medium',True,white)
        df_surface4=df_font.render('(3)Hard',True,white)
        df_surface5=df_font.render('(4)Harder',True,white)
        df_surface6=df_font.render('(5)Impossible',True,white)
        df_rect1=df_surface1.get_rect()
        df_rect1.midtop=(frame_size_x/2, frame_size_y/10*2)
        df_rect2=df_surface2.get_rect()
        df_rect2.midtop=(frame_size_x/2, frame_size_y/10*3)
        df_rect3=df_surface3.get_rect()
        df_rect3.midtop=(frame_size_x/2, frame_size_y/10*4)
        df_rect4=df_surface4.get_rect()
        df_rect4.midtop=(frame_size_x/2, frame_size_y/10*5)
        df_rect5=df_surface5.get_rect()
        df_rect5.midtop=(frame_size_x/2, frame_size_y/10*6)
        df_rect6=df_surface5.get_rect()
        df_rect6.midtop=(frame_size_x/2, frame_size_y/10*7)
        dif_window.fill(black)
        dif_window.blit(df_surface1, df_rect1)
        dif_window.blit(df_surface2, df_rect2)
        dif_window.blit(df_surface3, df_rect3)
        dif_window.blit(df_surface4, df_rect4)
        dif_window.blit(df_surface5, df_rect5)
        dif_window.blit(df_surface6, df_rect6)
        #pygame.display.flip()

    if text == '1':
        difficulty=10
    if text == '2':
        difficulty=25
    if text == '3':
        difficulty=40
    if text == '4':
        difficulty=60
    if text == '5':
        difficulty=120

def show_scoreboard():
    board_window = pygame.display.set_mode((frame_size_x, frame_size_y))
    board_font = pygame.font.SysFont('consolas',20)
    board_surface1 = board_font.render('top 5 record ',True ,white)
    board_surface2 = board_font.render('1st '+str(sboard[0]),True ,white)
    board_surface3 = board_font.render('2nd '+str(sboard[1]),True ,white)
    board_surface4 = board_font.render('3rd '+str(sboard[2]),True ,white)
    board_surface5 = board_font.render('4th '+str(sboard[3]),True ,white)
    board_surface6 = board_font.render('5th '+str(sboard[4]),True ,white)
    board_rect1=board_surface1.get_rect()
    board_rect1.topleft=(0,0)
    board_rect2=board_surface2.get_rect()
    board_rect2.topleft=(0,25)
    board_rect3=board_surface3.get_rect()
    board_rect3.topleft=(0,50)
    board_rect4=board_surface4.get_rect()
    board_rect4.topleft=(0,75)
    board_rect5=board_surface5.get_rect()
    board_rect5.topleft=(0,100)
    board_rect6=board_surface6.get_rect()
    board_rect6.topleft=(0,125)
    board_window.fill(black)
    board_window.blit(board_surface1, board_rect1)
    board_window.blit(board_surface2, board_rect2)
    board_window.blit(board_surface3, board_rect3)
    board_window.blit(board_surface4, board_rect4)
    board_window.blit(board_surface5, board_rect5)
    board_window.blit(board_surface6, board_rect6)
    pygame.display.flip()

# Game Over
def game_over():
    global score
    my_font = pygame.font.SysFont('times new roman', 90)#You died 문구를 보여줄 font와 size를 my_font 객체에 저장
    game_over_surface = my_font.render('YOU DIED', True, red)#red색으로 antialias 기법 true, 'YOU DIED'문구 출력
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)#game over screen의 midtop 좌표를 [frame_size_x/2, frame_size_y/4]로 설정
    game_window.fill(black)#game_over 화면을 Colors에서 설정한 black값으로 채움
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    game_font = pygame.font.SysFont('times new roman',20)
    reset_surface = game_font.render('Reset Game: Press r key',True,white)
    reset_rect = reset_surface.get_rect()
    reset_rect.midleft = (frame_size_x/3, frame_size_y/2)
    quit_surface = game_font.render('Quit Game: Press q key or ESC', True, white)
    quit_rect = quit_surface.get_rect()
    quit_rect.midleft = (frame_size_x/3, (frame_size_y/2 + 20))
    board_surface =game_font.render('ScoreBoard : Preess b key',True, white)
    board_rect = reset_surface.get_rect()
    board_rect.midleft = (frame_size_x/3, frame_size_y/2+40)
    game_window.blit(reset_surface, reset_rect)
    game_window.blit(quit_surface, quit_rect)
    game_window.blit(board_surface, board_rect)
    for i in range(5):
        if(score>sboard[i]):
            sboard.insert(i,score)
            break
    sboard.sort(reverse=True)
    pygame.display.flip()#지금까지 화면에 작성한 모든 행위 업데이트
    time.sleep(3)#game over 후 3초간 프로세스 일시정지
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == event.key == ord('q'):
                    print("the game is over")
                    pygame.quit()#게임 종료
                    sys.exit()#sys모듈 프로그램 종료
                if event.key == event.key == ord('b'):
                    print("scoreboard")
                    show_scoreboard()
                if event.key == event.key == ord('r'):
                    print("reset")
                    pygame.init()
                    return 


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)#점수를 보여줄 문자를 입력받은 font와 size를 통해 객체를 생성 후 저장
    score_surface = score_font.render('Score : ' + str(score), True, color)#저장한 score_font 객체를 render 메소드를 통해 함수를 실행하는 screen
                                                                           #에 그린다. score_font는 입력받은 color값을 통해 색이 정해지고 True는
                                                                           #antialias(선을 부드럽게 하는 그래픽 기법)값으로 False라면 선이 투박해진다.
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)#game over 내의 score 좌표를 [frame_size_x/2, frame_size_y/1.25]로 설정
    game_window.blit(score_surface, score_rect)
    #pygame.display.flip()

# Main logic
# difficulty=getLevel()
# fps_controller.tick(difficulty)

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_start_screen():
    # game splash/start screen
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('Snake Game', True, green)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

show_start_screen()    
wait_for_key()
while True:
    
    difficultyC()
    obstacle_pos=[]
    block_size=[0,710,0,470]
    is_true=True
    # Window size
    #화면 크기를 지정하는 전역변수 선언

    frame_size_x = 720
    frame_size_y = 480

    # Checks for errors encountered
    check_errors = pygame.init()#pygame 모듈 사용을 위해 초기화
    # pygame.init() example output -> (6, 0)
    # second number in tuple gives number of errors

    if check_errors[1] > 0:
        print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')#게임 초기화 중 실패
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')#게임 초기화 성공


    # Initialise game window
    #display 타이틀바의 이름 설정
    pygame.display.set_caption('Snake Eater')
    #[frame_size_x, frame_size_y]크기의 display 생성
    game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


    # Colors (R, G, B)
    #게임에서 사용되는 color 전역변수 선언
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)


    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()#해당 변수를 통해 FPS 즉 화면을 초당 몇 번 출력하는가를 설정할 수 있다.


    # Game variables
    #snake 생성
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

    #snake가 먹을 food(점수)를 display내 random으로 생성
    food_pos = [random.randrange(30, (frame_size_x-30)//10) * 10, random.randrange(30, (frame_size_y-30)//10)*10]
    food_spawn = True

    deadfood_pos = [random.randrange(30, (frame_size_x-30)//10) * 10, random.randrange(30, (frame_size_y-30)//10)*10]
    deadfood_spawn =True

    direction = 'RIGHT'
    change_to = direction

    #score 0으로 초기화
    score = 0 
    
    loopbreak=True
    while(True):
        for event in pygame.event.get():
            #윈도우 닫기 버튼 클릭시 프로그램 종료
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:#키가 눌려졌다 떼어진다면 발생
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):#방향기 위, 혹은 w키를 눌렀다면 change_to 변수를 UP으로 변경
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):#방향기 아래, 혹은 s키를 눌렀다면 change_to 변수를 DOWN으로 변경
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):#방향기 왼쪽, 혹은 a키를 눌렀다면 change_to 변수를 LEFT으로 변경
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):#방향기 오른쪽, 혹은 d키를 눌렀다면 change_to 변수를 RIGHT으로 변경
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                #Esc키를 누를시 대기열에 게임 종료하는 이벤트 배치
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
        


        # Making sure the snake cannot move in the opposite direction instantaneously
        #snake가 본인 스스로에게 부딪쳐도 gameover 되기에 바로 반대 방향으로 전환하는 것을 막는다.
        if change_to == 'UP' and direction != 'DOWN':#change_to변수가 UP이고 direction 변수가 DOWN이 아니라면 direction변수를 UP으로 변경
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':#change_to변수가 DOWN이고 direction 변수가 UP이 아니라면 direction변수를 DOWN으로 변경
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':#change_to변수가 LEFT이고 direction 변수가 RIGHT이 아니라면 direction변수를 LEFT으로 변경
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':#change_to변수가 RIGHT이고 direction 변수가 LEFT이 아니라면 direction변수를 RIGHT으로 변경
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            #snake 좌표와 food 좌표가 겹치게 된다면 score를 1점 올린다.
            score += 1
            food_spawn = False
            deadfood_spawn=False
            if score %  5 == 0:
                is_true=True
        else:
            #아닐경우 snake_bady의 마지막 요소를 지우며 앞으로 나가는 것을 표현한다.
            snake_body.pop()

        if score >= 5 and score < 10 and is_true:
            is_true=False
            block_size[0]+=10
            block_size[1]-=10
            block_size[2]+=10
            block_size[3]-=10
            for i in range(0,480,10):
                line1=[]
                line1.append(0)
                line1.append(i)
                obstacle_pos.append(line1)

            for i in range(0,720,10):
                line2=[]
                line2.append(i)
                line2.append(470)
                obstacle_pos.append(line2)

            for i in range(0,480,10):
                line3=[]
                line3.append(710)
                line3.append(i)
                obstacle_pos.append(line3)

            for i in range(0,720,10):
                line4=[]
                line4.append(i)
                line4.append(0)
                obstacle_pos.append(line4)
            
        if score >= 10 and score <15 and is_true:
            is_true=False
            block_size[0]+=10
            block_size[1]-=10
            block_size[2]+=10
            block_size[3]-=10
            for i in range(10,470,10):
                line1=[]
                line1.append(10)
                line1.append(i)
                obstacle_pos.append(line1)

            for i in range(10,710,10):
                line2=[]
                line2.append(i)
                line2.append(460)
                obstacle_pos.append(line2)

            for i in range(10,470,10):
                line3=[]
                line3.append(700)
                line3.append(i)
                obstacle_pos.append(line3)

            for i in range(10,710,10):
                line4=[]
                line4.append(i)
                line4.append(10)
                obstacle_pos.append(line4)

        if score >= 15 and is_true:
            is_true=False
            block_size[0]+=10
            block_size[1]-=10
            block_size[2]+=10
            block_size[3]-=10
            for i in range(20,460,10):
                line1=[]
                line1.append(20)
                line1.append(i)
                obstacle_pos.append(line1)

            for i in range(20,700,10):
                line2=[]
                line2.append(i)
                line2.append(450)
                obstacle_pos.append(line2)

            for i in range(20,460,10):
                line3=[]
                line3.append(690)
                line3.append(i)
                obstacle_pos.append(line3)

            for i in range(20,700,10):
                line4=[]
                line4.append(i)
                line4.append(20)
                obstacle_pos.append(line4)

        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(30, (frame_size_x-30)//10) * 10, random.randrange(30, (frame_size_y-30)//10)*10]
        food_spawn = True

        if not deadfood_spawn:
            deadfood_pos = [random.randrange(30, (frame_size_x-30)//10) * 10, random.randrange(30, (frame_size_y-30)//10)*10]
            while snake_pos[0] == deadfood_pos[0] and snake_pos[1] == deadfood_pos[1]:
                deadfood_pos = [random.randrange(30, (frame_size_x-30)//10) * 10, random.randrange(30, (frame_size_y-30)//10)*10]
        deadfood_spawn= True

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        for pos in obstacle_pos:
            pygame.draw.rect(game_window, red, pygame.Rect(pos[0], pos[1], 10, 10))
        
        pygame.draw.rect(game_window, red, pygame.Rect(deadfood_pos[0], deadfood_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < block_size[0] or snake_pos[0] > block_size[1]:#snake의 좌표가 0보다 작거나 (x-10)값보다 크면 game over
            game_over()
            break
        if snake_pos[1] < block_size[2] or snake_pos[1] > block_size[3]:#snake의 좌표가 0보다 작거나 (y-10)값보다 크면 game over
            game_over()
            break



        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()
                loopbreak=False
                break
        if(loopbreak==False):
            break

        for block in snake_body[1:]:
            if snake_pos[0] == deadfood_pos[0] and snake_pos[1] == deadfood_pos[1]:
                game_over()
                loopbreak=False
                break
        if(loopbreak==False):
            break

        show_score(1, white, 'consolas', 20)#consolas글꼴의 하얀색 글씨 20크기로 현재 점수를 보여줌
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)

        