"""Step 3.5 - Control variables that could be acquired from open sources.

Acquired (annual, national): official exchange rate BDT/USD (World Bank WDI PA.NUS.FCRF) and
consumer price index 2010=100 (WDI FP.CPI.TOTL); Bangladesh-reported onion imports HS 070310
(UN Comtrade public preview API, annual).
NOT acquired (documented as limitations, nothing is fabricated): monthly customs import volumes,
district cold-storage capacity, BBS food CPI sub-index, BBS district production.
National series are collinear with the commodity x year-month fixed effects of the baseline model,
so they can only enter the less-saturated robustness specification (R18).
"""
import glob
import json
import numpy as np
import pandas as pd
from config import *


def main():
    c = RAW / "controls"
    out = []
    for ind, name in (("PA.NUS.FCRF", "exchange_rate_bdt_per_usd"), ("FP.CPI.TOTL", "cpi_2010_100")):
        d = json.load(open(c / f"wb_{ind}.json"))[1]
        out.append(pd.Series({int(x["date"]): x["value"] for x in d}, name=name))
    a = pd.concat(out, axis=1).sort_index().rename_axis("year").reset_index()
    a["ln_exchange_rate"] = np.log(a.exchange_rate_bdt_per_usd)
    a["ln_cpi"] = np.log(a.cpi_2010_100)
    rows = []
    for f in sorted(glob.glob(str(c / "comtrade" / "*.json"))):
        y = int(f[-9:-5])
        try:
            r = (json.load(open(f)).get("data") or [])
        except Exception:
            r = []
        rows.append(dict(year=y, onion_import_mt_comtrade=r[0]["netWgt"] / 1000 if r and r[0].get("netWgt") else np.nan,
                         onion_import_usd_comtrade=r[0]["primaryValue"] if r else np.nan))
    a = a.merge(pd.DataFrame(rows), on="year", how="left")
    a.to_csv(INTER / "controls_annual.csv", index=False)
    print(a.to_string())


if __name__ == "__main__":
    main()
