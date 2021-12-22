import pygame


def scale_img(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def resize_img(img, size):
    return pygame.transform.scale(img, (size, size))
