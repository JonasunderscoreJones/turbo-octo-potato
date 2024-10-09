import pyautogui
import time
import os

# The position of the right click to open the context menu for the object
RIGHTCLICK_X = 1870
RIGHTCLICK_Y = 675

# The position of the "Save Object" option in the context menu
SAVECONTEXTMENUCLICK_X = 2030
SAVECONTEXTMENUCLICK_Y = 875

# The position of the name input field in the "Save Object" poup
NAMEFIELDCLICK_X = 1700
NAMEFIELDCLICK_Y = 1110

# The position of the save button in the "Save Object" popup
SAVECLICK_X = 1770
SAVECLICK_Y = 1200

# The timeout for UI elements to load (in seconds)
TIMEOUTTIME = 0.15

# initialize the counter
count = 0


time.sleep(3) # delay to focus the game after launching the script

while count < 100:
    # Right click for context menu
    pyautogui.moveTo(RIGHTCLICK_X, RIGHTCLICK_Y)
    pyautogui.click(RIGHTCLICK_X, RIGHTCLICK_Y, button='right')
    time.sleep(TIMEOUTTIME)

    # Click on the "Save Object" option in the context menu
    pyautogui.click(SAVECONTEXTMENUCLICK_X, SAVECONTEXTMENUCLICK_Y)
    time.sleep(TIMEOUTTIME)

    # Click on the name input field to focus it
    pyautogui.click(NAMEFIELDCLICK_X, NAMEFIELDCLICK_Y)
    time.sleep(TIMEOUTTIME)

    # Get the current Unix timestamp
    timestamp = str(int(time.time()))

    # Enter the timestamp as key presses
    pyautogui.write(timestamp)

    # Click on the save button
    pyautogui.click(SAVECLICK_X, SAVECLICK_Y)
    time.sleep(TIMEOUTTIME)

    # update the counter and display it
    count += 1
    print(count, end='\r')
