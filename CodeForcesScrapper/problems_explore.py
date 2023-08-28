import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""For each of the problem link. We get the keywords present in body and heading of problem including tags."""

#   To resolve certificate error
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
s = Service('chromedriver.exe')

driver = webdriver.Chrome(service=s, options=options)

#   Check the class style of heading
heading_class = "div.header div.title"
index = 1
DATA_FOLDER = "Problemdata"


def get_array_of_links():
    links = []
# Open the file
    with open("ProblemLinks.txt", "r") as file:
        # Read each line one by one
        for line in file:
            links.append(line)
    return links


def add_text_to_index_file(text):
    index_file_path = os.path.join(DATA_FOLDER, "index.txt")
    with open(index_file_path, "a") as index_file:
        index_file.write(text + "\n")


def add_link_to_Qindex_file(text):
    index_file_path = os.path.join(DATA_FOLDER, "Qindex.txt")
    with open(index_file_path, "a", encoding="utf-8", errors="ignore") as Qindex_file:
        Qindex_file.write(text)


def getPagaData(url, index):
    try:
        driver.get(url)
        time.sleep(5)
        heading = driver.find_element(By.CSS_SELECTOR, heading_class)
        print(heading.text)
        if (heading.text):
            add_text_to_index_file(heading.text)
            add_link_to_Qindex_file(url)
        time.sleep(1)
        return True
    except Exception as e:
        print(e)
        return False


links = get_array_of_links()
for link in links:
    success = getPagaData(link, index)
    if (success):
        index = index+1


driver.quit()
