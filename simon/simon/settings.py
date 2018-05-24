from . import constants


FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FLASH_SPEED = 500 # in milliseconds
FLASH_DELAY = 200 # in milliseconds
BUTTON_SIZE = 200
BUTTON_GAP_SIZE = 20
TIMEOUT = 4 # seconds before game over if no button is pushed.

X_MARGIN = int((WINDOW_WIDTH - (2 * BUTTON_SIZE) - BUTTON_GAP_SIZE) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (2 * BUTTON_SIZE) - BUTTON_GAP_SIZE) / 2)

BG_COLOR = constants.BLACK
