from bs4 import BeautifulSoup
import re
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

S = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=S)
form_url = "https://forms.gle/ZGeC7FdPL4f78pQeA"
headers={
    "Accept-Language":"en-US,en;q=0.9",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}
zillow_url = "https://www.zillow.com/salem-ma/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22users" \
             "SearchTerm%22%3A%22Salem%2C%20MA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-71.00796490551758%2C%22east%22%3A" \
             "-70.80712109448243%2C%22south%22%3A42.463115895480165%2C%22north%22%3A42.56864179001237%7D%2C%22regionSel" \
             "ection%22%3A%5B%7B%22regionId%22%3A33821%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22fi" \
             "lterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C" \
             "%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo" \
             "%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afa" \
             "lse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%" \
             "22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%2" \
             "2%3A13%7D" \

response = requests.get(url=zillow_url, headers=headers)
data = response.text

soup = BeautifulSoup(data, "html.parser")
time.sleep(2)

for link in soup.find_all(class_="list-card"):
    print(link)
    try:
        address = link.find(class_="list-card-addr").text
    except AttributeError:
        address = "No address"
    print(address)
    try:
        price = link.find(class_="list-card-price").text
        price = re.split('_|/|!|\+|$', price)[0][1:]
    except AttributeError:
        price = "No price"
    print(price)
    try:
        link = link.find("a")["href"]
    except AttributeError:
        link = "No link"
    if "zillow" not in link:
        link = "https://www.zillow.com" + link
    driver.get(form_url)
    time.sleep(2)
    #UPDATE FORM QUESTIONS
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(address)
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(price)
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(link)
    #SUBMIT FORM
    driver.find_element(By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div").click()
    time.sleep(2)


