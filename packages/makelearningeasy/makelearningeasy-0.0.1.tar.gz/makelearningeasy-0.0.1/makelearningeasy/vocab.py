"""
vocab
"""

from selenium import webdriver
from IPython.display import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
