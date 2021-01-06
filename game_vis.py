import pygame

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Teleportation cube')

icon = pygame.image.load('свас.jpg')
pygame.display.set_icon(icon)

usr_width = 75
usr_height = 75
usr_x = display_width // 3 - 200
usr_y = display_height - usr_height - 300

clock = pygame.time.Clock()
FPS = 60


def game_running():
    game = True

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill((92, 86, 26))

        pygame.draw.rect(display, (41, 240, 200), (usr_x, usr_y, usr_width, usr_height))

        pygame.display.update()
        clock.tick(FPS)


game_running()