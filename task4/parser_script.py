import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def parse_page(driver, url):
    driver.get(url)
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
        if (name and year and kmage and summary):
            data.append({
                'name' : name,
                'price' : price,
                'year' : year,
                'mileage' : kmage,
                'engine_capacity' : first_col[0],
                'horse_powers' : first_col[1][:-5],
                'fuel_type' : first_col[2],
                'transmission' : tags[1],
                'car_type' : tags[2],
                'drive' : tags[3],
                'color' : tags[4]
            })
    return data

def switch_to_next_page(driver, url, page_number):
    try:
        next_button = driver.find_element(By.CLASS_NAME, 'ListingPagination__next')
        next_button.click()
        return True
    except:
        print("No more pages")
        return False

def parse_3_pages(url):
    driver = webdriver.Chrome()
    page_number = 1
    all_data = []
    url = url + "?page=1"
    while page_number <= 3:
        print(f"Parsing page {page_number}...")
        page_data = parse_page(driver, url)
        all_data.extend(page_data)      
        url = url[:-1] + str(page_number+1)
        
        page_number += 1
        time.sleep(3)

    driver.quit()
    return all_data

# URL = 'https://auto.ru/novosibirsk/cars/toyota/all/'
