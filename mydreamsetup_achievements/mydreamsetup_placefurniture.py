import pyautogui
import time

# Constant delay in seconds
DELAY = 0.125
DELAY = 0

# Define the main function to perform the clicks
def perform_clicks():
    while True:
        # Click on pixel (300, 150)
        pyautogui.click(300, 150)
        time.sleep(DELAY)

        # Click on pixel (960, 530)
        pyautogui.click(960, 530)
        time.sleep(DELAY)

        # Click on pixel (960, 530) again
        pyautogui.click(960, 530)
        time.sleep(DELAY)

        # Click on pixel (960, 555)
        pyautogui.click(960, 555)
        time.sleep(DELAY)

# Start the clicking loop
if __name__ == "__main__":
    time.sleep(5)
    perform_clicks()
