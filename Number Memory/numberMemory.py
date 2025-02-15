import pyautogui
import numpy as np
import time
import webbrowser
import cv2
import easyocr

URL = "https://humanbenchmark.com/tests/number-memory"

BLUE = np.array([43, 135, 209])

def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(1)

def start_game():
    screenWidth, screenHeight = pyautogui.size()
    game_lower_border = -1
    game_upper_border = screenHeight
    screenshot = np.array(pyautogui.screenshot())
    for y in range(screenHeight):
        if np.array_equal(screenshot[y][screenWidth//2], BLUE):
            if game_lower_border < 0:
                game_lower_border = y
            else:
                game_upper_border = y
    
    button_location = pyautogui.locateCenterOnScreen("StartButton.png", confidence=0.9)
    for i in range(100):
        pyautogui.click(button_location)
        detect_number(i, game_lower_border, game_upper_border, screenWidth)

def detect_number(level, game_lower_border, game_upper_border, screenWidth):
    time.sleep(1)
    level_cooldown = time.time() + level + 1

    game_size = game_upper_border - game_lower_border
    screenshot_path = f"number.png"
    image = pyautogui.screenshot(screenshot_path, region=(0, game_lower_border, screenWidth, game_size))

    # Convert to OpenCV format
    image = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding to improve contrast
    _, image = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY)

    # Save processed image for debugging
    # cv2.imwrite(f"processed_{level}.png", image)

    reader = easyocr.Reader(['en'])
    data = reader.readtext(image)

    print(data)
    time.sleep(max(0, level_cooldown-time.time()))
    number = ''
    for x in data:
        number+=x[1]
    pyautogui.write(number)
    pyautogui.write('\n')

open_human_benchmark()
start_game()