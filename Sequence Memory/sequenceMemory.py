import pyautogui
import numpy as np
import time
import webbrowser

URL = "https://humanbenchmark.com/tests/sequence"

def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(3)

def remember_sequence(max_level):
    button_location = pyautogui.locateCenterOnScreen("StartButton.png", confidence=0.9)
    pyautogui.click(button_location)
    for level in range(max_level):
        play_level(level+1)
        time.sleep(0.75)
    
    
def play_level(level):
    memory = []
    while len(memory)!=level:
        try:
            x = pyautogui.locateCenterOnScreen("SequenceButton.png", confidence=0.9)
            if len(memory)==0 or x!=memory[-1]:
                memory.append(x)
        except:
            pass

    #print(memory)
    time.sleep(1)
    for i in range(level):
        pyautogui.click(memory[i].x, memory[i].y)
        time.sleep(0.1)
        
        
        

open_human_benchmark()
remember_sequence(max_level=250)