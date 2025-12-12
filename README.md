## Project Overview
This project studies housing vacancy and affordability in New York City using data from the NYC Department of Housing Preservation and Development (NYCHVS). The dataset covers the period from 1991 to 2023 and includes information on occupancy status, rent, mortgage payments, household demographic information, and housing characteristics.

We analyze vacancy patterns across years and boroughs, investigate reported reasons for vacancy, and explore the structural characteristics of vacant units using tools such as weighted vacancy rates and principal component analysis. Our findings suggest that most vacant units are unavailable due to renovations, seasonal use, or structural and legal constraints, rather than intentional withholding from the rental market.

In addition, we examine housing affordability across income and demographic groups. The analysis focuses on rent levels, income, housing burden, and rent-income ratios for renters and owners with mortgages. Results show that rent growth has consistently outpaced income growth since the early 1990s, leaving low and middle income renters especially vulnerable, even in an extremely tight housing market. 

In general, this project finds that New York City's housing challenges are driven less by excess vacancy and more by long-term structural constraints, limited rental supply, and a persistent mismatch between rent growth and income growth.

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

