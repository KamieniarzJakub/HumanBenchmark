import pyautogui
import numpy as np
import time
import webbrowser

URL = "https://humanbenchmark.com/tests/sequence"

BUTTON_COLOR = np.array([255, 209, 84])
BLUE = np.array([43, 135, 209])

screenWidth, screenHeight = pyautogui.size()

def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(3)

def remember_sequence():
    game_lower_border = -1
    game_upper_border = screenHeight
    button_height = None
    screenshot = np.array(pyautogui.screenshot())
    for x in range(screenHeight):
        if np.array_equal(screenshot[x][screenWidth//2], BLUE):
            if game_lower_border==-1:
                game_lower_border = x
            else:
                game_upper_border = x
        if np.array_equal(screenshot[x][screenWidth//2], BUTTON_COLOR):
            button_height = x
    pyautogui.click(screenWidth//2, button_height)
    for level in range(1, 10):
        play_level(level, game_lower_border, game_upper_border)
        time.sleep(0.75)
    
    
def play_level(level, game_lower_border, game_upper_border):
    game_size = (0, game_lower_border, screenWidth, game_upper_border-game_lower_border)
    original = np.array(pyautogui.screenshot(region=game_size))
    screenshot = original
    level_memory = [original]*level
    for i in range(level):
        while True:
            new = np.array(pyautogui.screenshot(f"{level} {i+1}.png", region=game_size))
            new-=original
            print(np.where([new>0]))
            if not np.array_equal(screenshot, new) and not np.array_equal(original, new):
                screenshot = new
                level_memory[i] = screenshot
                time.sleep(0.65-level*0.035)
                break
    for i in range(level):
        click(original, level_memory[i], game_lower_border, game_upper_border)
        time.sleep(0.1)
        

def click(original, level, game_lower_border, game_upper_border):
    for y in range(game_upper_border-game_lower_border):
        if not np.array_equal(original[y], level[y]):
            for x in range(screenWidth):
                if not np.array_equal(original[y][x], level[y][x]):
                    pyautogui.click(x, game_lower_border+y)
                    return

open_human_benchmark()
remember_sequence()