import pyautogui
import time

FIRSTCLICK_X = 2300
FIRSTCLICK_Y = 70
INBETWEENSLEEPTIME = 0.2
SECONDCLICK_X = 1760
SECONDCLICK_Y = 1140
TIMEOUTSLEEPTIME = 2

count = 0

time.sleep(3)

while True:
    # Click at pixel (2300, 70)
    pyautogui.click(FIRSTCLICK_X, FIRSTCLICK_Y)
    time.sleep(INBETWEENSLEEPTIME)

    # Click at pixel (1760, 1140)
    pyautogui.click(SECONDCLICK_X, SECONDCLICK_Y)
    time.sleep(TIMEOUTSLEEPTIME)  # Wait for 3 seconds before repeating
    count += 1
    print(count, end="\r")
