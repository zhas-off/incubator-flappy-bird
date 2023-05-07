import pygame, sys, random

# Рисуем поверхность
def draw_floor():
    screen.blit(floor_sur, (floor_x, 600))
    screen.blit(floor_sur, (floor_x + 430, 600))

# Создание трубы
def create_pipe():
    random_pos = random.choice(pipe_height)
    bottom_pipe = pipe_sur.get_rect(midtop=(700, random_pos))
    top_pipe = pipe_sur.get_rect(midbottom=(700, random_pos - 200))
    return bottom_pipe, top_pipe

# Движение труб
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

# Рисуем трубы
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 700:
            screen.blit(pipe_sur, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_sur, False, True)
            screen.blit(flip_pipe, pipe)

# Проверяем на столкновение
def check_collison(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            die_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 600:
        die_sound.play()
        can_score = True
        return False

    return True

# Поворот птицы
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

# Анимация птицы
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

# Вывод счета
def score_display(game_state):
    if game_state == "main_game":
        score_sur = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_sur.get_rect(center=(215, 70))
        screen.blit(score_sur, score_rect)

    if game_state == "game_over":
        score_sur = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_sur.get_rect(center=(215, 70))
        screen.blit(score_sur, score_rect)

        high_score_sur = game_font.render(
            f"High Score: {int(high_score)}", True, (255, 255, 255)
        )
        high_score_rect = high_score_sur.get_rect(center=(215, 550))
        screen.blit(high_score_sur, high_score_rect)

# Обновление счета
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# Проверяем счет трубы
def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


pygame.init()
screen = pygame.display.set_mode((430, 700))
clock = pygame.time.Clock()
game_font = pygame.font.Font("assets/sprites/font.ttf", 30)

# Игровые переменные
gravity = 0.3
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

background = pygame.image.load("assets/sprites/background-day.png").convert()
background = pygame.transform.scale2x(background)

floor_sur = pygame.image.load("assets/sprites/base.png").convert()
floor_sur = pygame.transform.scale2x(floor_sur)
floor_x = 0

bird_downflap = pygame.image.load("assets/sprites/yellowbird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("assets/sprites/yellowbird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("assets/sprites/yellowbird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_sur = bird_frames[bird_index]
bird_rect = bird_sur.get_rect(center=(100, 300))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_sur = pygame.image.load("assets/sprites/pipe-green.png")
pipe_sur = pygame.transform.scale2x(pipe_sur)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 850)
pipe_height = [200, 300, 400]

game_over_sur = pygame.image.load("assets/sprites/message.png").convert_alpha()
game_over_rect = game_over_sur.get_rect(center=(215, 310))

flap_sound = pygame.mixer.Sound("assets/audio/wing.wav")
hit_sound = pygame.mixer.Sound("assets/audio/hit.wav")
score_sound = pygame.mixer.Sound("assets/audio/point.wav")
die_sound = pygame.mixer.Sound("assets/audio/die.wav")
score_sound_countdown = 100

# Основная функция
if __name__ == "__main__":

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 10
                    flap_sound.play()
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 300)
                    bird_movement = 0
                    score = 0

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())

            if event.type == BIRDFLAP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0

                bird_sur, bird_rect = bird_animation()

        screen.blit(background, (0, 0))

        if game_active:
            # Птица
            bird_movement += gravity + 0.07
            rotated_bird = rotate_bird(bird_sur)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)
            game_active = check_collison(pipe_list)

            # Трубы
            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            # Счет
            pipe_score_check()
            score_display("main_game")
        else:
            screen.blit(game_over_sur, game_over_rect)
            high_score = update_score(score, high_score)
            score_display("game_over")

        # Пол
        floor_x -= 1
        draw_floor()
        if floor_x <= -430:
            floor_x = 0

        pygame.display.update()
        clock.tick(100)
