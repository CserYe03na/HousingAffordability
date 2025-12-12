import pandas as pd
import requests
from io import StringIO

def parse_puf_by_layout(layout_csv, url_txt_template, url_dat_template, output_file):
    """
    Generic PUF parser for both occupied and vacant files.
    Reads the layout CSV, determines colspecs, downloads files,
    parses fixed-width records, and outputs combined CSV.
    """

    layout_full = pd.read_csv(layout_csv)
    layout_full["year"] = layout_full["year"].astype(str).str.zfill(2)
    YEARS = sorted(layout_full["year"].unique())
    print(f"\nUsing layout file: {layout_csv}")
    print("Found years:", YEARS)

    def get_puf_url(year: str) -> str:
        # Years 11, 14, 17 use .txt; others use .dat (same rule as occupied)
        if year in ("11", "14", "17"):
            return url_txt_template.format(year)
        else:
            return url_dat_template.format(year)

    def parse_one_year(year: str):
        print(f"\n--- Processing year {year} ---")

        # Filter layout
        layout = layout_full[layout_full["year"] == year].sort_values("start")

        # Build colspecs: [start-1, end)
        colspecs = [(s - 1, e) for s, e in zip(layout["start"], layout["end"])]
        names = layout["variable"].tolist()

        # Download data file
        url = get_puf_url(year)
        print("Downloading:", url)
        r = requests.get(url)
        if r.status_code != 200:
            print(f"Failed to download {url}")
            return None
        text_raw = r.text

        # Parse fixed-width text
        df = pd.read_fwf(
            StringIO(text_raw),
            colspecs=colspecs,
            names=names,
            dtype=str,
            header=None
        )

        # Expand 2-digit year → 4-digit year
        yr_int = int(year)
        if yr_int >= 90:   # 91, 93, 96, etc.
            full_year = int("19" + year)
        else:
            full_year = int("20" + year)
        df["year"] = full_year

        # Convert FW implied decimal
        if "FW" in df.columns:
            df["FW"] = pd.to_numeric(df["FW"], errors="coerce") / 1e5

        print(f"Parsed {len(df)} rows for year {full_year}")
        if "BORO" in df.columns:
            print("Sample BORO values:", df["BORO"].dropna().unique()[:10])

        return df

    # Process all years
    dfs = []
    for y in YEARS:
        df_y = parse_one_year(y)
        if df_y is not None:
            dfs.append(df_y)

    final = pd.concat(dfs, ignore_index=True)
    final.to_csv(output_file, index=False)
    print(f"\nSaved structured PUF to: {output_file}\n")

    return final



occupied_all = parse_puf_by_layout(
    layout_csv="/Users/serenacyn03/HousingAffordability/data_raw/occupied_layout.csv",
    url_txt_template="https://www.nyc.gov/assets/hpd/downloads/misc/research/occupied_puf_{}.txt",
    url_dat_template="https://www.nyc.gov/assets/hpd/downloads/misc/research/occupied_puf_{}.dat",
    output_file="/Users/serenacyn03/HousingAffordability/data_raw/occupied_all_years.csv"
)

vacant_all = parse_puf_by_layout(
    layout_csv="/Users/serenacyn03/HousingAffordability/data_raw/vacant_layout.csv",
    url_txt_template="https://www.nyc.gov/assets/hpd/downloads/misc/research/vacant_puf_{}.txt",
    url_dat_template="https://www.nyc.gov/assets/hpd/downloads/misc/research/vacant_puf_{}.dat",
    output_file="/Users/serenacyn03/HousingAffordability/data_raw/vacant_all_years.csv"
)
