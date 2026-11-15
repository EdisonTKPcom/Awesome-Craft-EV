# Open EV patent data

Research export of public patent pledges and patent records for [Awesome Craft EV](https://github.com/EdisonTKPcom/Awesome-Craft-EV). Parsed and fetched on **2026-11-15** in **Asia/Kuala_Lumpur (UTC+8)**.

This folder is a research summary of public web pages and patent-database exports. It is **not legal advice**. A row in these files does not grant a licence, confirm that a patent is in force, or mean that a pledged patent is free to use. Pledges have conditions, exceptions and time limits. Read the official terms and get legal advice before relying on any of them.

Evidence tags used in the list README also apply here:

- **FACT** — a figure or statement taken from a named source.
- **GOAL** — a stated plan, roadmap or manufacturer claim that this project did not independently measure.
- **ESTIMATE** — a count or filter we computed from those sources.

## Files

| File | What it contains |
| --- | --- |
| [tesla-patents.csv](tesla-patents.csv) / [tesla-patents.json](tesla-patents.json) | Tesla's official Patent List (361 entries). |
| [tesla-patents-google.csv](tesla-patents-google.csv) / [tesla-patents-google.json](tesla-patents-google.json) | Supplemental Google Patents export for Tesla-related assignees. |
| [byd-patents.csv](byd-patents.csv) / [byd-patents.json](byd-patents.json) | Google Patents export for BYD assignees, filtered to EV-relevant titles. |
| [ev-patent-pledges.csv](ev-patent-pledges.csv) / [ev-patent-pledges.json](ev-patent-pledges.json) | Verified EV-related patent pledges and one opened charging-connector design. |
| [export-summary.json](export-summary.json) | Row counts used by `gen.py`. |
| [build_patents.py](build_patents.py) | Regenerates the exports from saved HTML and Google Patents CSVs. |

The raw Google Patents downloads and archived HTML are not stored in this repository (several of the CSVs were 5–6 MB and noisy until filtered). The script reads them from `/tmp/patents` when rerun.

## Tesla official Patent List

**Source used for `tesla-patents.csv`:** Tesla's own Patent List, not a first-principles rebuild from a patent office.

Tesla's legal page says a list of Tesla Patents subject to the Patent Pledge "will be maintained" at [tesla.com/legal/additional-resources#patent-list](https://www.tesla.com/legal/additional-resources#patent-list). The company does not publish filing dates, grant dates, legal status or CPC classes on that list.

This snapshot recovered the itemised table from archived HTML:

- [Wayback 20190506080739](https://web.archive.org/web/20190506080739/https://www.tesla.com/about/legal) of `https://www.tesla.com/about/legal#patent-list` — **6 May 2019, 16:07 Asia/Kuala_Lumpur (UTC+8)** (08:07 UTC).
- [Wayback 20240108120748](https://web.archive.org/web/20240108120748/https://www.tesla.com/legal/additional-resources) of `https://www.tesla.com/legal/additional-resources#patent-list` — **8 January 2024, 20:07 Asia/Kuala_Lumpur (UTC+8)** (12:07 UTC).

**Row count (FACT from those pages):** 361 patent-number-and-title entries. The two archives are identical.

**Jurisdiction counts (ESTIMATE, counted from the official numbers):** US 249, JP 27, DE 22, EP 22, FR 14, GB 14, CA 5, CN 5, AU 1, HK 1, KR 1. These are national or regional filings, so 361 is not 361 distinct inventions.

**Limits:**

- Tesla's pledge text defines "Tesla Patents" as all patents Tesla owns now or in the future, except jointly owned patents and later-acquired patents that come with an encumbrance. The published list is therefore not a complete legal map of coverage, and Tesla does not itemise which later patents are in or out.
- A [Wayback 20250312165943](https://web.archive.org/web/20250312165943/https://www.tesla.com/legal/additional-resources) capture of the same legal page — **13 March 2025, 00:59 Asia/Kuala_Lumpur (UTC+8)** (12 March 2025, 16:59 UTC) — still contains the pledge wording and the `#patent-list` URL, but the captured HTML does not include the itemised table. This snapshot does not claim to know whether the list is served another way on the live site (tesla.com blocked automated fetches here).
- `status` and `cpc` are empty: neither Tesla's list nor the Google Patents CSV used for enrichment includes legal status (active/expired) or CPC classes.
- Filing, publication and grant dates, and a precise Google Patents id, are filled only when this snapshot matched the official number to a Google Patents record. **163 of 361** official entries were matched that way (ESTIMATE). Unmatched rows still have a Google Patents search link built from the official number; that is a lookup link, not a claim that the record was found.

The pledge terms themselves come from Tesla's legal page (verified in the 2019, 2024 and 2025 archives) and from the 12 June 2014 blog post [All Our Patent Are Belong To You](https://www.tesla.com/blog/all-our-patent-are-belong-you). Direct fetches of tesla.com returned HTTP 403 in this environment, so wording was checked against archived official pages.

## Tesla Google Patents supplement

**File:** `tesla-patents-google.csv`

**Method:** Google Patents CSV export on 2026-11-15, via `https://patents.google.com/xhr/query?url=...&download=true`.

Queries that were kept:

- `assignee=Tesla Inc` → [patents.google.com/?assignee=Tesla+Inc](https://patents.google.com/?assignee=Tesla+Inc)
- `assignee="Tesla Motors"` → [patents.google.com/?assignee=%22Tesla+Motors%22](https://patents.google.com/?assignee=%22Tesla+Motors%22)

A quoted query for `"Tesla, Inc."` (with the comma) returned about 17,925 mixed rows, most of them other companies whose names end in "Inc." That file was discarded.

Rows were then kept only when the assignee looked like Tesla, Inc., Tesla Motors, Tesla Energy Operations, or the Korean, Chinese or Japanese Tesla company names in the export. Joint filings with Panasonic, Argonne or similar are flagged `joint_assignee=yes`. Tesla's pledge excludes jointly owned patents. Unrelated assignees that Google also returned (Tesla Nanocoatings, Tesla BioHealing, Manz AG and others) were dropped.

**Row count (ESTIMATE):** 1,139 unique Google Patents records after that assignee filter. **163** of them also appear on Tesla's official 361-entry list.

**Limits:**

- This is not Tesla's itemisation of pledge coverage. Many records post-date the official list. This project does not decide whether the pledge covers them.
- The export includes energy and solar titles assigned to Tesla, Inc., not only vehicle patents.
- Google Patents CSV has no CPC class and no active/expired status. A grant date is present when Google provided one (not proof the patent is still in force).
- The export is not a complete worldwide register. National filings on the official list (especially CN, DE, JP, EP, FR, GB) often did not appear in this Google Patents download.
- USPTO PatentsView was not used: the current Search API requires a key, and no unauthenticated option was available in this snapshot.

## BYD patents

**File:** `byd-patents.csv`

**Method:** The same Google Patents CSV export on 2026-11-15, for:

- `assignee="BYD Co Ltd"`
- `assignee="BYD Company Limited"`

The two downloads were merged and de-duplicated by Google Patents id. Rows were kept when the assignee string contained BYD, 比亚迪 / 比亞迪, 비와이디 or ビーワイディー.

**Raw portfolio counts (ESTIMATE from this export, before EV filtering):** 45,906 rows across the two CSVs, 33,320 unique ids, **33,254** unique ids with a BYD-related assignee. Google Patents may truncate large result sets, so this is not a certified complete inventory of BYD's worldwide portfolio.

**EV filter (ESTIMATE):** titles were kept if they matched a focus-topic regex (Blade Battery / 刀片, LFP / cell-to-pack, e-Platform / 8-in-1, DM-i / hybrid, Super e-Platform / megawatt flash charging, cell-to-body) or a tighter EV-vehicle / charging / pack / drive-motor keyword list in English or Chinese. See `FOCUS` and `TIGHT` in `build_patents.py`.

**Row count after filtering:** **3,934** unique records — 446 with at least one focus tag, 3,488 with only the broader EV keywords.

**Focus-tag counts (ESTIMATE, a record may have more than one tag):** DM-i / hybrid 368, LFP / cell-to-pack 61, Blade Battery 9, e-Platform 7, cell-to-body 1, Super e-Platform / megawatt flash charging 0.

**Limits:**

- This is a title-keyword filter, not a legal classification and not an official BYD catalogue. Marketing names such as Blade Battery, e-Platform 3.0, Super e-Platform and CTB rarely appear in patent titles, so those tag counts are far lower than the number of possibly related filings.
- No CPC classes or legal status (active/expired) are in the Google Patents CSV, so those columns are empty.
- No verified BYD patent pledge or royalty-free patent licence was found. These rows are public patent records, not open patents.

## EV patent pledges

**File:** `ev-patent-pledges.csv`

Seven verified programmes, each with official source URLs:

1. Tesla Patent Pledge (2014) — standstill, not a licence.
2. Tesla NACS opening (2022) and SAE J3400 — an opened connector design, not a patent pledge.
3. Toyota fuel-cell licences (2015) — royalty-free under contract; vehicle-FCV term was stated until about the end of 2020; hydrogen-station patents were said to be open indefinitely.
4. Toyota electrification licences (2019) — about 23,740 licences royalty-free through the end of 2030, under contract.
5. Ford electrified-vehicle licensing offer (2015) — **for a fee**, not a free pledge. The original Ford Media URL was verified from a [19 May 2025, 19:46 Asia/Kuala_Lumpur (UTC+8)](https://web.archive.org/web/20250519114603/https://media.ford.com/content/fordmedia/fna/us/en/news/2015/05/28/ford-opens-portfolio-of-patented-technologies-to-competitors-to-.html) Wayback capture (11:46 UTC); the live URL redirected to a general Ford site on 2026-11-15.
6. Low Carbon Patent Pledge (2021) — royalty-free licence limited to listed low-carbon energy uses, not a general EV-vehicle pledge.
7. Eco-Patent Commons — launched January 2008, discontinued May 2016.

Searched and **not** included as verified EV patent pledges: a 2024 Volvo "open patents" announcement (news in 2024 was about Volvo's electrified-sales target, not a patent pledge); General Motors or Hyundai open EV patent pledges (none verified on official pages in this snapshot); Open Invention Network and LOT Network (defensive patent networks, not EV patent pledges).

## BYD technology sources (not patent pledges)

Official pages used in the README, for claims that must be tagged FACT (BYD stated this) or GOAL (a plan or unmeasured manufacturer spec):

- Blade Battery announcement: [en.byd.com news](https://en.byd.com/news/byds-new-blade-battery-set-to-redefine-ev-safety-standards/). A later official BYD EU blog, [BYD's revolutionary Blade Battery: all you need to know](https://www.byd.com/eu/blog/BYDs-revolutionary-Blade-Battery-all-you-need-to-know.html) (22 January 2023), says the Blade Battery was launched in March 2020 and describes BYD CTP (cell-to-pack) technology.
- e-Platform 3.0 debut: [BYD Debuts e-Platform 3.0](https://en.byd.com/news/byd-debuts-e-platform-3-0-leading-the-next-generation-of-smart-electric-vehicles/) (19 April 2021, Shanghai Auto Show). A later official EU page, [Why is BYD's e-Platform 3.0 so special?](https://www.byd.com/eu/blog/Why-is-BYDs-e-Platform-3-0-so-special.html) (2 January 2023), describes the platform as launched in September 2021.
- Cell-to-body: [BYD SEAL: Dynamic and Intelligent](https://www.byd.com/eu/news-list/BYD_SEAL_Dynamic_and_Intelligent) (12 April 2023).
- Super e-Platform: [BYD Unveils Super e-Platform with Megawatt Flash Charging](https://www.byd.com/en/news-list/BYD-Unveils-Super-e-Platform-Megawatt-Flash-Charging-Electric-Vehicles-Matching-Refueling-Speeds) (17 March 2025).
- DiLink developer platform: [oip.byd.com](https://oip.byd.com/) (比亚迪汽车工业有限公司). The page did not load from this environment (connection timed out). It is still cited as BYD's official domain for that platform.

No official BYD Company GitHub organisation was verified. `github.com/byd` is a personal account (display name Zima). `github.com/BYDcar` is a GitHub organisation with 7 repositories, but the public page describes community sharing of service materials rather than an official BYD Company release, so it is not listed as official open source.

## Regenerating

Place the archived Tesla HTML and Google Patents CSVs in `/tmp/patents` with the filenames expected by `build_patents.py`, then run:

```bash
python3 data/build_patents.py
python3 gen.py
```
