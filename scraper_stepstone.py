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
import chromedriver_autoinstaller


def main(location_input):
    # Check if the current version of chromedriver exists and if it doesn't exist, download it automatically, then add chromedriver to path
    chromedriver_autoinstaller.install(cwd=True)

    # Set up parameters for file export
    portal = "stepstone"
    scraping_date = time.strftime("%d_%m_%Y")
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
    driver.get("https://www.stepstone.de")  # Specify URL to scrape
    wait = WebDriverWait(driver, 30)

    # Accept cookies
    try:
        element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Alles akzeptieren']"))
        )
        driver.execute_script("arguments[0].click();", element)
        print("Clicked successfully")
    except NoSuchElementException:
        print("Could not click")
        pass

    input_ort = driver.find_element(By.ID, "stepstone-autocomplete-155")
    input_ort.send_keys(location_input + Keys.ENTER)

    job_title = []
    company_info = []
    location = []
    date = []
    home_office = []
    snippet = []
    id = []
    page = 1
    max_page = int(driver.find_element(By.CSS_SELECTOR, "li.res-1b3es54:nth-child(8) > a:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)").text)
    while True:
        time.sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        results = soup.find_all("article", {"data-at": "job-item"})
        for result in results:
            job_title.append(
                result.find("a", {"data-at": "job-item-title"}).get_text().strip()
            )
            company_info.append(
                result.find("span", {"data-at": "job-item-company-name"})
                .get_text()
                .strip()
            )
            location.append(
                result.find("span", {"data-at": "job-item-location"}).get_text().strip()
            )
            if result.find("time")["datetime"]:
                date.append(result.find("time")["datetime"])
            else:
                date.append("")
            if result.find("div", {"data-at": "jobcard-content"}):
                snippet.append(
                    result.find("div", {"data-at": "jobcard-content"})
                    .get_text()
                    .strip()
                )
            else:
                snippet.append("")
            id.append(result["id"])
            if result.find("span", {"data-at": "job-item-work-from-home"}):
                home_office.append(1)
            else:
                home_office.append(0)
        if page <= max_page:  # run loop until there are no more pages left
            try:
                element = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "[aria-label='Nächste']")
                    )
                )
                driver.execute_script("arguments[0].click();", element)
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
            "snippet": snippet,
            "home_office": home_office,
            "id": id,
            "country": country,
            "portal": portal,
        }
    )

    filename_output = country + "_" + portal + "_" + scraping_date

    df.to_csv(filename_output + ".csv", index=False)

    return filename_output + ".csv"


if __name__ == "__main__":
    main()
