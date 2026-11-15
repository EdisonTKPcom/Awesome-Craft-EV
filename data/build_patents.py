#!/usr/bin/env python3
"""Build Tesla, BYD and EV-pledge data files from saved official-page HTML and Google Patents CSVs."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(__file__).resolve().parent
RAW = Path("/tmp/patents")
FETCHED = "2026-11-15"
FETCHED_ZONE = "Asia/Kuala_Lumpur (UTC+8)"

TESLA_OFFICIAL_COLS = [
    "patent_number",
    "title",
    "jurisdiction",
    "filing_date",
    "publication_date",
    "grant_date",
    "status",
    "cpc",
    "google_patents_id",
    "link",
    "listed_on_tesla_patent_list",
    "source",
    "notes",
]

GP_COLS = [
    "id",
    "patent_number",
    "title",
    "assignee",
    "inventor",
    "priority_date",
    "filing_date",
    "publication_date",
    "grant_date",
    "status",
    "cpc",
    "joint_assignee",
    "on_tesla_official_list",
    "link",
    "source",
]

BYD_COLS = [
    "id",
    "patent_number",
    "title",
    "assignee",
    "inventor",
    "priority_date",
    "filing_date",
    "publication_date",
    "grant_date",
    "status",
    "cpc",
    "topics",
    "match_type",
    "link",
    "source",
]


def load_gp(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    start = 1 if lines and lines[0].lower().startswith("search url") else 0
    return list(csv.DictReader(lines[start:]))


def rowcells(row_html: str) -> list[str]:
    cells = re.findall(r"<t[hd][^>]*>([\s\S]*?)</t[hd]>", row_html, re.I)
    out = []
    for c in cells:
        c = re.sub(r"<[^>]+>", " ", c)
        c = unescape(re.sub(r"\s+", " ", c)).strip()
        out.append(c)
    return out


def parse_official_list(html_path: Path, which_table: int | None = None) -> list[tuple[str, str]]:
    html = html_path.read_text(encoding="utf-8", errors="replace")
    tables = re.findall(r"<table[\s\S]*?</table>", html, re.I)
    if not tables:
        return []
    chosen = None
    if which_table is not None:
        chosen = tables[which_table]
    else:
        chosen = max(tables, key=len)
    rows = []
    for r in re.findall(r"<tr[\s\S]*?</tr>", chosen, re.I):
        cells = rowcells(r)
        if len(cells) >= 2 and cells[0] and not cells[0].lower().startswith("patent"):
            num = cells[0].replace("\xa0", " ").strip()
            title = cells[1].replace("\xa0", " ").strip()
            rows.append((num, title))
    return rows


def jurisdiction(number: str) -> str:
    m = re.match(r"^([A-Z]{2,3})\b", number.replace("\xa0", " ").strip())
    return m.group(1) if m else ""


def compact_number(number: str) -> str:
    return re.sub(r"\s+", "", number.replace("\xa0", " ").strip())


def gp_core_id(gid: str) -> str:
    # US-9093726-B2 -> US9093726 ; US-D735660-S -> USD735660 ; US-RE44994-E -> USRE44994
    parts = (gid or "").split("-")
    if len(parts) >= 2:
        return parts[0] + parts[1]
    return (gid or "").replace("-", "")


def google_link(gid: str | None, number: str) -> str:
    if gid:
        return f"https://patents.google.com/patent/{gid}/en"
    q = compact_number(number)
    from urllib.parse import quote
    return f"https://patents.google.com/?q={quote(q)}"


def is_core_tesla_assignee(assignee: str) -> tuple[bool, bool]:
    a = assignee or ""
    al = a.lower()
    excluded = (
        "nanocoatings",
        "laboratories",
        "biohealing",
        "bio healing",
        "subsea",
        "tesla coil",
        "purepulse",
        "manz ag",
        "qbotix",
        "q bio",
        "john miller",
        "hibar",
        "space exploration",
    )
    if any(x in al for x in excluded):
        return False, False
    patterns = (
        r"tesla,?\s*inc",
        r"tesla motors",
        r"telsa,?\s*inc",
        r"telsa motors",
        r"tesia motors",
        r"tesla energy operations",
        r"테슬라",
        r"特斯拉公司",
        r"特斯拉汽车",
        r"美商特斯拉",
        r"テスラ・",
        r"テスラ・インコーポレーテッド",
    )
    if not re.search("|".join(patterns), a, re.I):
        return False, False
    joint = "," in a and not re.fullmatch(r"\s*tesla[^,]*\s*", a, re.I)
    # also joint if another company name sits beside Tesla
    if re.search(r"panasonic|argonne|toyota|uchicago", al):
        joint = True
    return True, joint


def is_byd_assignee(assignee: str) -> bool:
    a = assignee or ""
    al = a.lower()
    return any(
        s in a or s in al
        for s in (
            "byd",
            "比亚迪",
            "比亞迪",
            "비와이디",
            "ビーワイディー",
        )
    )


FOCUS = {
    "blade_battery": r"blade|刀片",
    "lfp_ctp": r"lithium iron|lithium-iron|\blfp\b|ferrous phosphate|phosphate iron|磷酸铁锂|磷酸鐵鋰|cell[- ]to[- ]pack|\bctp\b|无模组|無模組|cell to pack",
    "e_platform": r"e-platform|e platform|e平台|e 平台|8-in-1|8 in 1|8合1|八合一",
    "dmi_hybrid": r"\bdm-?i\b|\bdmi\b|super hybrid|plug-?in hybrid|\bphev\b|hybrid power|hybrid vehicle|hybrid electric|超级混动|超級混動|插电混|插電混|混动|混動|混合动力|混合動力|混合电动|混合電動|油电混|油電混",
    "super_e_flash": r"super e-platform|超级e平台|超級e|1000\s*v|megawatt|兆瓦|flash charg|闪充|閃充|\b10c\b",
    "cell_to_body": r"cell[- ]to[- ]body|\bctb\b|电池车身|電池車身|车身一体|車身一體",
}

TIGHT = re.compile(
    r"electric vehicle|electric car|electric automobile|electric motor vehicle|"
    r"hybrid vehicle|hybrid electric|hybrid power|plugin hybrid|plug-in hybrid|"
    r"charging station|charge point|charge port|charging pile|charging connector|"
    r"battery pack|battery module|traction motor|drive motor|powertrain|"
    r"electric vehicle charging|on-board charger|onboard charger|"
    r"电动汽车|電動汽車|电动车|電動車|混动|混動|混合动力|混合動力|"
    r"充电桩|充電樁|充电枪|充電槍|充电座|充電座|充电口|充電口|"
    r"电池包|電池包|驱动电机|驅動電機|刀片电池|刀片電池|牵引电机|牽引電機",
    re.I,
)


def focus_tags(title: str) -> list[str]:
    t = title or ""
    return [k for k, p in FOCUS.items() if re.search(p, t, re.I)]


def write_csv_json(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})
    path.with_suffix(".json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    official_2019 = parse_official_list(RAW / "tesla-legal-2019b.html", which_table=1)
    official_2024 = parse_official_list(RAW / "tesla-legal-2024b.html")
    if not official_2019:
        raise SystemExit("failed to parse 2019 Tesla official patent list")
    set_2019 = {n for n, _ in official_2019}
    set_2024 = {n for n, _ in official_2024}
    if official_2024 and set_2019 != set_2024:
        print("WARNING: 2019 and 2024 official lists differ", len(set_2019 - set_2024), len(set_2024 - set_2019))
    else:
        print("official lists 2019/2024 identical", len(official_2019))

    # Google Patents Tesla
    gp_tesla_rows = []
    for name in ("gp-tesla-inc.csv", "gp-tesla-motors.csv"):
        p = RAW / name
        if p.exists():
            gp_tesla_rows.extend(load_gp(p))

    tesla_gp_by_core: dict[str, dict] = {}
    tesla_core_rows = []
    seen_ids = set()
    for r in gp_tesla_rows:
        ok, joint = is_core_tesla_assignee(r.get("assignee") or "")
        if not ok:
            continue
        gid = r.get("id") or ""
        if gid in seen_ids:
            continue
        seen_ids.add(gid)
        rec = {
            "id": gid,
            "patent_number": gp_core_id(gid),
            "title": (r.get("title") or "").strip(),
            "assignee": (r.get("assignee") or "").strip(),
            "inventor": (r.get("inventor/author") or "").strip(),
            "priority_date": r.get("priority date") or "",
            "filing_date": r.get("filing/creation date") or "",
            "publication_date": r.get("publication date") or "",
            "grant_date": r.get("grant date") or "",
            "status": "",
            "cpc": "",
            "joint_assignee": "yes" if joint else "no",
            "on_tesla_official_list": "",
            "link": f"https://patents.google.com/patent/{gid}/en" if gid else "",
            "source": "Google Patents CSV export, assignee query Tesla Inc / Tesla Motors, fetched 2026-11-15",
        }
        tesla_core_rows.append(rec)
        tesla_gp_by_core[gp_core_id(gid)] = rec

    official_rows = []
    official_compact = set()
    for number, title in official_2019:
        core = compact_number(number)
        official_compact.add(core)
        # try match US D / RE variants already compact
        match = tesla_gp_by_core.get(core)
        # official US 9093726 vs US9093726 already
        notes = (
            "Entry from Tesla's official Patent List on its legal page. "
            "Dates, Google Patents id and link are filled only when this snapshot matched a Google Patents record; "
            "they are not from Tesla. Filing/grant dates, legal status and CPC were not published on Tesla's list."
        )
        official_rows.append(
            {
                "patent_number": number,
                "title": title,
                "jurisdiction": jurisdiction(number),
                "filing_date": (match or {}).get("filing_date", ""),
                "publication_date": (match or {}).get("publication_date", ""),
                "grant_date": (match or {}).get("grant_date", ""),
                "status": "",
                "cpc": "",
                "google_patents_id": (match or {}).get("id", ""),
                "link": google_link((match or {}).get("id"), number),
                "listed_on_tesla_patent_list": "yes",
                "source": (
                    "Tesla official Patent List, archived from https://www.tesla.com/about/legal#patent-list "
                    "on 2019-05-06 (Wayback 20190506080739) and confirmed identical on "
                    "https://www.tesla.com/legal/additional-resources#patent-list archived 2024-01-08 "
                    "(Wayback 20240108120748). Parsed 2026-11-15."
                ),
                "notes": notes,
            }
        )

    matched = sum(1 for r in official_rows if r["google_patents_id"])
    print("official", len(official_rows), "enriched", matched, "juris", Counter(r["jurisdiction"] for r in official_rows))

    for rec in tesla_core_rows:
        rec["on_tesla_official_list"] = "yes" if rec["patent_number"] in official_compact else "no"
    tesla_core_rows.sort(key=lambda r: (r["id"] or ""))

    write_csv_json(DATA / "tesla-patents.csv", official_rows, TESLA_OFFICIAL_COLS)
    write_csv_json(DATA / "tesla-patents-google.csv", tesla_core_rows, GP_COLS)
    print("tesla google core", len(tesla_core_rows), "on official list", sum(1 for r in tesla_core_rows if r["on_tesla_official_list"] == "yes"))

    # BYD
    byd_raw = []
    for name in ("gp-byd-co-ltd.csv", "gp-byd-company.csv"):
        p = RAW / name
        if p.exists():
            byd_raw.extend(load_gp(p))
    byd_unique = {}
    byd_assignee_unique = {}
    for r in byd_raw:
        gid = r.get("id") or ""
        if not gid:
            continue
        if is_byd_assignee(r.get("assignee") or ""):
            byd_assignee_unique.setdefault(gid, r)
        byd_unique.setdefault(gid, r)
    print("byd raw", len(byd_raw), "unique ids", len(byd_unique), "byd-assignee unique", len(byd_assignee_unique))

    byd_rows = []
    tag_counts: Counter[str] = Counter()
    match_counts: Counter[str] = Counter()
    for gid, r in byd_assignee_unique.items():
        title = (r.get("title") or "").strip()
        tags = focus_tags(title)
        tight = bool(TIGHT.search(title))
        if not tags and not tight:
            continue
        match_type = "focus" if tags else "ev_keyword"
        for t in tags:
            tag_counts[t] += 1
        match_counts[match_type] += 1
        byd_rows.append(
            {
                "id": gid,
                "patent_number": gp_core_id(gid),
                "title": title,
                "assignee": (r.get("assignee") or "").strip(),
                "inventor": (r.get("inventor/author") or "").strip(),
                "priority_date": r.get("priority date") or "",
                "filing_date": r.get("filing/creation date") or "",
                "publication_date": r.get("publication date") or "",
                "grant_date": r.get("grant date") or "",
                "status": "",
                "cpc": "",
                "topics": "|".join(tags),
                "match_type": match_type,
                "link": f"https://patents.google.com/patent/{gid}/en",
                "source": "Google Patents CSV export, assignee query BYD Co Ltd / BYD Company Limited, fetched 2026-11-15; filtered to EV-relevant titles",
            }
        )
    byd_rows.sort(key=lambda r: (0 if r["match_type"] == "focus" else 1, r["id"]))
    write_csv_json(DATA / "byd-patents.csv", byd_rows, BYD_COLS)
    print("byd ev-filtered", len(byd_rows), "tags", dict(tag_counts), "match", dict(match_counts))

    pledges = [
        {
            "organization": "Tesla, Inc.",
            "program": "Tesla Patent Pledge",
            "announced_date": "2014-06-12",
            "term": "Stated as irrevocable; applies for so long as the other party is acting in good faith",
            "what_is_covered": "Patents owned now or in the future by Tesla, except patents owned jointly with a third party and later-acquired patents that come with an encumbrance that prevents them being subject to the pledge. Tesla said a list of Tesla Patents subject to the pledge would be maintained on its legal page.",
            "terms_one_line": "Irrevocable standstill not to sue for EV or related-equipment use while the other party acts in good faith; not a licence or waiver, and good-faith exclusions apply.",
            "consideration": "No fee stated; it is a standstill, not a royalty-free licence.",
            "official_source_url": "https://www.tesla.com/legal/additional-resources",
            "source_title": "Tesla Additional Resources, Patent Pledge",
            "related_source_url": "https://www.tesla.com/blog/all-our-patent-are-belong-you",
            "status": "Pledge text still present on Tesla's legal page in a 2025-03-12 archive; the itemised patent table is in 2019 and 2024 archives (361 identical entries) but was not present in the 2025-03-12 captured HTML.",
            "notes": "FACT from Tesla's blog (12 June 2014) and legal page. This is not legal advice.",
        },
        {
            "organization": "Tesla, Inc. / SAE International",
            "program": "North American Charging Standard (NACS), later SAE J3400",
            "announced_date": "2022-11-11",
            "term": "Tesla opened the connector design in November 2022. Tesla said on 30 September 2024 that the design and specification files are now in SAE J3400 Recommended Practice.",
            "what_is_covered": "Tesla opened its EV connector and charge-port design, renamed NACS. SAE J3400_202409 is the SAE Recommended Practice for the North American Charging System (NACS).",
            "terms_one_line": "Connector design opened in 2022; Tesla later pointed adopters to SAE J3400 after it became a Recommended Practice, and removed the specs and CAD from Tesla's website.",
            "consideration": "Not a patent pledge. It is an opened connector design later standardised as SAE J3400.",
            "official_source_url": "https://www.tesla.com/blog/opening-north-american-charging-standard",
            "source_title": "Opening the North American Charging Standard (Tesla blog, 11 November 2022)",
            "related_source_url": "https://saemobilus.sae.org/standards/j3400_202409-north-american-charging-system-nacs-electric-vehicles",
            "status": "SAE J3400_202409 published 30 September 2024 as a Recommended Practice.",
            "notes": "Also see Tesla Support Charging & Adapter Product Guides, update of 30 September 2024.",
        },
        {
            "organization": "Toyota Motor Corporation",
            "program": "Fuel-cell vehicle patent licences",
            "announced_date": "2015-01-06",
            "term": "FCV-related patents for manufacturing and selling FCVs were offered royalty-free through the initial market introduction period, anticipated until about the end of 2020. About 70 hydrogen-station-related patent licences were offered royalty-free for an unlimited duration.",
            "what_is_covered": "Approximately 5,680 FCV-related patent licences (including pending applications) held globally on an unconsolidated basis: about 1,970 fuel-cell stack, 290 high-pressure hydrogen tank, 3,350 system-control, and 70 hydrogen production and supply / station licences.",
            "terms_one_line": "Royalty-free use under a negotiated contract with Toyota; FCV vehicle patents were time-limited to about 2020, hydrogen-station patents were said to be open indefinitely, and Toyota may request but not require reciprocal licensing.",
            "consideration": "Royalty-free, but a contract with Toyota is required.",
            "official_source_url": "https://global.toyota/en/detail/4663648",
            "source_title": "Toyota Opens Its Fuel Cell Vehicle Patents for Free Use (6 January 2015)",
            "related_source_url": "",
            "status": "The stated royalty-free window for FCV vehicle patents ran until about the end of 2020 and has therefore ended as originally described. The hydrogen-station patents were stated to remain open for an unlimited duration. Later expanded by the 2019 electrification announcement.",
            "notes": "US newsroom release is dated 5 January 2015 and gives the same counts; the global official release is dated 6 January 2015.",
        },
        {
            "organization": "Toyota Motor Corporation",
            "program": "Vehicle electrification patent licences",
            "announced_date": "2019-04-03",
            "term": "Grant period starts immediately and lasts through the end of 2030.",
            "what_is_covered": "Nearly 24,000 patents (Toyota's figure is approximately 23,740, including some pending applications) for vehicle electrification-related technologies, including about 2,590 electric-motor, 2,020 PCU, 7,550 system-control, 1,320 engine-transaxle, 2,200 charger, and 2,380 additional fuel-cell patents (bringing fuel-cell-related patents to 8,060).",
            "terms_one_line": "Royalty-free licences through the end of 2030 under a contract with Toyota; separate fee-based technical support is offered for Toyota electrification systems.",
            "consideration": "Patent licences are royalty-free; technical support is fee-based; both are contract-based.",
            "official_source_url": "https://global.toyota/en/newsroom/corporate/27512455.html",
            "source_title": "Toyota Promotes Global Vehicle Electrification by Providing Nearly 24,000 Licences Royalty-Free (3 April 2019)",
            "related_source_url": "https://global.toyota/en/mobility/case/patents2030.html",
            "status": "Stated term runs through the end of 2030. Coverage and current process should be checked with Toyota.",
            "notes": "Counts are Toyota's own figures from the official announcement (FACT that Toyota stated them, not an independent audit).",
        },
        {
            "organization": "Ford Motor Company",
            "program": "Electrified-vehicle patent licensing offer",
            "announced_date": "2015-05-28",
            "term": "No end date was stated in the 28 May 2015 announcement.",
            "what_is_covered": "Ford said it was opening its portfolio of electrified-vehicle technology patents and published applications to competitive automakers. It stated it had more than 650 electrified-vehicle patents and approximately 1,000 pending applications.",
            "terms_one_line": "Patents offered for licence through Ford's technology commercialisation and licensing office or AutoHarvest, available for a fee — this is licensing, not a free pledge.",
            "consideration": "Available for a fee.",
            "official_source_url": "https://media.ford.com/content/fordmedia/fna/us/en/news/2015/05/28/ford-opens-portfolio-of-patented-technologies-to-competitors-to-.html",
            "source_title": "Ford Opens Portfolio of Patented Technologies to Competitors to Accelerate Industry-Wide Electrified Vehicle Development (28 May 2015)",
            "related_source_url": "https://web.archive.org/web/20250519114603/https://media.ford.com/content/fordmedia/fna/us/en/news/2015/05/28/ford-opens-portfolio-of-patented-technologies-to-competitors-to-.html",
            "status": "The original Ford Media announcement is dated 28 May 2015. The live media.ford.com URL redirected to a general Ford site in this 2026-11-15 snapshot; the text was verified from a 19 May 2025 Wayback capture.",
            "notes": "Not a royalty-free or open-source pledge.",
        },
        {
            "organization": "Low Carbon Patent Pledge signatories",
            "program": "Low Carbon Patent Pledge (LCPP)",
            "announced_date": "2021-04-22",
            "term": "Royalty-free licence for the entire term of each pledged patent, subject to defensive termination.",
            "what_is_covered": "Patents listed by pledgors at the LCPP pledged-IP page, for practising the patented technologies for the use, generation, storage or distribution of low-carbon energy from solar, wind, ocean, hydropower or geothermal sources. LCPP news later said 563 pledged patents had been uploaded to the WIPO GREEN database.",
            "terms_one_line": "Royalty-free, non-transferable, non-sublicensable, non-exclusive, worldwide, fully paid-up licence limited to those low-carbon energy uses; the licence terminates if the licensee asserts IP against the pledgor or does not act in good faith.",
            "consideration": "Royalty-free, within the stated energy-use field.",
            "official_source_url": "https://lowcarbonpatentpledge.org/the-pledge/",
            "source_title": "The Pledge – Low Carbon Patent Pledge",
            "related_source_url": "https://lowcarbonpatentpledge.org/news-and-events/",
            "status": "Active pledge text on the official LCPP site as of this research. The licence field is low-carbon energy (including storage), not a general EV-vehicle patent pledge.",
            "notes": "Launched on Earth Day 2021 by Hewlett Packard Enterprise, Microsoft and Meta (formerly Facebook), per LCPP news. Later official LCPP news items announce additional pledgors including JPMorgan Chase, Micro Focus, Majid Al Futtaim, UPS, Lenovo, Alibaba, VIAVI Solutions, Ant Group, Panasonic, Amazon and TD Bank Group. That is not necessarily a complete current membership list.",
        },
        {
            "organization": "Eco-Patent Commons (defunct)",
            "program": "Eco-Patent Commons",
            "announced_date": "2008-01",
            "term": "The Commons was formally discontinued in May 2016.",
            "what_is_covered": "Environmentally beneficial patents pledged by participating companies into a shared commons, originally administered with the World Business Council for Sustainable Development.",
            "terms_one_line": "A now-discontinued commons that made pledged environmental patents available under the Commons' terms; it is no longer operating.",
            "consideration": "Historically pledged for use under the Commons' terms; the programme has ended.",
            "official_source_url": "https://houstonlawreview.org/article/10854-pledging-patents-for-the-public-good-rise-and-fall-of-the-eco-patent-commons",
            "source_title": "Pledging Patents for the Public Good: Rise and Fall of the Eco-Patent Commons (Houston Law Review)",
            "related_source_url": "https://www.wipo.int/en/web/wipo-magazine/articles/the-eco-patent-commons-caring-through-sharing-36818",
            "status": "Defunct (discontinued May 2016).",
            "notes": "Launched in January 2008 by IBM, Nokia, Pitney Bowes and Sony, with WBCSD as initial administrator, as described in the WIPO Magazine article and the Houston Law Review / Contreras-Hall-Helmers post-mortem. The original Commons website is no longer an official live source.",
        },
    ]
    pledge_fields = list(pledges[0].keys())
    write_csv_json(DATA / "ev-patent-pledges.csv", pledges, pledge_fields)
    print("pledges", len(pledges))

    # summary sidecar for the README generator and data/README.md
    summary = {
        "fetched": FETCHED,
        "fetched_zone": FETCHED_ZONE,
        "tesla_official_rows": len(official_rows),
        "tesla_official_enriched_with_google_patents": matched,
        "tesla_official_jurisdictions": dict(Counter(r["jurisdiction"] for r in official_rows)),
        "tesla_google_core_rows": len(tesla_core_rows),
        "tesla_google_core_also_on_official_list": sum(1 for r in tesla_core_rows if r["on_tesla_official_list"] == "yes"),
        "byd_google_raw_rows": len(byd_raw),
        "byd_google_unique_ids": len(byd_unique),
        "byd_assignee_unique_ids": len(byd_assignee_unique),
        "byd_ev_filtered_rows": len(byd_rows),
        "byd_focus_rows": match_counts.get("focus", 0),
        "byd_ev_keyword_rows": match_counts.get("ev_keyword", 0),
        "byd_focus_tag_counts": dict(tag_counts),
        "pledge_rows": len(pledges),
    }
    (DATA / "export-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
