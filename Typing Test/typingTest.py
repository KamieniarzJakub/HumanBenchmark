import pyautogui
import numpy as np
import time
import webbrowser
import cv2
import easyocr
import pytesseract

URL = "https://humanbenchmark.com/tests/typing"

TEXT_BACKGROUND_COLOR = np.array([234, 243, 250])

def open_human_benchmark():
    webbrowser.open(URL, 1, True)
    time.sleep(3)

def start_game():
    game_size = determine_text_position()
    pyautogui.write(detect_text(game_size))
        
def determine_text_position():
    screenWidth, screenHeight = pyautogui.size()
    y_lower_border = -1
    y_upper_border = screenHeight
    screenshot = np.array(pyautogui.screenshot())
    for y in range(screenHeight):
        if np.array_equal(screenshot[y][screenWidth//2], TEXT_BACKGROUND_COLOR):
            if y_lower_border < 0:
                y_lower_border = y
            else:
                y_upper_border = y
    x_lower_border = -1
    x_upper_border = screenWidth
    for x in range(screenWidth):
        if np.array_equal(screenshot[(y_upper_border+y_lower_border)//2][x], TEXT_BACKGROUND_COLOR):
            if x_lower_border < 0:
                x_lower_border = x
            else:
                x_upper_border = x
    text_width =  x_upper_border-x_lower_border
    text_height = y_upper_border-y_lower_border
    return (x_lower_border, y_lower_border+int(0.05*text_height),text_width, int(0.9*text_height))


def detect_text(game_size):
    time.sleep(0.01)
    screenshot_path = "text.png"
    image = pyautogui.screenshot(screenshot_path, region=game_size)

    # Convert to OpenCV format
    image = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding to improve contrast
    _, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)

    # Save processed image for debugging
    cv2.imwrite(f"processed_text.png", image)

    #reader = easyocr.Reader(['en'])
    #data = reader.readtext(image)
    #print(data)
    #text = ""
    #for x in data:
    #    text+=x[1]
    #    text+=" "
    #text+= "."*10

    pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
    data = pytesseract.image_to_string(image, lang='eng', config='--psm 6')

    text = ""
    for i in range(len(data)):
        if len(text)==0 and data[i].isalnum():
            text+=data[i]
            continue
        elif ord(data[i])!=10:
            text+=data[i]
        else:
            text+=" "
    print(text)
    return text[:-1]

open_human_benchmark()
start_game()