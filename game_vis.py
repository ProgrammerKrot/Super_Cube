import pygame
import time

pygame.init()

display_width = 1280
display_height = 920

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Teleportation cube')

icon = pygame.image.load('свас.jpg')
pygame.display.set_icon(icon)

usr_width = 75
usr_height = 75
usr_x = display_width // 3 - 200
usr_y = display_height - usr_height - 450

clock = pygame.time.Clock()
FPS = 60
can_jump = False
can_tp_up = False
can_tp_down = False
time_over = False
count_jump = 30


def game_running():
    global can_jump, can_tp_up, can_tp_down
    game = True

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            can_jump = True

        if keys[pygame.K_w]:
            can_tp_up = True

        if keys[pygame.K_s]:
            can_tp_down = True

        if can_jump:
            jump()

        if can_tp_down:
            teleport_down()

        if can_tp_up:
            teleport_up()


        display.fill((92, 86, 26))

        pygame.draw.rect(display, (41, 240, 200), (usr_x, usr_y, usr_width, usr_height))
        draw_terra()

        pygame.display.update()
        clock.tick(FPS)


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
    if usr_y == display_height - usr_height - 450 or usr_y == display_height - usr_height - 450 + 300:
        usr_y -= 300
        time.sleep(0.15)
        can_tp_up = False


def teleport_down():
    global usr_y, can_tp_down, display_height, usr_height
    if usr_y == display_height - usr_height - 450 or \
            usr_y == display_height - usr_height - 450 - 300:
        usr_y += 300
        time.sleep(0.15)
        can_tp_down = False



def draw_terra():
    pygame.draw.line(display, (0, 0, 0), [0, display_height - 150], [1280, display_height - 150], 5)
    pygame.draw.line(display, (0, 0, 0), [0, display_height - 450], [1280, display_height - 450], 5)
    pygame.draw.line(display, (0, 0, 0), [0, display_height - 750], [1280, display_height - 750], 5)



game_running()