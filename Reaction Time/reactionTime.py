import pyautogui
import numpy as np
import time
import webbrowser

URL = "https://humanbenchmark.com/tests/reactiontime"

RED = np.array([206, 38, 54])

screenWidth, screenHeight = pyautogui.size()

def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(1)


def detect_green():
    pyautogui.click(screenWidth/2, screenHeight/2)
    
    for i in range(5):
        while True:
            screenshot = np.array(pyautogui.screenshot())
            if not np.array_equal(screenshot[screenHeight//2][screenWidth//2], RED):
                #print(screenshot[screenHeight//2][screenWidth//2])
                break
        pyautogui.click(screenWidth/2, screenHeight/2)
        time.sleep(0.1)
        pyautogui.click(screenWidth/2, screenHeight/2)

open_human_benchmark()
detect_green()