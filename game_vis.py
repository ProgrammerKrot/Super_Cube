import pygame
import time
import os


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    print(fullname)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удается загрузить', fullname)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()

display_width = 1280
display_height = 1024

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Teleportation cube')

icon = load_image('usr_slavs.png')
pygame.display.set_icon(icon)

background = pygame.image.load(r'background.jpg')

enemy_width, enemy_height = 35, 70
enemy_x, enemy_y = display_width - 50, display_height - enemy_height - 150

usr_width = 75
usr_height = 150
usr_x = display_width // 3 - 200
usr_y = display_height - usr_height - 500
usr_image = load_image('usr.stand.png')

clock = pygame.time.Clock()
FPS = 80
invisible = False
can_jump = False
can_tp_up = False
can_tp_down = False
time_over = False
count_jump = 30
count_tp = 1
sit_yep = False


class Enemy_classic:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            pygame.draw.rect(display, (30, 144, 255), (self.x, self.y, self.width, self.height))
            self.x -= self.speed
        else:
            self.x = display_width - 50


def game_running():
    global can_jump, can_tp_up, sit_yep, usr_image,can_tp_down, invisible, usr_color
    game = True
    enemy_arr_one_floor = []
    enemy_arr_two_floor = []
    create_enemy_classic(enemy_arr_one_floor)
    create_bullet_enemy(enemy_arr_two_floor)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    print('w')
                    can_tp_up = True

                if event.key == pygame.K_DOWN:
                    print('s')
                    can_tp_down = True

        usr_image = load_image('usr.stand.png')
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            print('SPACE')
            can_jump = True

        if keys[pygame.K_x]:
            print('x')
            sprint()

        if keys[pygame.K_z]:
            print('Z')
            invisible = True

        if keys[pygame.K_d] or keys[pygame.K_a]:
            print('уже иду!')
            go()

        if keys[pygame.K_c]:
            sit_yep = True

        if keys[pygame.K_ESCAPE]:
            pause()

        if can_jump:
            jump()

        if sit_yep:
            sit()

        if can_tp_down or can_tp_up:
            teleport()

        if invisible:
            cube_inv()

        if keys[pygame.K_BACKSPACE]:
            game = False


        display.blit(background, (0, 0))
        draw_enemy_classic(enemy_arr_one_floor)
        draw_enemy_classic(enemy_arr_two_floor)

        draw_usr()
        draw_terra()

        if check_collision(enemy_arr_one_floor) or check_collision(enemy_arr_two_floor):
            game = False

        pygame.display.update()
        clock.tick(FPS)
    return game_over()

def draw_usr():
    display.blit(usr_image, (usr_x, usr_y))


def jump():
    global usr_y, count_jump, can_jump
    if count_jump >= -30:
        usr_y -= count_jump / 3
        count_jump -= 1
    else:
        count_jump = 30
        can_jump = False


def teleport():
    global usr_y, can_jump,can_tp_up, display_height, usr_height, can_tp_down
    print('Лети вверх')
    if not can_jump:
        if can_tp_down and usr_y + 300 < 1024:
            usr_y += 300
        if can_tp_up and usr_y - 300 > 0:
            usr_y -= 300
    can_tp_up = False
    can_tp_down = False


def cube_inv():
    global invisible
    print('меняю цвет')
    invisible = False


def go():
    global usr_x
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        if usr_x <= 1205: #чтобы персонаж не выходил за пределы окна
            usr_x += 2
    if keys[pygame.K_a]:
        if usr_x >= 0:#чтобы персонаж не выходил за пределы окна
            usr_x -= 2

def sit():
    global usr_image, sit_yep, usr_height
    if sit_yep:
        usr_image = load_image('usr.png')
        usr_height -= 125
    sit_yep = False
    usr_height += 125



def sprint():
    global usr_x
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        for i in range(1):
            if usr_x - 5 > 0:
                usr_x -= 5
    if keys[pygame.K_d]:
        for i in range(1):
            if usr_x + 5 < 1180:
                usr_x += 5


def draw_terra():
    pygame.draw.line(display, (0, 0, 0), [0, display_height - 150], [1280, display_height - 150], 5)
    pygame.draw.line(display, (0, 0, 0), [0, display_height - 450], [1280, display_height - 450], 5)
    pygame.draw.line(display, (0, 0, 0), [0, display_height - 750], [1280, display_height - 750], 5)


def create_enemy_classic(array):
    array.append(Enemy_classic(display_width - 50, display_height - 240, 40, 90, 9))
    array.append(Enemy_classic(display_width + 300, display_height - 220, 60, 70, 5))
    array.append(Enemy_classic(display_width - 500, display_height - 165, 200, 15, 3))


def create_bullet_enemy(array):
    array.append(Enemy_classic(display_width - 100, display_height - 600, 30, 10, 5))
    array.append(Enemy_classic(display_width + 350, display_height - 600, 30, 10, 5))
    array.append(Enemy_classic(display_width - 550, display_height - 600, 30, 10, 5))


def draw_enemy_classic(array):
    for enemy_classic in array:
        Enemy_classic.move(enemy_classic)


def print_text(massage, x, y, font_color = (0, 0, 0), font_type = 'fonts.otf', font_size = 40):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(massage, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Пауза', 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(30)


def check_collision(barriers):
    for barrier in barriers:
        if usr_y + usr_height >= barrier.y + barrier.height:
            if barrier.x <= usr_x <= barrier.x + barrier.width:
                return True
            elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                return True
    return False

def game_over():
    stoped = True
    while stoped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over', 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True

        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(30)


while game_running():
    pass
pygame.quit()
quit()
