## Project Overview


## Reproducible workflow

This repository provides a fully reproducible workflow for downloading, parsing, reconstructing, and analyzing the NYC Housing and Vacancy Survey (NYCHVS) Public Use Files (PUF) from 1991–2023.

1. Download 2021 and 2023 NYCHVS microdata (8 CSV files)

   - Visit: https://www.nyc.gov/site/hpd/about/research.page  
   
   - Under the **2023 NYCHVS Public Use Files (PUF)** and **2021 NYCHVS Public Use Files (PUF)** sections, download all four datasets for each year: 
   
     - All units (CSV)  
     - Occupied units (CSV)  
     - Person (CSV)  
     - Vacant units (CSV)  
     
   Save all eight CSV files inside the `data_raw/` folder.

2. Construct record layouts for the 1991–2017 PUF fixed-width datasets

   - In the **Public Use Files (1991–2017)** section of the same webpage, open the Record Layouts (All Datasets) for each year.
   
   - From these layouts, extract the character positions for the following variables:  
   
     - *Vacant units:* Borough, Status of Vacant Unit, Housing Unit Weight  
     
     - *Occupied units:* Borough, Housing Unit Weight, Total Household Income (Recode), Monthly Gross Rent  
     
   - Using these character positions, create two layout files:  
   
     - `data_raw/occupied_layout.csv`  
     
     - `data_raw/vacant_layout.csv`  
     
   These files define how the historical fixed-width `.txt` and `.dat` files should be parsed.

3. Run the extraction script to build the 1991–2017 datasets

   - Execute:  
     
     ```bash
     python3 scripts/extract_prev.py
     ```
   This script reads and parses each year's fixed-width PUF data based on the layout files, extracts the required variables, and outputs two consolidated datasets:
     
     - `data_raw/occupied_all_years.csv`
     
     - `data_raw/vacant_all_years.csv`
   
4. Run the full analysis and generate all visualizations.

    - Render the Quarto document:
  
      ```bash
      quarto render results.qmd
      ```
      
    This will produce all figures, analyses, and tables using both the 2021–2023 microdata and the reconstructed 1991–2017 datasets.

