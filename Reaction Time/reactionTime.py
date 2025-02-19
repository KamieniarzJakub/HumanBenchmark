import pyautogui
import numpy as np
import time
import webbrowser

URL = "https://humanbenchmark.com/tests/reactiontime"

RED = (206, 38, 54)

def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(1)


def detect_green():
    screenWidth, screenHeight = pyautogui.size()
    x = screenWidth//2
    y = screenHeight//2
    
    for i in range(5):
        pyautogui.click(x, y)
        time.sleep(0.1)
        while True:
            if not pyautogui.pixelMatchesColor(x, y, RED):
                break
        pyautogui.click(x, y)

open_human_benchmark()
detect_green()