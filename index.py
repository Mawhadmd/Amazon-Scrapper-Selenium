from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True) 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
searchquery = "pc"
# with open(f'{searchquery}.json','r') as a:
#     file = json.load(a)
file = []
# if file == "":
with open(f'{searchquery}.json', 'w') as w:
        json.dump([],w,indent=2)
    
html = driver.get(f'https://www.amazon.ae/s?k={searchquery}')


def login():
    e = driver.find_element(By.CSS_SELECTOR,'input#e')
    e.click()
    e.send_keys(f'{searchquery}')

    f = driver.find_element(By.CSS_SELECTOR,'input#f')
    f.click()

html = driver.find_element(By.XPATH, "//div[contains(@class, 's-main-slot s-result-list s-search-results sg-row')]")

i = 2
while True:
    maincompartment = abc= WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.XPATH,"//div[contains(@class, 'puisg-col-inner')]/div[contains(@class, 'a-section a-spacing-small a-spacing-top-small') and div[contains(@data-cy, 'title-recipe')]]")))
    for m in maincompartment:  
        name = ""
        available = False
        price = ""
        href = ""
        rating = ""
        stock = ""

        try:
            price_element = m.find_element(By.XPATH, ".//span[contains(@class,'a-price-whole')]")
            price = price_element.text
            available = True
        except:
            available = False
            
        try:
            name_element = m.find_element(By.XPATH, ".//h2[contains(@class,'a-size-mini a-spacing-none a-color-base s-line-clamp-2')]")
            name = name_element.text
        except:
            name = "Name not found"

        try:
            href_element = m.find_element(By.XPATH, ".//a[contains(@class,'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')]")
            href = href_element.get_attribute('href')
        except:
            href = "Href not found"

        try:
            rating_element = m.find_element(By.XPATH, ".//a[contains(@class,'a-popover-trigger a-declarative')]")
            rating = rating_element.text
        except:
            rating = "Rating not found"

        try:
            stock_element = m.find_element(By.XPATH, ".//span[contains(@class,'a-size-base a-color-price')]")
            stock = stock_element.text
        except:
            stock = "Not specified"
            
        file.append({
            'name': name,
            'rating': rating,
            'price': price,
            'stock': stock,
            'available': str(available),
            'href': href
        })
    try:
        abc= WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,f"//a[contains(@aria-label,'Go to page {i}')]")))
        abc.click()
        i+=1
    except:
        break



    
with open(f'{searchquery}.json','w') as a:
    json.dump(file,a,indent=2)