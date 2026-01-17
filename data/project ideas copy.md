
### 🟦 **Situation (the setup)**

* The airline industry is vital and highly visible.
* Air travel is statistically very safe, but crashes—though rare—trigger intense public and investor reactions.
* Airlines, manufacturers (like Boeing / Airbus), and insurers are all publicly traded, meaning market sentiment moves instantly after such events.
* **Data exists:** NTSB records (crashes) and financial markets (stock prices).

**→ Core context:** A single catastrophic event combines human tragedy and economic shock.

---

### 🟧 **Complication (the tension / problem)**

* We don’t clearly know **how markets react** and **how long recovery takes** after a crash.
* Is the damage short-lived or does it persist?
* Does it spread to related firms like Boeing or insurers?
* Are financially weaker airlines more prone to crashes or slower to rebound?
* Public perception (search interest, bookings) could also amplify or dampen the effect.

**→ Problem:** The relationship between *safety events* and *financial performance* is under-quantified.

---

### 🟩 **Resolution (what you’re solving / delivering)**

Your project provides **empirical evidence** of these links.

You’ll:

1. **Quantify the stock impact** of major crashes using an *event-study analysis* (abnormal returns & cumulative abnormal returns).
2. **Measure spillovers** to related firms (Boeing, Airbus, insurers).
3. **Predict recovery time** based on crash severity and airline features.
4. *(Optional)* Explore if public interest (Google Trends) tracks financial recovery.

**→ Resolution:** A data-driven picture of how catastrophic events ripple through the aviation ecosystem and capital markets.

---

So in one sentence:

> “We’re solving the uncertainty about how airline crashes affect financial markets — not just for the airline itself, but across the entire aviation network — and how long it takes to recover.”

That’s your narrative spine for the slides.


| Ticker                          | Primary source (quarterly)                                          | Good alternatives                           | Notes (history, caveats)                                                                                                                      |
| ------------------------------- | ------------------------------------------------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **BA** (Boeing)                 | **SEC EDGAR XBRL** (`companyfacts`/`companyconcept`)                | Sharadar SF1 (Nasdaq Data Link), EODHD, FMP | XBRL starts 2009; 2008 may be limited/annual. EDGAR has raw XBRL quarterly revenue by concept. ([Securities and Exchange Commission][1])      |
| **LUV** (Southwest)             | **SEC EDGAR XBRL**                                                  | Sharadar SF1, EODHD, FMP                    | Deep quarterly history via EDGAR; Sharadar standardizes historical quarters back 25+ yrs (US only). ([Securities and Exchange Commission][1]) |
| **CEA** (China Eastern ADR)     | **CNINFO** (A‑share 600115) or company IR; SEC 20‑F/6‑K for interim | EODHD, FMP                                  | CNINFO/HK give quarterly/interim reports; ADR 6‑Ks may be less granular. ([CNInfo][2])                                                        |
| **AF.PA** (Air France‑KLM)      | **EODHD Fundamentals** (quarterly)                                  | FMP, SimFin; ESEF (2020+) for raw XBRL      | ESEF gives iXBRL filings from 2020 onward; use aggregator for 2008–2019. ([EODHD][3])                                                         |
| **LHA.DE** (Lufthansa)          | **EODHD Fundamentals**                                              | FMP, SimFin; ESEF (2020+)                   | Similar to AF.PA: use ESEF for post‑2020, aggregator for 2008+. ([EODHD][3])                                                                  |
| **EADSY** / **AIR.PA** (Airbus) | **EODHD Fundamentals**                                              | FMP, SimFin; ESEF (2020+)                   | EU issuer; quarterly/interim via ESEF+IR. ADR EDGAR coverage is mixed. ([EODHD][3])                                                           |
| **020560.KS** (Asiana)          | **Korea FSS Open DART**                                             | EODHD (if covered)                          | Open DART exposes quarterly statements/XBRL (best from ~2011+). ([Engopendart][4])                                                            |
| **089590.KQ** (Jeju Air)        | **Korea FSS Open DART**                                             | EODHD (if covered)                          | Same as Asiana. ([Engopendart][4])                                                                                                            |
| **PGSUS.IS** (Pegasus)          | **Turkey KAP (Public Disclosure Platform)**                         | EODHD, FMP                                  | KAP hosts quarterly IFRS; EODHD/FMP standardize. ([KAP][5])                                                                                   |



$ figure out how to compute Max Adverse Excursion (MAE) & Time to Recovery (TTR) (add it to my notebook)
$ repeat my notebook (curr) for low-injury category, maybe one more
COMPILATION:
>> brief analysis of companies involved in crashes (groupings if vendors too necessary)
>> AVG TTR, MAE and CAR across categories
>> macro-stock visualization with crashes as red-dots (different colors for different categories)
>> visualize CAR, TTR and MAE for all the different companies for all different groupings

>> [optional] predictive model? maybe not
>> [optional] topical analysis for groupings ~~ IDK
