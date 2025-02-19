import pyautogui
import numpy as np
import time
import webbrowser
import easyocr
import cv2

URL = "https://humanbenchmark.com/tests/chimp"

MAX_LEVEL = 41

BLUE = np.array([43, 135, 209])

def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(1)

def start_game():
    button_location = pyautogui.locateCenterOnScreen("StartButton.png", confidence=0.9)
    pyautogui.click(button_location)
    game_size, x_border, y_border = determine_game_size()
    screenshot = np.array(pyautogui.screenshot(region=game_size))
    numbers = 0
    numbers += remember_board(screenshot)
    for level in range(4, MAX_LEVEL):
        pyautogui.click(button_location)
        positions = []
        screenshot = np.array(pyautogui.screenshot(region=game_size))
        for i in range(1, numbers+1):
            x, y, width, height = pyautogui.locateOnScreen(f"numbers/{i}.png", confidence=0.95)
            positions.append((x+width//2, y+height//2))
            screenshot[y-y_border-10:y-y_border+115, x-x_border-10:x-x_border+115] = BLUE
        if(remember_board(screenshot)):
            numbers+=1
            x, y, width, height = pyautogui.locateOnScreen(f"numbers/{numbers}.png", confidence=0.95)
            positions.append((x+width//2, y+height//2))
        for pos in positions:
            pyautogui.click(pos)
        

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

def remember_board(screenshot):
    new_numbers = 0
    for y in range(len(screenshot)-110):
        for x in range(len(screenshot[y])-110):
            if np.array_equal(screenshot[y][x], BLUE):
                continue
            image = screenshot[y:y+110, x:x+110]
            cv2.imwrite(f"number.png", image)
            image = cv2.imread(f"number.png", cv2.IMREAD_GRAYSCALE)
            _, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
            reader = easyocr.Reader(["en"])
            data = reader.readtext(image, allowlist="1234567890", detail=0)
            print("NEW NUMBER DETECTED:", data)
            number = screenshot[y-10:y+110, x-10:x+110]
            number = cv2.cvtColor(number, cv2.COLOR_RGB2BGR)
            new_numbers+=1
            try:
                cv2.imwrite(f"numbers/{data[0]}.png", number)
            except:
                cv2.imwrite(f"numbers/7.png", number)
            screenshot[y-10:y+110, x-10:x+110] = BLUE
    print("BOARD REMEMBERED")
    return new_numbers

open_human_benchmark()
start_game()