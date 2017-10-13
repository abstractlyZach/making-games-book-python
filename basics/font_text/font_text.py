import sys

import pygame
from pygame.locals import QUIT

pygame.init()

DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

font_object = pygame.font.Font('freesansbold.ttf', 32)
text_surface_object = font_object.render('Hello world!', True, GREEN, BLUE)
text_rect_object = text_surface_object.get_rect()
text_rect_object.center = (200, 150)

while True:
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(text_surface_object, text_rect_object)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
