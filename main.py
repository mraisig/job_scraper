import pandas as pd
import scraper_gastrojobs
import scraper_hotelcareer
import scraper_stepstone
import os

completed = 0

while completed == 0:
    print("Scraping started for gastrojobs...")
    results_DE = scraper_gastrojobs.main("Deutschland")
    results_AT = scraper_gastrojobs.main("Österreich")
    results = pd.concat((pd.read_csv(f) for f in [results_DE, results_AT]), ignore_index=True)
    filename = results_DE.split("_", maxsplit = 1)[1]
    results.to_csv(filename, index = False)
    (os.remove(f) for f in [results_DE, results_AT])
    print("Scraping completed for gastrojobs.")

    print("Scraping started for hotelcareer...")
    results_DE = scraper_hotelcareer.main("Deutschland")
    results_AT = scraper_hotelcareer.main("Österreich")
    results = pd.concat((pd.read_csv(f) for f in [results_DE, results_AT]), ignore_index=True)
    filename = results_DE.split("_", maxsplit = 1)[1]
    results.to_csv(filename, index = False)
    (os.remove(f) for f in [results_DE, results_AT])
    print("Scraping completed for hotelcareer.")

    print("Scraping started for stepstone...")
    results_DE = scraper_stepstone.main("Deutschland")
    results_AT = scraper_stepstone.main("Österreich")
    results = pd.concat((pd.read_csv(f) for f in [results_DE, results_AT]), ignore_index=True)
    filename = results_DE.split("_", maxsplit = 1)[1]
    results.to_csv(filename, index = False)
    (os.remove(f) for f in [results_DE, results_AT])
    print("Scraping completed for stepstone.")
    completed = 1