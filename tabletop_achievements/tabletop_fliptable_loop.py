import pyautogui
import time

# The position of the "Flip" button at the top of the screen
FIRSTCLICK_X = 2300
FIRSTCLICK_Y = 70

# The timeout for UI elements to load (in seconds)
INBETWEENSLEEPTIME = 0.2

# The position of the "Yes" button of the "FLip table?" prompt
SECONDCLICK_X = 1760
SECONDCLICK_Y = 1140

# The timeout set by the game until the "Flip" button becomes clickable again (in seconds)
TIMEOUTSLEEPTIME = 2

# The amount of iterations depending on the achievement
ITERATIONS = 100

# initialize the counter
count = 0

time.sleep(3) # delay to focus the game after launching the script

while count < ITERATIONS:
    # Click the "Flip" button
    pyautogui.click(FIRSTCLICK_X, FIRSTCLICK_Y)
    time.sleep(INBETWEENSLEEPTIME)

    # Click the confirmation button
    pyautogui.click(SECONDCLICK_X, SECONDCLICK_Y)

    # update the counter and display it
    count += 1
    print(count, end="\r")

    time.sleep(TIMEOUTSLEEPTIME)  # Wait for 3 seconds before repeating
