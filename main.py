import pandas as pd
import scraper_gastrojobs
import scraper_hotelcareer
import scraper_stepstone
import os

completed = 0

while completed == 0:
    results_DE = scraper_gastrojobs.main("Deutschland")
    results_AT = scraper_gastrojobs.main("Österreich")
    results = pd.concat((pd.read_csv(f) for f in [results_DE, results_AT]), ignore_index=True)
    filename = results_DE.split("_", maxsplit = 1)[1]
    results.to_csv(filename, index = False)
    (os.remove(f) for f in [results_DE, results_AT])

    results_DE = scraper_hotelcareer.main("Deutschland")
    results_AT = scraper_hotelcareer.main("Österreich")
    results = pd.concat((pd.read_csv(f) for f in [results_DE, results_AT]), ignore_index=True)
    filename = results_DE.split("_", maxsplit = 1)[1]
    results.to_csv(filename, index = False)
    (os.remove(f) for f in [results_DE, results_AT])

    results_DE = scraper_stepstone.main("Deutschland")
    results_AT = scraper_stepstone.main("Österreich")
    results = pd.concat((pd.read_csv(f) for f in [results_DE, results_AT]), ignore_index=True)
    filename = results_DE.split("_", maxsplit = 1)[1]
    results.to_csv(filename, index = False)
    (os.remove(f) for f in [results_DE, results_AT])
    completed = 1