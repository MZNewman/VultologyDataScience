from selenium import webdriver
from selenium.webdriver.common.by import By
from math import floor
from time import sleep
import re

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://vultology.com/list-of-terms/")
sleep(10)
num_samples = int(re.search(r'\d+', driver.find_element(by=By.ID, value="code_block-8-2008").text).group())

driver.get("https://vultology.com/database/?type=&development=")
urls_per_page = []
sleep(10)
wrappers = driver.find_elements(by=By.CLASS_NAME, value="bxcard-wrapper")
for wrapper in wrappers:
    url = wrapper.get_attribute("href")
    urls_per_page.append(url)
per_page = len(urls_per_page)

for _ in range(floor(num_samples/per_page)):
    load_more = driver.find_element(by=By.ID, value="load-more-btn")
    load_more.click()
    sleep(10)

url_list = []
wrappers = driver.find_elements(by=By.CLASS_NAME, value="bxcard-wrapper")
for wrapper in wrappers:
    url = wrapper.get_attribute("href")
    url_list.append(url)

#"https://vultology.com/metabolism-pt2-ti-platonism-fi-animism/"
#for that element of the list, take it and everything after it out
#because it's the end of the database proper

idx = url_list.index("https://vultology.com/metabolism-pt2-ti-platonism-fi-animism/")
with open("DBLinks.txt", "w") as file:
    for url in url_list[:idx]:
        file.write(url + "\n")
