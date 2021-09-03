# Load selenium components
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import pandas as pd
import threading


data = pd.read_csv('content.csv', sep=';')
url_list = data['url'].values
price_list = data['price'].values
result = {}
def parse_link(url_link, price_class):
    global result

    print(url_link)
    # Establish chrome driver and go to report site URL
    url = url_link
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)

    driver.find_element_by_css_selector(
        '.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary').click()

    dropList = Select(driver.find_element_by_css_selector(
        '.MuiNativeSelect-root-178.MuiNativeSelect-select-179.MuiInputBase-input-207.MuiInput-input-195.MuiInputBase-inputMarginDense-208.MuiInput-inputMarginDense-196'))

    dropList.select_by_value('3')

    price = driver.find_elements_by_class_name(price_class)
    name = driver.find_elements_by_class_name('card-title.h5')

    if float(price[0].get_attribute("innerText").split()[0]) * 2 <= float(price[1].get_attribute("innerText").split()[0]):
        if url_link not in result:
            result[url_link] = [name[0].get_attribute("innerText")]
        else:
            result[url_link].append(name[0].get_attribute("innerText"))

    # for i, j in zip(price, name):
    #     print(i.get_attribute("innerText"), j.get_attribute("innerText"))
    #     if url_link not in result:
    #         result[url_link] = [j.get_attribute("innerText")]
    #     else:
    #         result[url_link].append(j.get_attribute("innerText"))


threads = []

for u, p in zip(url_list, price_list):
    t = threading.Thread(target=parse_link, args=[u, p])
    t.daemon = True
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print(result)
print(len(result))