import numpy as np
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
K_LEFT = ord('a')
K_RIGHT = ord('d')
K_UP = ord('w')
K_DOWN = ord('s')
SCALE = 64
BUTTON_FEEDBACK = False
DAYLIGHT_SPEED = 2
DAYLIGHT_DIVISOR = 1/DAYLIGHT_SPEED
UPDATE = True

SPEED = 1
ACCELERATION=.02
MAX_MAG = 500
JOYSTICK_CONTRIBUTION=0.08
PRESS_TO_MOVE = True

DARK_COLOR = np.array([50,32,66])
SUN_BRIGHTNESS = 1
CAMERA_ANGLE = np.array([180,180,180])
SOURCE_CUTOFF = .25