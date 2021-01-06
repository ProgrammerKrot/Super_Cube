import pygame

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
count_jump = 30


def game_running():
    global can_jump
    game = True

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            can_jump = True

        if can_jump:
            jump()


        display.fill((92, 86, 26))

        pygame.draw.rect(display, (41, 240, 200), (usr_x, usr_y, usr_width, usr_height))

        pygame.display.update()
        clock.tick(FPS)


def jump():
    global usr_y, count_jump, can_jump
    if count_jump >= -30:
        usr_y -= count_jump / 3
        count_jump -= 1
        pass
    else:
        count_jump = 30
        can_jump = False


game_running()