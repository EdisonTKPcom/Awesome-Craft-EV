#!/usr/bin/env python3
import csv
import urllib.parse as U
from pathlib import Path

ROOT = Path(__file__).resolve().parent
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

This snapshot has no GOAL figures. None of the dashboard numbers come from project roadmaps.

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
