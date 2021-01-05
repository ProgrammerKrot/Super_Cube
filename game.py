import os
import sys

import pygame

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
screen_size = (1280, 920)
clock = pygame.time.Clock()
FPS = 50
tile_width = tile_height = 50


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["нажмите любую кнопку",
                  "чтобы продолжить", " "
                  "ХЭйо",
                  "Тут будет игра"]

    fon = pygame.transform.scale(load_image('fonk.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Geometry run')

start_screen()