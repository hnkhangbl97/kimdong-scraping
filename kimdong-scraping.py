from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd

import logging

#Set up the input website
url ='https://nxbkimdong.com.vn/collections/doraemon-2/'

#Connect to Kimdong publisher website
driver = webdriver.Chrome()
driver.get(url)

#Initialize
title= list()
current_price = list()
original_price = list()

logging.basicConfig(level= logging.DEBUG)

#Scarping data 


pagination_div = driver.find_element(By.XPATH,"//div[@class='pagination-custom']")
pages = pagination_div.find_elements(By.TAG_NAME,'span')


page_cnt = int(pages[-2].text)

logging.info("Start Scraping...")
for page in range(0,page_cnt):
    
    driver.implicitly_wait(5)

    current_page = int(driver.find_element(By.XPATH,"//span[@class='page page-node current']").text)
    product_list = driver.find_elements(By.XPATH,"//div[contains(@class,'product-list')]//div[contains(@class,'product-item')]")

    for item in product_list:
        title.append(item.find_element(By.XPATH,".//div[@class='product-title']/a").text)
        current_price.append(item.find_element(By.XPATH,".//div[contains(@class,'product-price')]/span[contains(@class,'current-price')]").text)
        original_price.append(item.find_element(By.XPATH,".//div[contains(@class,'product-price')]/span[contains(@class,'original-price')]").text)
    if current_page == page_cnt:
       break 
    else:
        next_page_btn = driver.find_element(By.XPATH,"//span[@class='nextPage']")
        next_page_btn.click()
        logging.info("Scraping next page...")

logging.info("Scraping was done, saving data to csv file")
#Save data to csv file
df = pd.DataFrame({
    'title': title,
    'original_price': original_price,
    'current_price': current_price
})

df.to_csv('kimdong_doraemon_collections_data.csv',index = False)

logging.info('Scraped data saved successfully!')
#Finalization
driver.quit()
