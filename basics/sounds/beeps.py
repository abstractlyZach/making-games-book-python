import time
import sys

import pygame

pygame.init()

sound_object = pygame.mixer.Sound('beep1.ogg')
sound_object.play()
time.sleep(1)
sound_object.stop()
