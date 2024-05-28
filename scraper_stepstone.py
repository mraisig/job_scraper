"""Scraper for hotelcareer"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Set up parameters for file export
scraping_date = time.strftime('%d_%m_%Y')
location = "Deutschland"
if location == "Deutschland":
    country = "DE"
elif location == "Österreich":
    country = "AT"


# Initialize a fake user agent so scraping is harder to detect
options = Options()
ua = UserAgent()
a = ua.random
user_agent = ua.random
print(user_agent)
options.add_argument(f"user-agent={user_agent}")


# Initialize WebDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)

driver.maximize_window()
driver.get("https://www.stepstone.de")  # Specify URL to scrape
wait = WebDriverWait(driver, 30)

# Accept cookies
try:
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[11]/section/div/section/div[2]/div[1]/div[2]/div/div"))
    ).click()
    print("Clicked successfully")
except NoSuchElementException:
    print("Could not click")
    pass

input_ort = driver.find_element(By.ID, "stepstone-autocomplete-155")
input_ort.send_keys(location + Keys.ENTER)

job_title = []
company_info = []
location = []
date = []
home_office = []
snippet = []
id = []
page = 1

while True:
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all("article", {"data-at": "job-item"})
    for result in results:
        job_title.append(result.find("a", {"data-at": "job-item-title"}).get_text().strip())
        company_info.append(result.find("span", {"data-at" : "job-item-company-name"}).get_text().strip())
        location.append(result.find("span", {"data-at": "job-item-location"}).get_text().strip())
        date.append(result.find("time")['datetime'])
        if result.find("div", {"data-at": "jobcard-content"}):
            snippet.append(result.find("div", {"data-at": "jobcard-content"}).get_text().strip())
        else:
            snippet.append("")
        id.append(result['id'])
        if result.find("span", {"data-at": "job-item-work-from-home"}):
            home_office.append(1)
        else:
            home_office.append(0)
    if (
        len(driver.find_elements(By.XPATH, "/html/body/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/nav/ul/li[9]/a")) > 0
    ):  # run loop until there are no more pages left
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div[1]/div/div[3]/div/div[2]/div[3]/nav/ul/li[9]/a"))).click()
            print(f"Clicked successfully to: {page+1}")
            page += 1
        except TimeoutException:
            break
    else:
        break

df = pd.DataFrame(
    {
        "job_title": job_title,
        "company_info": company_info,
        "location": location,
        "date": date,
        "snippet" : snippet,
        "home_office": home_office,
        "id" : id,
        "country" : country,
    }
)

filename_output = country + "_" + "stepstone" + "_" + scraping_date

df.to_csv(filename_output + ".csv", index=False)