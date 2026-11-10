# DAM 11-Commodity Real Extractor

## Included
- `dam_11_commodity_extractor.py` — complete extractor + cleaner
- `common_dropdowns.json` — the DAM metadata response you captured
- `requirements.txt`

## Real commodities
The script selects these 11 DAM IDs from the captured metadata:

### Onion
- 831 — Onion (local)
- 832 — Onion-imported
- 833 — Onion (New)

### Potato
- 942 — Potato (Local) - Old
- 943 — Potato (Local)
- 944 — Potato (Holland) - White (Old)
- 945 — Potato (Holland) - White (New)
- 946 — Potato (Holland) - Red (Old)
- 947 — Potato (Holland) - Red
- 948 — Sweet Potato
- 21014 — Potatoes-imported

## Run

1. Open Command Prompt in this folder.
2. Install dependencies:

    pip install -r requirements.txt

3. Test 3 markets x 11 commodities:

    python dam_11_commodity_extractor.py --max-markets 3 --workers 2 --delay 0.6

4. Check the generated CSVs against the DAM website.

5. Run all markets:

    python dam_11_commodity_extractor.py --workers 4 --delay 0.4

## Authentication

The script will ask for your current DAM Bearer token.

Paste only the token itself, not `Bearer `.

You can instead create a text file in this folder named:

    dam_token.txt

containing only the token on one line.

Optional environment variables:
- DAM_BEARER_TOKEN
- DAM_ACCESS_USER_ID
- DAM_ACCESS_USERNAME

The token is not written into any output file.

## Outputs

    dam_output/
      market_master.csv
      commodity_master_11.csv
      extraction_log.csv
      coverage_matrix.csv
      summary_11_commodities.csv
      raw_json/
      clean_parts/
      master/
        11 separate CSV files
        DAM_ALL_11_COMMODITIES_2010_2026.csv

## Data structure

One row = one market x commodity x reported price date.

The script preserves:
- geography IDs
- market names
- English + Bengali commodity names
- price date/year/month
- wholesale low/high/average
- retail low/high/average
- adjusted wholesale/retail low/high fields exactly as returned
- supply
- unit IDs and unit names
- DAM CPI price record ID
- created_at

No synthetic values are inserted.

## Important geographic naming note

The captured `marketList` contains market names plus division_id,
district_id and upazila_id. It does not contain district_name or
upazila_name in each market record. Therefore the master CSV keeps the
official DAM IDs and market names, while district/upazila names remain blank
until a dedicated DAM hierarchy-name response is captured.

This is deliberate: the script never invents a district/upazila name.
