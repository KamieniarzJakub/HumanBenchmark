import pyautogui
import numpy as np
import time
import webbrowser
import cv2

URL = "https://humanbenchmark.com/tests/memory"

DARK_BLUE = np.array([37, 115, 193])
WHITE = np.array([255, 255, 255])
MARGIN = 5

def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(3)

def remember_level(max_level):
    button_location = pyautogui.locateCenterOnScreen("StartButton.png", confidence=0.9)
    pyautogui.click(button_location)
    screenWidth, screenHeight = pyautogui.size()
    game_lower_border = -1
    game_upper_border = screenHeight
    screenshot = np.array(pyautogui.screenshot())
    for y in range(screenHeight):
        if np.array_equal(screenshot[y][screenWidth//2], DARK_BLUE):
            if game_lower_border < 0:
                game_lower_border = y
            else:
                game_upper_border = y
        
    game_length = game_upper_border-game_lower_border
    game_size = (int(button_location.x)-game_length//2, game_lower_border, game_length, game_length)
    for level in range(max_level):
        play_level(level+1, game_lower_border, game_length, game_size, int(button_location.x)-game_length//2)
        time.sleep(0.75)
    
    
def play_level(level, game_lower_border, game_length, game_size, right_margin):
    time.sleep(1)
    
    screenshot = np.array(pyautogui.screenshot(f"level.png", region=game_size))
    time.sleep(2)
    tile_size, gap_size = determine_tile_size(game_size)
    clicked = 0
    for y in range(tile_size//2, len(screenshot), tile_size+gap_size):
        for x in range(tile_size//2, len(screenshot[y]), tile_size+gap_size):
            if np.array_equal(screenshot[y][x], WHITE):
                pyautogui.click(x+right_margin, y+game_lower_border)
                clicked+=1
                if clicked==level+2:
                    return
                #screenshot[max(0, y-tile_size):min(len(screenshot), y+tile_size), max(0, x-tile_size):min(len(screenshot[y]), x+tile_size)] = DARK_BLUE
                #cv2.imwrite(f"{level} {clicked}.png", screenshot)

def determine_tile_size(game_size):
    empty_level = np.array(pyautogui.screenshot("emtpy_level.png", region=game_size))
    i=0
    while not np.array_equal(empty_level[i][i], DARK_BLUE):
        i+=1
    j=i
    while np.array_equal(empty_level[i+10][j+1], DARK_BLUE):
        j+=1
    k=j+1
    while not np.array_equal(empty_level[i+10][k], DARK_BLUE):
        k+=1
    return j, k-j



open_human_benchmark()
remember_level(max_level=100)