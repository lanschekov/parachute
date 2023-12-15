import os
import random
import sys
from typing import Any

import pygame

SIZE = WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode(SIZE)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Mountain(pygame.sprite.Sprite):
    image = load_image('mountains.png')

    def __init__(self, *groups):
        super(Mountain, self).__init__(*groups)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = HEIGHT


class Parachute(pygame.sprite.Sprite):
    image = load_image('pt.png')

    def __init__(self, pos: tuple[float, float], *groups):
        super(Parachute, self).__init__(*groups)
        self.image = Parachute.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, *args: Any, **kwargs: Any) -> None:
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(0, 1)


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    parachutes = pygame.sprite.Group()
    mountain = Mountain(all_sprites)

    fps = 50
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Parachute(event.pos, parachutes)

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()

        parachutes.draw(screen)
        parachutes.update()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
