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


screen_height = 1280
screen_width = 920
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

    fon = pygame.transform.scale(load_image('fonk.jpg'), (screen_height, screen_width))
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption('Geometry run')

icon = pygame.image.load('свас.jpg')
pygame.display.set_icon(icon)

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Walls:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self):
        if self.x >= - self.width:
            pygame.draw.rect(screen, (0, 255, 153), (self.x, self.y, self.width, self.height))
            self.x -= self.speed
            return True
        else:
            # self.x = display_width + 10 + random.randrange(-60, 80)
            return False

usr_width = 60
usr_height = 100
usr_x, usr_y = screen_width // 3, screen_height - usr_height - 100

cactus_width, cactus_height = 20, 70,
cactus_x, cactus_y = 50, screen_height - cactus_height - 100
clock = pygame.time.Clock()

make_jump = False
count_jump = 30

start_screen()

