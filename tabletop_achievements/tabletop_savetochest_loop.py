import pyautogui
import time
import os

time.sleep(3)

while True:
    # Click at pixel (1870, 675)
    pyautogui.moveTo(1870, 675)
    pyautogui.click(1870, 675, button='right')
    time.sleep(0.15)

    # Click at pixel (2030, 875)
    pyautogui.click(2030, 875)
    time.sleep(0.15)

    # Click at pixel (1700, 1110)
    pyautogui.click(1700, 1110)
    time.sleep(0.15)

    # Get the current Unix timestamp
    timestamp = str(int(time.time()))

    # Enter the timestamp as key presses
    pyautogui.write(timestamp)

    # Click at pixel (1770, 1200)
    pyautogui.click(1770, 1200)
    time.sleep(0.2)
