import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

def parse_page():
    time.sleep(3)
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
            price_element = driver.find_element(By.CSS_SELECTOR, ".ListingItemPrice__link span")
            price = price_element.text
        if name and year and kmage and summary:
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
        next_button = driver.find_element(By.CLASS_NAME, 'ListingPagination__next')
        next_button.click()
        
        return True
    except:
        print("No more pages")
        return False

URL = 'https://auto.ru/novosibirsk/cars/toyota/all/'
driver.get(URL)

time.sleep(3)
page_number = 0
all_data = []
answer = 'Y'

while True:
    if (answer == 'Y'):
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
        answer = input()

df = pd.DataFrame(all_data)
df.to_csv('parsed_site.csv', index=False)
print("Data saved to parsed_site.csv")

driver.quit()