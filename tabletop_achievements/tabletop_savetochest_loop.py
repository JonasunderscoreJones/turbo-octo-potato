import pyautogui
import time
import os

RIGHTCLICK_X = 1870
RIGHTCLICK_Y = 675
SAVECONTEXTMENUCLICK_X = 2030
SAVECONTEXTMENUCLICK_Y = 875
NAMEFIELDCLICK_X = 1700
NAMEFIELDCLICK_Y = 1110
SAVECLICK_X = 1770
SAVECLICK_Y = 1200


time.sleep(3)

while True:
    # Click at pixel (1870, 675)
    pyautogui.moveTo(RIGHTCLICK_X, RIGHTCLICK_Y)
    pyautogui.click(RIGHTCLICK_X, RIGHTCLICK_Y, button='right')
    time.sleep(0.15)

    # Click at pixel (2030, 875)
    pyautogui.click(SAVECONTEXTMENUCLICK_X, SAVECONTEXTMENUCLICK_Y)
    time.sleep(0.15)

    # Click at pixel (1700, 1110)
    pyautogui.click(NAMEFIELDCLICK_X, NAMEFIELDCLICK_Y)
    time.sleep(0.15)

    # Get the current Unix timestamp
    timestamp = str(int(time.time()))

    # Enter the timestamp as key presses
    pyautogui.write(timestamp)

    # Click at pixel (1770, 1200)
    pyautogui.click(SAVECLICK_X, SAVECLICK_Y)
    time.sleep(0.2)
