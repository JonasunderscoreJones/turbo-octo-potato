import pyautogui
import time
import random

# The position of the right-click to open the context menu on an object
RIGHTCLICK_X = 1890
RIGHTCLICK_Y = 970

# The position of the "Color Tint" button in the context menu
FIRSTCLICK_X = 2055
FIRSTCLICK_Y = 1225

# The position of the upper left corner of the color-selector square
SECONDCLICK_XMIN = 600
SECONDCLICK_YMIN = 600

# The position of the lower right corner of the color-selector square
SECONDCLICK_XMAX = 1100
SECONDCLICK_YMAX = 1100

# The position of the "Apply" button of the color selector
CONFIRMCLICK_X = 760
CONFIRMCLICK_Y = 1550

# The timeout for UI elements to load (in seconds)
SLEEPTIME = 0.15

# initialize the counter
count = 0

time.sleep(3) # delay to focus the game after launching the script

# Move to and rightclick on the object
pyautogui.moveTo(RIGHTCLICK_X, RIGHTCLICK_Y)
pyautogui.click(RIGHTCLICK_X, RIGHTCLICK_Y, button='right')

while count < 1000:
    # Click on the "Color Tint" option
    pyautogui.click(FIRSTCLICK_X, FIRSTCLICK_Y)
    time.sleep(SLEEPTIME)

    # Generate random x and y coordinates
    x = random.randint(SECONDCLICK_XMIN, SECONDCLICK_XMAX)
    y = random.randint(SECONDCLICK_YMIN, SECONDCLICK_YMAX)

    # Click at the random coordinates
    pyautogui.click(x, y)
    time.sleep(SLEEPTIME)

    # Click on the "Apply" button
    pyautogui.click(CONFIRMCLICK_X, CONFIRMCLICK_Y)
    time.sleep(SLEEPTIME)
