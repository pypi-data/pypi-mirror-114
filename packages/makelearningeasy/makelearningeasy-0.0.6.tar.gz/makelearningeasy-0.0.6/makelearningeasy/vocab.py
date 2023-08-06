"""
vocab
"""

from selenium import webdriver
from IPython.display import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from IPython.display import display, Image
import PIL.Image
from io import BytesIO
import cv2
import numpy as np
import time

def meaning(word):

    wd = webdriver.Chrome("/Users/sainagimmidisetty/Downloads/chromedriver")
    wd.maximize_window()
    wd.get("https://www.google.com/")
    meaning = WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@title='Search']")))
    meaning.send_keys(word)
     # + " " +"meaning")
    meaning.send_keys(Keys.ENTER)
    wd.save_screenshot('img/pic.png')
    return Image("img/pic.png")

def wikipedia(word):

    wd = webdriver.Chrome("/Users/sainagimmidisetty/Downloads/chromedriver")
    wd.maximize_window()
    word.replace(" ","_")
    wd.get("https://en.wikipedia.org/wiki/" + word)
    time.sleep(10)
    wd.save_screenshot('img/pic.png')
    return Image("img/pic.png")

def show_image(img, fmt='png'):
    a = np.uint8(img)
    f = BytesIO()
    PIL.Image.fromarray(a).save(f, fmt)
    display(Image(data=f.getvalue()))

def display_all_images(lower_bound,upper_bound):
    for i in range(lower_bound,upper_bound):
        img = cv2.imread("img/pic " + str(i) + ".png")
        show_image(img)
