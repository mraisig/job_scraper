# Job Scraper
This repository contains scripts, that will scrape the job postings available on the platforms [Stepstone](stepstone.de), [GastroJobs](gastrojobs.de) and [HotelCareer](hotelcareer.de). The retrieved data will be stored in tables and can be used for future analysis.

# Installation
## Step 1: Clone the repository
1. If not already installed, first [install](https://git-scm.com/download/win) git on your local machine.
2. Open the command prompt or terminal in your IDE
3. Navigate to the directory where you want to clone the repository using the ```cd``` command.
4. Run the following command: \
```git clone https://github.com/mraisig/job_scraper.git```

The repository will now be cloned to your local machine into the current folder.

## Step 2: Create environment
1. If not already installed, download and install a distribution of conda or mamba.
2. Run the following command to create a new conda environment: \
```conda env create -f environment.yml```
3. Activate the newly created environment: \
```conda activate job_scraper```

# Usage
Currently you have to run the scrapers seperately for each platform and each country.
1. Specify the location in each script by setting the ```location``` variable to `` "Deutschland" `` or `` "Österreich" ``.
2. Run the file using the command line (e.g for Gastrojobs): \
    ```python scraper_gastrojobs.py```

    


