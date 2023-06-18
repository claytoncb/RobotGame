import numpy as np
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
K_LEFT = ord('a')
K_RIGHT = ord('d')
K_UP = ord('w')
K_DOWN = ord('s')
SCALE = 64
BUTTON_FEEDBACK = False

DAYLIGHT_SPEED = 10
DAYLIGHT_DIVISOR = 1/DAYLIGHT_SPEED
DARKNESS_SHIFT = 0.0
SUN_BRIGHTNESS = .005
SUN_DARKNESS = .005
UPDATE = True

SPEED = 1
ACCELERATION=.02
MAX_MAG = 500
JOYSTICK_CONTRIBUTION=0.08
PRESS_TO_MOVE = True

DARK_COLOR = np.array([30,48,54])
LIGHT_COLOR = np.array([248,255,205])

CAMERA_ANGLE = np.array([180,180,180])
SOURCE_CUTOFF = .25