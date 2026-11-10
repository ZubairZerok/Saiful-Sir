DAM 11-COMMODITY REAL EXTRACTOR — FINAL

Files:
- dam_11_commodity_extractor_FINAL.py
- common_dropdowns.json
- requirements.txt

IMPORTANT:
This final version uses the user's captured DAM Bearer token directly, so
there is NO token prompt.

FIRST TEST:
python dam_11_commodity_extractor_FINAL.py --test-known

That tests the known captured-style market/commodity:
market_id=28, commodity_id=832 (Onion-imported).

THEN SMALL TEST:
python dam_11_commodity_extractor_FINAL.py --max-markets 3 --workers 2 --delay 0.6

THEN FULL RUN:
python dam_11_commodity_extractor_FINAL.py --workers 4 --delay 0.6

The script creates:
- raw JSON archive
- clean per-market CSVs
- extraction_log.csv
- coverage_matrix.csv
- summary_11_commodities.csv
- 11 separate master CSVs
- one combined master CSV

The output never fills missing prices with fabricated values.
