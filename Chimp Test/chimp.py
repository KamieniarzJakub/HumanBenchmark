import pyautogui
import numpy as np
import time
import webbrowser
import imgkit

URL = "https://humanbenchmark.com/tests/chimp"

MAX_LEVEL = 41

def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(1)

def start_game():
    #generate_numbers()
    button_location = pyautogui.locateCenterOnScreen("StartButton.png", confidence=0.9)
    for level in range(3, MAX_LEVEL):
        time.sleep(1)
        pyautogui.click(button_location)
        pyautogui.screenshot(f"level {level}.png")
        
        for x in remember_board():
            time.sleep(0.5)
            pyautogui.click(x)
        
def generate_numbers():
    html_code = """
        <html>
        <head>
            <style>
            body {
            margin: 0;
            }
            div {
                width: 80px;
                height: 80px;
                background-color: #3498db;
                color: white;
                font-size: 65px;
                text-align: center;
                line-height: 80px;
                font-family: Helvetica, Arial, sans-serif;
                padding: 0;
                font-weight: 400;
                outline: 0;
                margin: 0;
                box-sizing: border-box;
            }
            </style>
        </head>
        <body>
            <div>1</div>
        </body>
        </html>
        """
    for i in range(1, MAX_LEVEL):
        f = open("number.html", "w")
        f.write(html_code.replace("<div>1</div>", f"<div>{i}</div>"))
        f.close()
        options = {
            "width": 80,
            "height": 80,
        }
        config = imgkit.config(wkhtmltoimage=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe")
        imgkit.from_file(filename="number.html", output_path=f"{i}.png", config=config, options=options)

        
def remember_board():
    positions = []
    for i in range(1, MAX_LEVEL):
        try:
            positions.append(pyautogui.locateCenterOnScreen(f"{i}.png", confidence=0.9))
        except:
            break
    return positions

open_human_benchmark()
start_game()