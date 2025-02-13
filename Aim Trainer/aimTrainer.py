import pyautogui
import numpy as np
import time
import webbrowser

URL = "https://humanbenchmark.com/tests/aim"

TARGETS = 31

def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(3)

def click_on_targets():
    for i in range(TARGETS):
        pyautogui.click(pyautogui.locateCenterOnScreen("target.png", confidence=0.4))


open_human_benchmark()
click_on_targets()