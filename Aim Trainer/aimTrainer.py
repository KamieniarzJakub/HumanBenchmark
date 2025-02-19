import pyautogui
import numpy as np
import time
import webbrowser

URL = "https://humanbenchmark.com/tests/aim"

TARGETS = 30

BLUE = np.array([43, 135, 209])

pyautogui.PAUSE = 0.02

def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(3)

def click_on_targets():
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
    game_length=int(game_upper_border-game_lower_border)
    game_size = (int(screenWidth*0.2), int(game_lower_border)+int(0.1*game_length), int(0.6*screenWidth), int(0.8*game_length))
    pyautogui.click(pyautogui.locateCenterOnScreen("target.png", region=game_size, confidence=0.9, grayscale=True))
    for _ in range(TARGETS):
        pyautogui.click(pyautogui.locateCenterOnScreen("target.png", region=game_size, confidence=0.23, grayscale=True))
        

open_human_benchmark()
click_on_targets()