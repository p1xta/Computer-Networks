import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

def parse_page():
    products = driver.find_elements(By.CLASS_NAME, 'ListingItem__description')
    data = []

    for product in products:
        name = product.find_element(By.CLASS_NAME, 'ListingItemTitle__link').text
        year = product.find_element(By.CLASS_NAME, 'ListingItem__year').text
        kmage = product.find_element(By.CLASS_NAME, 'ListingItem__kmAge').text

        summary = product.find_element(By.CLASS_NAME, 'ListingItem__techSummary')

        tags = [elem.text for elem in summary.find_elements(By.CLASS_NAME, 'ListingItemTechSummaryDesktop__cell')]
        first_col = tags[0].split('/')
        first_col = [elem.strip('\u2009') for elem in first_col]
        try:
            price = product.find_element(By.CLASS_NAME, 'ListingItemPrice__content').text
        except:
            price_element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ListingItemPrice__link span")))
            price = price_element.text
        if (name and year and kmage and summary):
            data.append({
                'Name' : name,
                'Price' : price,
                'Year' : year,
                'Milage' : kmage,
                'Engine capacity' : first_col[0],
                'Horse powers' : first_col[1][:-5],
                'Fuel type' : first_col[2],
                'Transmission' : tags[1],
                'Car type' : tags[2],
                'Drive' : tags[3],
                'Color' : tags[4]
            })
    return data

def switch_to_next_page():
    try:
        # next_button = WebDriverWait(driver, 10).until(driver.find_element(By.CLASS_NAME, "ListingPagination__next"))
        next_button = driver.find_element(By.CLASS_NAME, 'ListingPagination__next')
        # ActionChains(driver).scroll_to_element(next_button).perform()
        next_button.click()
        time.sleep(3)
        return True
    except:
        print("No more pages")
        return False

page_number = 0
all_data = []



URL = 'https://auto.ru/novosibirsk/cars/toyota/all/'
driver.get(URL)

time.sleep(3)
answ = 'Y'

while True:
    if (answ == 'Y'):
        print(f"Parsing page {page_number+1}...")
        page_data = parse_page()
        all_data.extend(page_data)
        if not switch_to_next_page():
            break
        page_number += 1
    else:
        print(f'Parsed {page_number} pages.')
        break
    if page_number % 5 == 0:
        print("Do you want to keep parsing?(Y/n)")
        answ = input()

df = pd.DataFrame(all_data)
df.to_csv('parsed_site.csv', index=False)
print("Data saved to parsed_site.csv")

driver.quit()