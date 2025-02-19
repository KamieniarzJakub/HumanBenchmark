import pyautogui
import numpy as np
import time
import webbrowser
import easyocr
import cv2

URL = "https://humanbenchmark.com/tests/chimp"

MAX_LEVEL = 41

BLUE = np.array([43, 135, 209])
NUMBER_BORDER_COLOR = np.array([68, 152, 212])


def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(1)

def start_game():
    
    button_location = pyautogui.locateCenterOnScreen("StartButton.png", confidence=0.9)
    for level in range(3, MAX_LEVEL):
        time.sleep(0.5)
        pyautogui.click(button_location)
        pyautogui.screenshot(f"level {level}.png")

        positions = sorted(remember_board(), key=lambda x: x[0])
        
        for x in positions:
            pyautogui.click(x[1])

def determine_game_size():
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
    return (screenWidth//10, int(game_lower_border), int(0.8*screenWidth), int(game_upper_border-game_lower_border)), screenWidth//10, game_lower_border

def remember_board():
    positions = []
    game_size, x_border, y_border = determine_game_size()
    screenshot = np.array(pyautogui.screenshot("level.png", region=game_size))
    for y in range(len(screenshot)-100):
        for x in range(len(screenshot[y])-100):
            if np.array_equal(screenshot[y][x], BLUE):
                continue
            image = screenshot[y:y+100, x:x+100]
            cv2.imwrite(f"number.png", image)
            image = cv2.imread(f"number.png", cv2.IMREAD_GRAYSCALE)
            _, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
            reader = easyocr.Reader(["en"])
            data = reader.readtext(image, allowlist="1234567890", detail=0)
            screenshot[y-10:y+100, x-10:x+100] = BLUE
            print(data)
            try:
                positions.append([int(data[0]), (x+x_border+50, y+y_border+50)])
            except:
                positions.append([7, (x+x_border+50, y+y_border+50)])
    print()
    return positions

open_human_benchmark()
start_game()