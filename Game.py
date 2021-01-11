import pygame
import random

pygame.init()

display_width = 900
display_height = 650

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Space Runner')

icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(icon)

enemy_img = [pygame.image.load('enemy1.png')]

health_img = pygame.image.load('heart.png')
health_img = pygame.transform.scale(health_img, (30, 30))

health = 3

usr_width = 25
usr_height = 50
usr_x = display_width // 30
usr_y = display_height / 1.728

enemy_width = 70
enemy_height = 70
enemy_x = display_width - 50
enemy_y = display_height / 1.825

clock = pygame.time.Clock()

do_jump = False
count_jumps = 30

do_tp_up = False
do_tp_down = False

class Button:
    def __init__(self, width, height, inactive_color, active_color):
        self.width = width
        self.height = height
        self.inactive_color = (125, 61, 204)
        self.active_color = (120, 7, 232)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()

        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))

        print_text(message=message, x=x+10, y=y+10, font_size=font_size)

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            pygame.draw.rect(display, (200, 200, 200), [self.x, self.y, self.width, self.height])
            self.x -= self.speed
            return True
        else:
            # self.x = display_width + 50 + 100 + random.randrange(-80, 60)
            return False

    def return_self(self, radius):
        self.x = radius


def game_cycle():
    global do_jump, do_tp_up, do_tp_down
    game = True
    enemy_arr = []
    create_enemy_arr(enemy_arr)
    create_enemy2_arr(enemy_arr)
    create_enemy3_arr(enemy_arr)
    space_background = pygame.image.load('space_background.png')

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    do_tp_up = True

                if event.key == pygame.K_DOWN:
                    do_tp_down = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            do_jump = True

        if do_jump:
            jump()

        if do_tp_up or do_tp_down:
            teleport()

        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            go()

        if keys[pygame.K_ESCAPE]:
            pause()

        display.blit(space_background, (0, 0))
        draw_array(enemy_arr)

        show_health()

        pygame.draw.rect(display, (100, 100, 100), [usr_x, usr_y, usr_width, usr_height])

        if check_collision(enemy_arr):
            if not check_health():
                game = False

        pygame.display.update()
        clock.tick(60)
    return game_over()


def jump():
    global usr_y, do_jump, count_jumps
    if count_jumps >= -30:
        usr_y -= count_jumps / 3
        count_jumps -= 1
    else:
        count_jumps = 30
        do_jump = False


def teleport():
    global usr_y, do_jump, do_tp_up, do_tp_down, display_height, usr_height
    if not do_jump:
        if do_tp_down and usr_y + 221 < 650:
            usr_y += 221
        if do_tp_up and usr_y - 221 > 0:
            usr_y -= 221
    do_tp_up = False
    do_tp_down = False


def go():
    global usr_x
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if usr_x <= 850:
            usr_x += 5
    if keys[pygame.K_LEFT]:
        if usr_x >= 3:
            usr_x -= 5


def create_enemy_arr(array):
    array.append(Enemy(display_width + 20, display_height - 275, 60, 20, 4))
    array.append(Enemy(display_width + 300, display_height - 275, 30, 50, 4))
    array.append(Enemy(display_width + 600, display_height - 437, 25, 100, 4))


def create_enemy2_arr(array):
    array.append(Enemy(display_width + 100, display_height - 34, 100, 30, 4))
    array.append(Enemy(display_width + 380, display_height - 217, 20, 110, 4))
    array.append(Enemy(display_width + 680, display_height - 64, 50, 60, 4))


def create_enemy3_arr(array):
    array.append(Enemy(display_width + 200, display_height - 646, 40, 90, 4))
    array.append(Enemy(display_width + 480, display_height - 475, 80, 30, 4))
    array.append(Enemy(display_width + 780, display_height - 646, 25, 130, 4))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 350)

    return radius


def draw_array(array):
    for enemy in array:
        check = enemy.move()
        if not check:
            radius = find_radius(array)
            enemy.return_self(radius)


def print_text(message, x, y, font_color=(0, 0, 0), font_type='fonts.otf', font_size=40):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Пауза', 360, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)


def check_collision(barriers):
    for barrier in barriers:
        if usr_y == display_height / 1.728:
            if usr_y + usr_height >= barrier.y + barrier.height:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    return True
                elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                    return True

        if usr_y == display_height / 1.728 + 221:
            if usr_y + usr_height >= barrier.y + barrier.height:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    return True
                elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                    return True

        if usr_y == display_height / 1.728 - 221:
            if usr_y + usr_height >= barrier.y + barrier.height:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    return True
                elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                    return True
    return False


def game_over():
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over', 320, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)


def show_health():
    global health
    show = 0
    x = 800
    while show != health:
        display.blit(health_img, (x, 15))
        x += 25
        show += 1


def check_health():
    global health
    health -= 1
    if health == 0:
        return False
    else:
        return True


def show_menu():
    menu_background = pygame.image.load('menu.png')

    start_btn = Button(190, 65, (125, 61, 204), (120, 7, 232))
    quit_btn = Button(190, 65, (125, 61, 204), (120, 7, 232))

    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(menu_background, (0, 0))
        start_btn.draw(345, 260, 'Start', start_game, 50)
        quit_btn.draw(345, 350, 'Exit', quit, 50)

        pygame.display.update()
        clock.tick(60)

def start_game():
    global health

    while game_cycle():
        pass


show_menu()

while game_cycle():
    health = 3

pygame.quit()
quit()
