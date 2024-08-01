"""Scraper for hotelcareer"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import chromedriver_autoinstaller

def main(location_input):
    # Check if the current version of chromedriver exists and if it doesn't exist, download it automatically, then add chromedriver to path
    chromedriver_autoinstaller.install(cwd = True)

    # Set up parameters for file export
    portal = "hotelcareer"
    scraping_date = time.strftime('%d_%m_%Y')
    location_input = location_input
    if location_input == "Deutschland":
        country = "DE"
    elif location_input == "Österreich":
        country = "AT"


    # Initialize a fake user agent so scraping is harder to detect
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless=new")

    # Initialize WebDriver
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    driver.maximize_window()
    driver.get("https://www.hotelcareer.de")  # Specify URL to scrape
    wait = WebDriverWait(driver, 60)

    # Accept cookies
    try:
        wait.until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[starts-with(@id,'sp_message_iframe')]")
            )
        )
        element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Zustimmen']"))
        )
        driver.execute_script("arguments[0].click();", element)
        print("Clicked successfully")
    except NoSuchElementException:
        print("Could not click")
        pass

    time.sleep(10)

    # Set location
    # Does not work starting from 19.6.2024
    #input_ort = driver.find_element(By.ID, "input_ort")
    #input_ort.send_keys(location + Keys.ENTER)

    driver.execute_script(("document.getElementById('input_ort').value=arguments[0]"), location_input)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnSearch_new']"))).click()


    # Close pop-up
    try:
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Close']"))
        ).click()
        print("Clicked successfully")
    except NoSuchElementException:
        print("Could not click")
        pass

    hits = driver.find_element(By.XPATH, "//*[@id='Results_list']/p/span")
    print("Number of results:", hits.text)

    time.sleep(10)

    job_title = []
    company_info = []
    location = []
    job_type = []
    date = []
    snippet = []
    id = []
    page = 1

    # Start scraping each available page and writing results in lists
    while True:
        time.sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        results = soup.find_all("li", {"class": "clearfix"})
        for result in results:
            job_title.append(result.find("a", {"class": "job"}).get_text().strip())
            company_info.append(result.find("div", {"company_info"}).get_text().strip())
            location.append(result.find("li", {"class": "location"}).get_text().strip())
            job_type.append(result.find("li", {"class": "info"}).get_text().strip())
            date.append(result.find("li", {"class": "date"}).get_text().strip())
            if result.find("div", {"class": "snippet"}):
                snippet.append(result.find("div", {"class": "snippet"}).get_text().strip())
            else:
                snippet.append("")
            id.append(result['ang'])
        if (
            len(driver.find_elements(By.CLASS_NAME, "weiter")) > 0
        ):  # run loop until there are no more pages left
            try:
                element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "weiter")))
                driver.execute_script("arguments[0].click();", element)
                print(f"Clicked successfully to: {page+1}")
                page += 1
            except TimeoutException:
                print("Reached last page")
                break
        else:
            break

    # Creating dataframe containing all lists
    df = pd.DataFrame(
        {
            "job_title": job_title,
            "company_info": company_info,
            "location": location,
            "job_type": job_type,
            "date": date,
            "snippet" : snippet,
            "id" : id, 
            "country": country,
            "portal" : portal
        }
    )

    filename_output = country + "_" + portal + "_" + scraping_date

    df.to_csv(filename_output + ".csv", index=False)
    return filename_output + ".csv"

if __name__ == "__main__":
    main()
