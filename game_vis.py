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
usr_height = 75
usr_x = display_width // 3 - 200
usr_y = display_height - usr_height - 450
usr_image = load_image('герой.png')

clock = pygame.time.Clock()
FPS = 80
invisible = False
can_jump = False
can_tp_up = False
can_tp_down = False
time_over = False
count_jump = 30

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
    global can_jump, can_tp_up, can_tp_down, invisible, usr_color
    game = True
    enemy_arr_c = []
    create_enemy_classic(enemy_arr_c)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            print('w')
            can_tp_up = True

        if keys[pygame.K_SPACE]:
            print('SPACE')
            can_jump = True

        if keys[pygame.K_DOWN]:
            print('s')
            can_tp_down = True

        if keys[pygame.K_z]:
            print('Z')
            invisible = True

        if keys[pygame.K_d] or keys[pygame.K_a]:
            print('уже иду!')
            go()

        if keys[pygame.K_ESCAPE]:
            pause()

        if can_jump:
            jump()

        if can_tp_down:
            teleport_down()
            print('Должен идти вниз')

        if can_tp_up:
            teleport_up()
            print('Должен идти вверх')

        if invisible:
            cube_inv()

        if keys[pygame.K_BACKSPACE]:
            game = False

        display.blit(background, (0, 0))
        draw_enemy_classic(enemy_arr_c)

        draw_usr()
        draw_terra()

        pygame.display.update()
        clock.tick(FPS)


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


def teleport_up():
    global usr_y, can_tp_up, display_height, usr_height
    print('Лети вверх')
    usr_y -= 300
    time.sleep(0.2)
    can_tp_up = False


def teleport_down():
    global usr_y, can_tp_down, display_height, usr_height
    print('Лети вниз')
    usr_y += 300
    time.sleep(0.2)
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


def draw_terra():
    pygame.draw.line(display, (0, 0, 0), [0, display_height - 150], [1280, display_height - 150], 5)
    pygame.draw.line(display, (0, 0, 0), [0, display_height - 450], [1280, display_height - 450], 5)
    pygame.draw.line(display, (0, 0, 0), [0, display_height - 750], [1280, display_height - 750], 5)


def create_enemy_classic(array):
    array.append(Enemy_classic(display_width - 50, display_height - 240, 40, 90, 9))
    array.append(Enemy_classic(display_width + 300, display_height - 220, 60, 70, 5))
    array.append(Enemy_classic(display_width - 500, display_height - 165, 200, 15, 3))


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


game_running()
