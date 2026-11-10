# DAM Geography Validation Report

**Total Markets in DAM Central Directory (`marketList`):** 352  
**Total Active Markets with Extracted Data:** 117  
**Total Administrative Divisions Represented:** 8 / 8  
**Total District IDs Represented:** 64  
**Total Upazila IDs Represented:** 112  

---

## 1. Administrative Hierarchy Status

| Geographic Level | ID Availability | String Name Availability | Status / Resolution |
|---|---|---|---|
| **Division** | 100% Complete (`division_id`) | 100% Resolved (`division_name`) | Fully mapped to 8 official divisions of Bangladesh via official lookup. |
| **District** | 100% Complete (`district_id`) | 0% in DAM `marketList` | Official integer `district_id` preserved deterministically. No speculative string imputation. |
| **Upazila** | 100% Complete (`upazila_id`) | 0% in DAM `marketList` | Official integer `upazila_id` preserved deterministically. No speculative string imputation. |
| **Market** | 100% Complete (`market_id`) | 100% English (`market_name`) & Bengali (`market_name_bn`) | Complete verified match against DAM market directory. |

---

## 2. Active Markets by Division

| Division ID | Division Name | Active Markets Count | Total Observations Count |
|---|---|---|---|
| 1 | Chattogram | 23 | 537 |
| 2 | Khulna | 13 | 569 |
| 3 | Rajshahi | 18 | 461 |
| 4 | Barishal | 8 | 197 |
| 5 | Sylhet | 9 | 283 |
| 6 | Dhaka | 23 | 644 |
| 7 | Rangpur | 16 | 467 |
| 8 | Mymensingh | 7 | 190 |

---

## 3. Methodological Note on Missing District/Upazila Names
The DAM `common_dropdowns.json` API endpoint encapsulates `division_id`, `district_id`, and `upazila_id` inside each market record but does not provide standalone text dictionaries for district and upazila names. Per research safety rules, we strictly avoid third-party heuristic name guessing. All spatial grouping and fixed effects for econometric modeling can be executed directly on the immutable numeric IDs (`division_id`, `district_id`, `upazila_id`, `market_id`).
