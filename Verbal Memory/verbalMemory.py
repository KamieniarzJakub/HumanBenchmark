import pyautogui
import numpy as np
import time
import webbrowser
import cv2
import easyocr

URL = "https://humanbenchmark.com/tests/verbal-memory"

IGNORE_WORDS = ["Lives", "Score", "SEEN", "NEW", "|", "0", "1", "2", "3"]

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
    pyautogui.click(button_location)
    _, button_y, _, _ = pyautogui.locateOnScreen("SEENButton.png", confidence=0.9)
    seen_location = pyautogui.locateCenterOnScreen("SEENButton.png", confidence=0.9)
    new_location = pyautogui.locateCenterOnScreen("NEWButton.png", confidence=0.9)
    
    game_lower_border += game_upper_border-button_y
    game_upper_border = button_y
    words = set()
    for i in range(500):
        w = detect_world(game_lower_border, game_upper_border, screenWidth)
        if w in words:
            pyautogui.click(seen_location)
            continue
        words.add(w)
        pyautogui.click(new_location)
        
def detect_world(game_lower_border, game_upper_border, screenWidth):
    time.sleep(0.01)
    game_size = (screenWidth//4, int(game_lower_border), int(0.5*screenWidth), int(game_upper_border-game_lower_border))
    screenshot_path = "word.png"
    image = pyautogui.screenshot(screenshot_path, region=game_size)

    # Convert to OpenCV format
    image = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding to improve contrast
    _, image = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY)

    # Save processed image for debugging
    # cv2.imwrite(f"processed_{level}.png", image)

    reader = easyocr.Reader(['en'])
    data = reader.readtext(image)

    return data[0][1]


open_human_benchmark()
start_game()