import pyautogui
import time
import random

RIGHTCLICK_X = 1890
RIGHTCLICK_Y = 970
FIRSTCLICK_X = 2055
FIRSTCLICK_Y = 1225
SECONDCLICK_XMIN = 600
SECONDCLICK_XMAX = 1100
SECONDCLICK_YMIN = 600
SECONDCLICK_YMAX = 1100
CONFIRMCLICK_X = 760
CONFIRMCLICK_Y = 1550
SLEEPTIME = 0.15

time.sleep(3)
#pyautogui.click(RIGHTCLICK_X, RIGHTCLICK_Y, button='right')

while True:
    # Click at pixel (2055, 1225)
    pyautogui.click(FIRSTCLICK_X, FIRSTCLICK_Y)
    time.sleep(SLEEPTIME)

    # Generate random x and y coordinates
    x = random.randint(SECONDCLICK_XMIN, SECONDCLICK_XMAX)
    y = random.randint(SECONDCLICK_YMIN, SECONDCLICK_YMAX)

    # Click at the random coordinates
    pyautogui.click(x, y)
    time.sleep(SLEEPTIME)

    # Click at pixel (760, 1550)
    pyautogui.click(CONFIRMCLICK_X, CONFIRMCLICK_Y)
    time.sleep(SLEEPTIME)
