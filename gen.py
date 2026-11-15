#!/usr/bin/env python3
import csv
import json
import urllib.parse as U
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPORT = json.loads((ROOT / "data/export-summary.json").read_text())
S = {
    r[0]: dict(stars=int(r[1]), forks=int(r[2]), lic=r[3], lang=r[4], push=r[5])
    for r in csv.reader((ROOT / "stats.tsv").open(), delimiter="\t")
}
LICNAME = {"NOASSERTION": "Custom", "none": "None", "OTHER": "Custom"}
AS = "2026-11-15"
ACTIVE_SINCE = "2026-10-16"
OPENPILOT = "commaai/openpilot"

# (name, repo, description) — descriptions already include licence/archive/safety flags
C = [
    (
        "CSMS and OCPP",
        [
            ("CitrineOS", "citrineos/citrineos-core", "LF Energy TypeScript charging station management system built around OCPP 2.0.1, with 1.6 support, an operator UI and OpenAPI APIs."),
            ("Java-OCA-OCPP", "ChargeTimeEU/Java-OCA-OCPP", "Java client and server library for OCPP 1.6 (JSON and SOAP), 2.0.1 and 2.1."),
            ("ocpp", "mobilityhouse/ocpp", "Python library for OCPP 1.6 and 2.0.1, used to build charge points and central systems."),
            ("OCPP.Core", "dallmann-consulting/OCPP.Core", ".NET charging station management system and operator UI for OCPP 1.6 and 2.0.1."),
            ("ocpp-go", "lorenzodonini/ocpp-go", "Go implementation of OCPP-J 1.6 and 2.0.1. The release cadence has slowed, with the last push on 2025-08-24."),
            ("Open e-Mobility", "sap-labs-france/ev-server", "SAP Labs France charging station management server with OCPP, roaming and smart charging. This repository is archived."),
            ("open-ocpp", "c-jimenez/open-ocpp", "C++ implementation of OCPP 1.6 and 2.0.1. Not the same project as ChargeLab's OpenOCPP."),
            ("rust-ocpp", "tommymalmqvist/rust-ocpp", "Rust message-type library for OCPP 1.6, 2.0.1 and 2.1, validated against the official schemas."),
            ("SAP Charging Stations Simulator", "SAP/e-mobility-charging-stations-simulator", "Node.js OCPP-J charge-point simulator for OCPP 1.6 and the 2.0.x line."),
            ("SteVe", "steve-community/steve", "Java charging station management system for OCPP 1.2 through 1.6 (SOAP and JSON), including the 1.6 security profiles, started at RWTH Aachen in 2013."),
        ],
    ),
    (
        "Charger firmware and ISO 15118",
        [
            ("ChargePi", "ChargePi/ChargePi-go", "Linux framework for building charge points, with hardware abstraction and OCPP support."),
            ("EVerest", "EVerest/EVerest", "LF Energy modular Linux stack for AC and DC chargers, with OCPP 1.6, 2.0.1 and 2.1 plus ISO 15118-2, -3 and -20."),
            ("Josev", "ecog-io/iso15118", "Python implementation of ISO 15118-2, -20 and -8, the protocol core of the Josev vehicle-to-grid stack (formerly SwitchEV)."),
            ("MicroOCPP", "matth-x/MicroOcpp", "C++ OCPP 1.6 and 2.0.1 client for microcontrollers, used in OpenEVSE firmware. Last push 2025-12-04."),
            ("OpenEVSE ESP32 firmware", "OpenEVSE/openevse_esp32_firmware", "Wi-Fi gateway, web interface and energy-management firmware for OpenEVSE chargers. GitHub reports no SPDX licence, so read the repository before you use it."),
            ("OpenOCPP", "ChargeLab/OpenOCPP", "Multi-platform C++ OCPP 1.6 and 2.0.1 stack for charging-station firmware. Not the same project as c-jimenez/open-ocpp."),
            ("SmartEVSE 3", "SmartEVSE/SmartEVSE-3", "Open-source EVSE controller with OCPP 1.6J, smart charging and power sharing."),
        ],
    ),
    (
        "Roaming protocols",
        [
            ("OCHP", "e-clearing-net/OCHP", "Open Clearing House Protocol specification from e-clearing.net. Last push 2024-05-02."),
            ("OCPI", "ocpi/ocpi", "Official Open Charge Point Interface specification for roaming between charge-point operators and e-mobility service providers. GitHub could not match a standard SPDX licence."),
            ("OCPI toolkit", "IZIVIA/ocpi-toolkit", "Kotlin library for OCPI operations. Not affiliated with the EVRoaming Foundation."),
            ("OICP", "hubject/oicp", "Hubject Open InterCharge Protocol specification. Licensed under CC-BY-SA-4.0, which is a content licence rather than an OSI software licence."),
            ("TECHS OCPI", "TECHS-Technological-Solutions/ocpi", "Python implementation of the Open Charge Point Interface."),
        ],
    ),
    (
        "Home charging and energy management",
        [
            ("EEBus", "enbility/eebus-go", "Go implementation of the EEBus protocol for coordinating chargers and other energy devices."),
            ("EMHASS", "davidusb-geek/emhass", "Energy-management optimiser for Home Assistant, useful for scheduling EV charging against solar and prices."),
            ("evcc", "evcc-io/evcc", "Local EV charge controller and home energy management system that talks to chargers, meters, solar and vehicles."),
            ("Home Assistant OCPP", "lbbrhzn/ocpp", "Home Assistant integration for chargers that speak OCPP 1.6, 2.0.1 and experimental 2.1."),
            ("OpenEMS", "OpenEMS/openems", "Open-source energy management system, including EV charging and site energy control."),
            ("openWB", "snaptec/openWB", "Modular wallbox and home charging software (version 1). Last push 2025-07-18; new work is in openWB 2."),
            ("openWB 2", "openWB/core", "Successor core for the openWB modular wallbox and home charging software."),
        ],
    ),
    (
        "Battery management systems",
        [
            ("Battery Emulator", "dalathegreat/Battery-Emulator", "Firmware that presents reused EV battery packs to solar inverters for stationary storage. High-voltage work needs qualified handling."),
            ("diyBMS v4", "stuartpittaway/diyBMSv4", "Do-it-yourself lithium pack battery management system. Licensed under CC BY-NC-SA 2.0 UK, which is not an OSI licence and does not allow commercial use."),
            ("ENNOID-BMS", "EnnoidMe/ENNOID-BMS", "Modular LTC68XX and STM32 battery management system for packs up to 400 V. Last push 2021-07-19, so treat it as unmaintained. High-voltage work needs qualified handling."),
            ("foxBMS 2", "foxBMS/foxbms-2", "Fraunhofer modular open battery-management development platform. GitHub could not match a standard SPDX licence, so read it before you use it. High-voltage work needs qualified handling."),
            ("LibreSolar BMS", "LibreSolar/bms-firmware", "Firmware for LibreSolar battery-management boards based on bq769x0, bq769x2 or ISL94202."),
        ],
    ),
    (
        "Motor controllers and inverters",
        [
            ("ODrive", "odriverobotics/ODrive", "High-performance general-purpose motor controller also used in light EV and conversion projects. Last push 2026-01-20."),
            ("OpenInverter", "jsphuebner/stm32-sine", "Open-source inverter firmware used in many DIY EV conversions. High-voltage work needs qualified handling."),
            ("VESC", "vedderb/bldc", "Vedder Electronic Speed Controller firmware, widely used in light EVs and conversions. GitHub reports no SPDX licence, so check the project terms before you use it."),
        ],
    ),
    (
        "Vehicle telematics and data",
        [
            ("bluelinky", "Hacksore/bluelinky", "Unofficial Node.js API for Hyundai Bluelink and Kia UVO vehicle data. Last push 2025-08-13."),
            ("openpilot", "commaai/openpilot", "comma's open driver-assistance system. It is ADAS software, not an EV charging or powertrain stack, though it supports some electric vehicles."),
            ("OVMS", "openvehicles/Open-Vehicle-Monitoring-System-3", "Open Vehicle Monitoring System for remote telemetry and control of many EV models. GitHub could not match a standard SPDX licence."),
            ("PSA Car Controller", "flobz/psa_car_controller", "Control and telemetry for Stellantis (PSA) connected cars, including electric models."),
            ("TeslaLogger", "bassmaster187/TeslaLogger", "Self-hosted data logger for Tesla vehicles."),
            ("TeslaMate", "teslamate-org/teslamate", "Self-hosted Tesla data logger with Grafana dashboards and MQTT."),
        ],
    ),
    (
        "CAN bus and diagnostics",
        [
            ("can-utils", "linux-can/can-utils", "Linux SocketCAN userspace tools such as candump and cansend. GitHub reports no SPDX licence, so confirm the terms in the repository."),
            ("cantools", "cantools/cantools", "Python tools for DBC decoding, monitoring and simulation of CAN buses."),
            ("opendbc", "commaai/opendbc", "Python API and CAN database collection for reading car signals, maintained by comma."),
            ("python-can", "hardbyte/python-can", "Python library for sending and receiving CAN messages across common interfaces."),
            ("SavvyCAN", "collin80/SavvyCAN", "Cross-platform Qt application for capturing, inspecting and decoding CAN traffic."),
        ],
    ),
    (
        "Battery modelling and simulation",
        [
            ("BattMo", "BattMoTeam/BattMo", "Continuum battery modelling toolbox in MATLAB."),
            ("BLAST-Lite", "NatLabRockies/BLAST-Lite", "NREL Battery Lifetime Analysis and Simulation Toolsuite, with degradation models for recent commercial lithium-ion cells. The live GitHub repository is NatLabRockies/BLAST-Lite."),
            ("liionpack", "pybamm-team/liionpack", "Battery-pack simulation tool built on the PyBaMM framework."),
            ("PyBaMM", "pybamm-team/PyBaMM", "Fast, flexible physics-based battery models in Python."),
        ],
    ),
    (
        "Charging maps and open data",
        [
            ("EVMap", "ev-map/EVMap", "Android app for finding public charge points, using community and open data."),
            ("Open Charge Map", "openchargemap/ocm-system", "Global public registry of EV charging locations, with an open API and community contributions."),
            ("Open EV Data", "open-ev-data/open-ev-data-dataset", "Community-maintained, versioned dataset of electric-vehicle specifications. GitHub could not match a standard SPDX licence."),
        ],
    ),
    (
        "Fleet, routing and V2G simulation",
        [
            ("EV2Gym", "StavrosOrf/EV2Gym", "Vehicle-to-grid simulation environment for large-scale EV charging optimisation research."),
            ("Pumperly", "GeiserX/Pumperly", "Self-hostable fuel and EV route planner with live prices in supported countries."),
        ],
    ),
    (
        "DIY conversions",
        [
            ("ccs32clara", "uhi22/ccs32clara", "STM32 and QCA7005 CCS charge-controller project for DIY and research use. High-voltage and mains work needs qualified handling."),
            ("OpenInverter VCU", "jsphuebner/stm32-vcu", "Vehicle control unit for EV conversion projects, a companion to the OpenInverter firmware. High-voltage work needs qualified handling."),
            ("pyPLC", "uhi22/pyPLC", "Python tools for investigating CCS and ISO 15118 charging at the power-line communication layer. High-voltage work needs qualified handling."),
        ],
    ),
]


def k(n):
    if n >= 1e6:
        return f"{n/1e6:.2f}M"
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)


def anchor(n):
    return n.lower().replace(",", "").replace(" ", "-")


def fact(text):
    return f'<span class="ev-fact">{text}</span>'


def estimate(text):
    return f'<span class="ev-est">{text}</span>'


def goal(text):
    return f'<span class="ev-goal">{text}</span>'


def patents_section():
    tesla_n = EXPORT["tesla_official_rows"]
    tesla_us = EXPORT["tesla_official_jurisdictions"]["US"]
    tesla_enriched = EXPORT["tesla_official_enriched_with_google_patents"]
    tesla_gp = EXPORT["tesla_google_core_rows"]
    tesla_gp_overlap = EXPORT["tesla_google_core_also_on_official_list"]
    byd_unique = EXPORT["byd_assignee_unique_ids"]
    byd_n = EXPORT["byd_ev_filtered_rows"]
    byd_focus = EXPORT["byd_focus_rows"]
    tags = EXPORT["byd_focus_tag_counts"]
    return f"""## Open patents and pledges

This section is a research summary of public statements and patent records, not legal advice. Patent pledges and royalty-free programmes have conditions, time limits and exceptions. A listing here does not grant a licence, confirm that a patent is in force, or mean it is free to use. Read the official terms and get legal advice before relying on any pledge.

Figures and statements below use the same evidence tags as the dashboard: {fact("FACT")} from a named source, {goal("GOAL")} for a stated plan or an unmeasured manufacturer claim, and {estimate("ESTIMATE")} for counts this project computed. Source notes and export limits are in [data/README.md](data/README.md). The machine-readable files are [tesla-patents.csv](data/tesla-patents.csv), [byd-patents.csv](data/byd-patents.csv) and [ev-patent-pledges.csv](data/ev-patent-pledges.csv).

### Tesla Patent Pledge

On {fact("12 June 2014")}, Tesla published [All Our Patent Are Belong To You](https://www.tesla.com/blog/all-our-patent-are-belong-you), announcing that it "will not initiate patent lawsuits against anyone who, in good faith, wants to use our technology."

The current legal terms are on Tesla's [Additional Resources](https://www.tesla.com/legal/additional-resources) page (anchors `#patent-pledge` and `#patent-list`). As of the archives checked for this snapshot, those terms say:

<table>
<tr><th>Term</th><th>What Tesla's legal page says</th></tr>
<tr><td>Pledge</td><td>Tesla {fact("irrevocably pledges")} that it will not initiate a lawsuit against any party for infringing a Tesla Patent through activity relating to electric vehicles or related equipment for so long as that party is acting in good faith.</td></tr>
<tr><td>Legal effect</td><td>The pledge is a {fact("standstill")} (forbearance of enforcement). It is {fact("not a licence, covenant not to sue, waiver, or authorisation")} to practise the patents.</td></tr>
<tr><td>Good faith</td><td>Good faith excludes, among other things, asserting intellectual property rights against Tesla, asserting patent rights against a third party for use of electric-vehicle technologies, challenging Tesla patents, or marketing knock-off Tesla products.</td></tr>
<tr><td>Tesla Patents</td><td>This means all patents owned now or in the future by Tesla, other than a patent owned jointly with a third party or a later-acquired patent that comes with an encumbrance that prevents it from being subject to the pledge.</td></tr>
<tr><td>List</td><td>Tesla says a list of Tesla Patents subject to the pledge will be maintained on that legal page.</td></tr>
</table>

Tesla does not publish filing dates, legal status or CPC classes on that list, and this project does not treat the list as a complete legal map of the broader "now or in the future" definition.

The itemised table was recovered from official-page archives dated {fact("6 May 2019")} and {fact("8 January 2024")} (see data/README.md for the Wayback captures). Both captures contain the {fact(f"same {tesla_n} entries")}. {estimate(str(tesla_us))} of those numbers are US filings; the rest are AU, CA, CN, DE, EP, FR, GB, HK, JP or KR, so {tesla_n} is not {tesla_n} distinct inventions. {estimate(str(tesla_enriched))} official numbers were matched to a Google Patents record in this snapshot so that dates and a precise document id could be added; the other rows have a search link only. The export is data/tesla-patents.csv.

A {fact("12 March 2025")} archive of the same legal page still has the pledge wording and the `#patent-list` URL, but the captured HTML does not include the itemised table.

A separate Google Patents assignee export on {fact("15 November 2026")} found {estimate(str(tesla_gp))} Tesla-related records after filtering out unrelated assignees. {estimate(str(tesla_gp_overlap))} of those also appear on the official {tesla_n}-entry list. That Google Patents file is a public-database supplement, not Tesla's itemisation of pledge coverage, and it is saved as [tesla-patents-google.csv](data/tesla-patents-google.csv).

### NACS and SAE J3400

On {fact("11 November 2022")}, Tesla published [Opening the North American Charging Standard](https://www.tesla.com/blog/opening-north-american-charging-standard). It invited charging networks and vehicle makers to use the Tesla connector and charge port, then renamed NACS, and said the design and specification files were available for download while Tesla worked with standards bodies.

Tesla's [Charging & Adapter Product Guides](https://www.tesla.com/support/charging/product-guides) were later updated on {fact("30 September 2024")}: as NACS is recognised in an SAE Recommended Practice under SAE J3400, Tesla removed the technical specifications and CAD from its website and said those files are now available in the SAE J3400 Recommended Practice.

{fact("SAE J3400_202409")}, [North American Charging System (NACS) for Electric Vehicles](https://saemobilus.sae.org/standards/j3400_202409-north-american-charging-system-nacs-electric-vehicles), is the SAE Recommended Practice dated September 2024. This is an opened connector design that became a public standard, not a patent pledge. Performance comparisons in Tesla's 2022 blog, including "up to 1 MW DC charging", are Tesla's own statements.

### Other pledges and licences

<table>
<tr><th>Programme</th><th>When</th><th>What it is</th><th>Official source</th></tr>
<tr>
<td>Toyota fuel-cell licences</td>
<td>{fact("6 January 2015")}</td>
<td>Royalty-free licences on about {fact("5,680")} FCV-related patents, under a contract with Toyota. Licences for manufacturing and selling FCVs were offered through the initial market introduction period, anticipated until about the {fact("end of 2020")} — that stated window has ended. About {fact("70")} hydrogen-station patents were said to remain open for an unlimited duration.</td>
<td><a href="https://global.toyota/en/detail/4663648">Toyota global release</a></td>
</tr>
<tr>
<td>Toyota electrification licences</td>
<td>{fact("3 April 2019")}</td>
<td>Royalty-free licences on nearly {fact("24,000")} patents (Toyota's own figure is approximately {fact("23,740")}) for vehicle electrification technologies, through the {fact("end of 2030")}, under a contract. Separate technical support is {fact("fee-based")}. The end-2030 date is a stated term ({goal("GOAL")} of the programme's duration, as published by Toyota).</td>
<td><a href="https://global.toyota/en/newsroom/corporate/27512455.html">Toyota newsroom</a></td>
</tr>
<tr>
<td>Ford electrified-vehicle patents</td>
<td>{fact("28 May 2015")}</td>
<td>Ford offered competitors access to its electrified-vehicle patent portfolio. It said it had more than {fact("650")} electrified-vehicle patents and approximately {fact("1,000")} pending applications. The patents were {fact("available for a fee")} — this is licensing, not a free pledge.</td>
<td><a href="https://media.ford.com/content/fordmedia/fna/us/en/news/2015/05/28/ford-opens-portfolio-of-patented-technologies-to-competitors-to-.html">Ford Media announcement</a></td>
</tr>
<tr>
<td>Low Carbon Patent Pledge</td>
<td>{fact("22 April 2021")}</td>
<td>A royalty-free licence, launched by Hewlett Packard Enterprise, Microsoft and Meta, limited to practising pledged patents for the use, generation, storage or distribution of low-carbon energy from solar, wind, ocean, hydropower or geothermal sources. It is not a general EV-vehicle patent pledge. The licence has a defensive-termination clause. LCPP later said {fact("563")} pledged patents had been uploaded to WIPO GREEN.</td>
<td><a href="https://lowcarbonpatentpledge.org/the-pledge/">The Pledge</a></td>
</tr>
<tr>
<td>Eco-Patent Commons</td>
<td>{fact("January 2008")} – {fact("May 2016")}</td>
<td>A shared commons for environmentally beneficial patents. It was {fact("discontinued in May 2016")}.</td>
<td><a href="https://houstonlawreview.org/article/10854-pledging-patents-for-the-public-good-rise-and-fall-of-the-eco-patent-commons">Houston Law Review history</a></td>
</tr>
</table>

Volvo's 2024 electric-sales announcements were about vehicle-mix targets, not an open patent pledge, so they are not listed. This snapshot also did not find a verified official GM or Hyundai open EV patent pledge, and it does not treat Open Invention Network or LOT Network as EV patent pledges (they are defensive patent networks).

### BYD technology

No verified BYD patent pledge or royalty-free patent licence was found in this snapshot. The rows in data/byd-patents.csv are public patent records, not open patents.

Google Patents assignee exports for "BYD Co Ltd" and "BYD Company Limited" on {fact("15 November 2026")} produced {estimate(f"{byd_unique:,}")} unique BYD-assignee records before filtering (ESTIMATE, and possibly incomplete). After a title-keyword filter for EV-relevant filings, {estimate(f"{byd_n:,}")} records remain, of which {estimate(str(byd_focus))} match a focus topic: Blade Battery or 刀片 ({estimate(str(tags.get("blade_battery", 0)))}), LFP or cell-to-pack ({estimate(str(tags.get("lfp_ctp", 0)))}), e-Platform or 8-in-1 ({estimate(str(tags.get("e_platform", 0)))}), DM-i or hybrid ({estimate(str(tags.get("dmi_hybrid", 0)))}), cell-to-body ({estimate(str(tags.get("cell_to_body", 0)))}), and Super e-Platform or megawatt flash charging ({estimate(str(tags.get("super_e_flash", 0)))}). Those tag counts are keyword ESTIMATEs. Marketing names rarely appear in patent titles, so they are not a catalogue of every related filing.

Official BYD technology pages, with stated specs tagged as claims unless independently measured here:

- [Blade Battery](https://en.byd.com/news/byds-new-blade-battery-set-to-redefine-ev-safety-standards/) - BYD said long cells are arranged in an array in the pack and that pack space utilisation increased by over {fact("50%")} compared with conventional lithium-iron-phosphate block batteries. A later official EU page, [BYD's revolutionary Blade Battery](https://www.byd.com/eu/blog/BYDs-revolutionary-Blade-Battery-all-you-need-to-know.html), says the Blade Battery was launched in {fact("March 2020")} and describes this as BYD {fact("CTP (cell-to-pack)")} technology. Partnership language on the announcement page about sharing the technology with global partners is not a patent pledge.
- [e-Platform 3.0](https://en.byd.com/news/byd-debuts-e-platform-3-0-leading-the-next-generation-of-smart-electric-vehicles/) - Officially debuted on {fact("19 April 2021")} at the Shanghai Auto Show. BYD said the platform "will continue to be open to the industry." That is a stated product-platform policy, not an open-source software licence and not a patent pledge. A later official EU page, [Why is BYD's e-Platform 3.0 so special?](https://www.byd.com/eu/blog/Why-is-BYDs-e-Platform-3-0-so-special.html), describes the platform as launched in {fact("September 2021")}. Manufacturer-stated figures from those pages — including {goal("89%")} system efficiency, {goal("800 V")} fast charging, {goal("5 minutes")} of charge for {goal("90 miles")}, a {goal("0.21")} drag coefficient, and a vehicle OS "fully open to developers" — are BYD claims, not measurements made for this list. The same debut release introduced the 2021 Tang DM-i super-hybrid and stated fuel consumption as low as {goal("1.4 gallons per 60 miles")} with a comprehensive range of {goal("600 miles")}.
- [Cell-to-body (CTB)](https://www.byd.com/eu/news-list/BYD_SEAL_Dynamic_and_Intelligent) - Presented with the BYD SEAL on {fact("12 April 2023")}. BYD said SEAL is the first vehicle to implement CTB, integrating the Blade Battery into the body. Stated figures such as {goal("66%")} pack volume utilisation, {goal("10%")} system energy density and {goal("40,500 N·m/degree")} torsional stiffness are BYD claims.
- [Super e-Platform](https://www.byd.com/en/news-list/BYD-Unveils-Super-e-Platform-Megawatt-Flash-Charging-Electric-Vehicles-Matching-Refueling-Speeds) - Unveiled on {fact("17 March 2025")}. BYD described a full-domain {goal("1000 V")} architecture, {goal("1000 kW")} megawatt flash charging, a peak of {goal("2 km")} of range per second, and {goal("400 km")} of range in {goal("5 minutes")}, first on the Han L and Tang L in China. It also said it plans to build over {goal("4,000")} megawatt flash-charging stations in China. Those charging performance figures and the station rollout are BYD's stated specs and plans, not independent measurements.

On open software and developer access, this snapshot found BYD's DiLink / open-innovation site at [oip.byd.com](https://oip.byd.com/) (比亚迪汽车工业有限公司). The page itself did not load from this environment, so its current developer terms were not verified here. No official BYD Company GitHub organisation was verified: `github.com/byd` is a personal account, and `github.com/BYDcar` is not listed here as an official BYD release.

"""


tools = [t for _, ts in C for t in ts]
missing = [t[1] for t in tools if t[1] not in S]
if missing:
    raise SystemExit(f"missing stats for: {missing}")

# unique URLs
urls = [f"https://github.com/{t[1]}" for t in tools]
if len(urls) != len(set(urls)):
    raise SystemExit("duplicate GitHub URLs")

tot = sum(S[t[1]]["stars"] for t in tools)
tot_ex = sum(S[t[1]]["stars"] for t in tools if t[1] != OPENPILOT)
forks = sum(S[t[1]]["forks"] for t in tools)
langs = sorted({S[t[1]]["lang"] for t in tools if S[t[1]]["lang"] not in ("", "none")})
active = sum(1 for t in tools if S[t[1]]["push"] >= ACTIVE_SINCE)

o = []
o.append(
    f"""<div align="center">

# Awesome Craft EV [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of open-source software and hardware for electric vehicles and charging.

<img src="assets/craft-ev.svg" alt="Pixel-art electric vehicle at a generic charge point, with charge pulses on the cable and a filling battery" width="100%">

![Tools](https://img.shields.io/badge/tools-{len(tools)}-6366f1?style=for-the-badge)
[![Categories](https://img.shields.io/badge/categories-{len(C)}-0ea5e9?style=for-the-badge)](#contents)
[![Combined stars](https://img.shields.io/badge/combined_stars-{k(tot)}-f59e0b?style=for-the-badge&logo=github)](#-leaderboard)
[![Stars](https://img.shields.io/github/stars/EdisonTKPcom/Awesome-Craft-EV?style=for-the-badge&color=22c55e)](https://github.com/EdisonTKPcom/Awesome-Craft-EV/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/EdisonTKPcom/Awesome-Craft-EV?style=for-the-badge&color=ec4899)](https://github.com/EdisonTKPcom/Awesome-Craft-EV/commits/main)

</div>

Open-source tools now cover most of the EV stack: charge-point backends, station firmware, home energy management, battery and motor hardware, vehicle telemetry, and the models used to study packs and routes. Every entry below has a public repository that was checked on {AS}. Check each project's licence before you deploy, manufacture or sell anything built on it.

**Safety:** several hardware projects here work at pack, inverter or charger voltages. High-voltage and mains work needs qualified handling, the right personal protective equipment, and isolation procedures. This list is not instructions, training or a substitute for that.

Malaysia's public charging networks (including JomCharge, ChargeSini and chargEV) are commercial products. This snapshot did not find a verified, maintained open-source CSMS or driver app published by those networks, so no Malaysia-specific entry is listed.

Related lists: [Awesome Craft](https://github.com/EdisonTKPcom/Awesome-Craft), [Awesome Craft Hardware](https://github.com/EdisonTKPcom/Awesome-Craft-Hardware).

## Contents
"""
)
o += ["- [Dashboard](#dashboard)"] + [f"- [{n}](#{anchor(n)})" for n, _ in C]
o += ["- [Open patents and pledges](#open-patents-and-pledges)"]
o.append("\n## Dashboard\n")
o.append(
    f"""<style>
.ev-fact{{border-bottom:3px solid #0f172a;padding-bottom:1px}}
.ev-goal{{border-bottom:3px dashed #0f172a;padding-bottom:1px}}
.ev-est{{border-bottom:3px dotted #0f172a;padding-bottom:1px}}
</style>

<table>
<tr>
<td align="center"><h2>{fact(str(len(tools)))}</h2>listed projects</td>
<td align="center"><h2>{fact(str(len(C)))}</h2>categories</td>
<td align="center"><h2>{estimate(k(tot))}</h2>combined GitHub stars</td>
<td align="center"><h2>{estimate(k(forks))}</h2>combined forks</td>
<td align="center"><h2>{estimate(f"{active}/{len(tools)}")}</h2>pushed in the last 30 days</td>
<td align="center"><h2>{fact(str(len(langs)))}</h2>languages</td>
</tr>
</table>

**Evidence tags**

<table>
<tr><th>Tag</th><th>Style</th><th>Meaning</th></tr>
<tr><td><span class="ev-fact">FACT</span></td><td>solid underline</td><td>A measured figure, with the source named.</td></tr>
<tr><td><span class="ev-goal">GOAL</span></td><td>dashed underline</td><td>A stated roadmap or plan, not a result.</td></tr>
<tr><td><span class="ev-est">ESTIMATE</span></td><td>dotted underline</td><td>A sum or count we computed from the facts.</td></tr>
</table>

This snapshot's dashboard has no GOAL figures. None of the dashboard numbers come from project roadmaps. GOAL tags are used later, in the Open patents and pledges section, for stated plans and manufacturer claims.

**Sources and method**

- Star counts, fork counts, licences, primary languages and last-push dates are {fact("FACT")} values from the GitHub REST API (`GET /repos/{{owner}}/{{repo}}`) on {AS}.
- Combined stars ({estimate(k(tot))}) and combined forks ({estimate(k(forks))}) are {estimate("ESTIMATE")}s: the arithmetic sum of those per-repository FACT counts, with no weighting and no unique-user deduplication. A person who stars two projects is counted twice.
- Combined stars excluding openpilot: {estimate(k(tot_ex))}. openpilot is ADAS software and contributes {fact(k(S[OPENPILOT]["stars"]))} of the total, so the list total is shown both with and without it.
- Pushed in the last 30 days ({estimate(f"{active}/{len(tools)}")}) is an {estimate("ESTIMATE")}: the number of listed repositories whose FACT `pushed_at` date is on or after {ACTIVE_SINCE}.
- Language and category counts, and the licence badges, are {estimate("ESTIMATE")}s of FACT fields. Star badges next to each entry update live and may differ from this snapshot.
"""
)
top = sorted(tools, key=lambda t: -S[t[1]]["stars"])[:10]
mx = S[top[0][1]]["stars"]
o.append(
    '### 🏆 Leaderboard\n\nStar counts in this table are FACT values from the snapshot. The bars are only a visual scale.\n\n<table>\n<tr><th>Rank</th><th>Project</th><th>Kind</th><th align="right">Stars</th><th></th></tr>'
)
kind = {t[1]: n for n, ts in C for t in ts}
for i, t in enumerate(top, 1):
    s = S[t[1]]["stars"]
    bar = "█" * max(1, round(s / mx * 20))
    medal = ["🥇", "🥈", "🥉"][i - 1] if i < 4 else i
    o.append(
        f'<tr><td align="center">{medal}</td><td><b>{t[0]}</b></td><td>{kind[t[1]]}</td><td align="right">{fact(k(s))}</td><td><code>{bar}</code></td></tr>'
    )
o.append("</table>\n")
o.append("\n### Stars by category\n")
o.append(
    "These category totals are ESTIMATE sums of the per-repository FACT star counts.\n\n```mermaid\npie showData\n    title Combined GitHub stars by category"
)
for n, ts in C:
    o.append(f'    "{n}" : {sum(S[t[1]]["stars"] for t in ts)}')
o.append("```\n")
lc = {}
for t in tools:
    L = LICNAME.get(S[t[1]]["lic"], S[t[1]]["lic"])
    lc[L] = lc.get(L, 0) + 1
o.append(
    "### Licences\n\n"
    + " ".join(
        f"![{L}](https://img.shields.io/badge/{U.quote(str(L).replace('-', '--'))}-{c}-64748b?style=flat-square)"
        for L, c in sorted(lc.items(), key=lambda x: -x[1])
    )
    + "\n\nThese badge counts are ESTIMATE tallies of the SPDX identifier GitHub returned for each repository. "
    + '"Custom" or "None" means GitHub could not match a standard SPDX licence. '
    + "diyBMS v4 uses CC BY-NC-SA 2.0 UK, which is not an OSI licence. "
    + "OICP uses CC-BY-SA-4.0, a content licence rather than a typical OSI software licence. "
    + "Read each project licence before you use it commercially.\n"
)
for n, ts in C:
    o.append(f"## {n}\n")
    for t in sorted(ts, key=lambda t: t[0].lower()):
        desc = t[2]
        if not desc.endswith("."):
            desc += "."
        o.append(
            f"- [{t[0]}](https://github.com/{t[1]}) - {desc} ![Stars](https://img.shields.io/github/stars/{t[1]}?style=flat-square&label=%E2%AD%90)"
        )
    o.append("")
o.append(patents_section())
o.append(
    "## Contributing\n\nContributions welcome! Read the [contribution guidelines](contributing.md) first.\n\n"
    '<div align="center">\n\n'
    "If this list helped you find a tool, give it a ⭐ so others can find it.\n\n"
    "</div>\n"
)
(ROOT / "README.md").write_text("\n".join(o))
print(
    f"wrote README.md tools={len(tools)} stars={tot} stars_ex_openpilot={tot_ex} "
    f"forks={forks} langs={len(langs)} active={active}/{len(tools)}"
)
# print per-category counts for the report
for n, ts in C:
    print(f"  {n}: {len(ts)}  stars={sum(S[t[1]]['stars'] for t in ts)}")
