import time
import os
#   Install the selenium package in the virtual environment.
#   Its always a good practice to only import the required function rather than the entire library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

#   To resolve certificate error
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#   The chrome driver (in selenium) establishes a connection between your python script and chrome browser.
s = Service('chromedriver.exe')

# Instantiate the webdriver
driver = webdriver.Chrome(service=s, options=options)

# The base URL for the pages to scrape
page_URL = "https://codeforces.com/problemset/page/"

DATA_FOLDER = "Problemdata"

def add_text_to_index_file(text):
    index_file_path = os.path.join(DATA_FOLDER, "index.txt")
    with open(index_file_path, "a") as index_file:
        index_file.write(text + "\n")

def get_all_anchor_tags(url):
    # Load the URL in the browser
    driver.get(url)
    # Wait for 7 seconds to ensure the page is fully loaded
    time.sleep(7)
    # Find all the a elements on the page
    links = driver.find_elements(By.TAG_NAME, "a")
    headers = driver.find_elements(By.CSS_SELECTOR, "tr td.dark div:nth-child(1) a")
    ans = []
    #   links contain all the anchor tags of the page. We only need to filter out the achor tags of problem names.
    #   Those a tags are of the form ....com/problems/problem-name/

    for i in headers:
        try:
            add_text_to_index_file(i.text)
        except:
            pass

    for i in links:
        try:
            # Check if '/problems/' is in the href of the 'a' element
            if "/problemset/problem/" in i.get_attribute("href"):
                # If it is, append it to the list of links
                ans.append(i.get_attribute("href"))
        except:
            #   for some tage there may not be a href attribute so those give a error - Reason for except block
            pass
    
    # Remove duplicate links using set
    ans = list(set(ans))
    return ans


# Iterate over all pages and store in a list;
problem_links = []
for i in range(1, 89):
    problem_links += (get_all_anchor_tags(page_URL+str(i)))


#Store them in a set to remove duplicates
problem_links = list(set(problem_links))

with open('problemLinks.txt', 'a') as f:#   'a' specifies that we want data to append data to the end of file
    for j in problem_links:
        f.write(j+'\n')#    Dont forget to add newline at the end.


#   Quits the driver and closes the browser
driver.quit()
