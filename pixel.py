#!/usr/bin/env python3
"""EV charging pixel banner for Awesome Craft EV. Original scene, no brand marks."""
import random
from pathlib import Path

random.seed(42)
P = 8
W = 100
H = 34  # 800x272
out = []

def r(x, y, w, h, c, cls=None, extra=""):
    a = f' class="{cls}"' if cls else ""
    out.append(
        f'<rect x="{x*P}" y="{y*P}" width="{w*P}" height="{h*P}" fill="{c}"{a}{extra}/>'
    )

# 3x5 pixel font
F = {
    "A": ["010", "101", "111", "101", "101"],
    "C": ["011", "100", "100", "100", "011"],
    "E": ["111", "100", "110", "100", "111"],
    "F": ["111", "100", "110", "100", "100"],
    "R": ["110", "101", "110", "101", "101"],
    "T": ["111", "010", "010", "010", "010"],
    "V": ["101", "101", "101", "101", "010"],
    " ": ["000", "000", "000", "000", "000"],
}

style = """
<style>
.tw{animation:tw 2.4s steps(2) infinite}
.tw2{animation:tw 3.1s steps(2) infinite .8s}
.tw3{animation:tw 1.9s steps(2) infinite 1.4s}
@keyframes tw{0%,100%{opacity:1}50%{opacity:.15}}
.glow{animation:glow 1.4s steps(3) infinite}
.glow2{animation:glow 1.8s steps(3) infinite .5s}
@keyframes glow{0%,100%{opacity:.35}50%{opacity:1}}
.blink{animation:tw 1s steps(1) infinite}
.pulse{animation:pulse 1.8s linear infinite}
.pulse2{animation:pulse 1.8s linear infinite .6s}
.pulse3{animation:pulse 1.8s linear infinite 1.2s}
@keyframes pulse{0%{opacity:0}15%{opacity:1}70%{opacity:1}100%{opacity:0}}
.fill{transform-box:fill-box;transform-origin:left center;animation:fill 3.6s ease-in-out infinite}
@keyframes fill{0%{transform:scaleX(.2)}70%,100%{transform:scaleX(1)}}
.cell{animation:cell 3.6s steps(1) infinite}
.cell2{animation:cell 3.6s steps(1) infinite .9s}
.cell3{animation:cell 3.6s steps(1) infinite 1.8s}
.cell4{animation:cell 3.6s steps(1) infinite 2.7s}
@keyframes cell{0%,20%{opacity:.2}25%,100%{opacity:1}}
.led{animation:led 1.2s steps(2) infinite}
.led2{animation:led 1.6s steps(2) infinite .4s}
@keyframes led{0%,100%{opacity:1}50%{opacity:.2}}
</style>
"""

# Dusk sky over a charging bay
sky = ["#071018", "#0a1622", "#0d1e30", "#10263c", "#133048", "#163854", "#1a4260"]
for i, c in enumerate(sky):
    r(0, i * 4, W, 4, c)

# Sparse evening stars, keep the title band clear
for i in range(22):
    while True:
        x = random.randrange(W)
        y = random.randrange(10)
        if not (28 <= x <= 72 and y <= 8):
            break
    r(x, y, 1, 1, random.choice(["#7dd3fc", "#fff7c2", "#86efac"]), random.choice(["tw", "tw2", "tw3"]))

# Soft moon
r(88, 3, 5, 5, "#1e3a4c")
r(89, 4, 3, 3, "#cbd5e1")
r(90, 5, 1, 1, "#f8fafc")

# Title: CRAFT EV
t = "CRAFT EV"
tx = (W - len(t) * 4) // 2
ty = 2
for k, ch in enumerate(t):
    for yy, row in enumerate(F[ch]):
        for xx, b in enumerate(row):
            if b == "1":
                r(tx + k * 4 + xx + 0.25, ty + yy + 0.25, 1, 1, "#000", None, ' opacity=".55"')
                r(tx + k * 4 + xx, ty + yy, 1, 1, "#5eead4")

# Distant canopy / charging bay roof
r(8, 11, 84, 1, "#1f3d4d")
r(10, 10, 80, 1, "#2a5566")
for x in range(12, 90, 12):
    r(x, 11, 1, 14, "#1e3340")

# Charger pedestal on the left
# base
r(16, 24, 10, 2, "#334155")
r(17, 25, 8, 1, "#1e293b")
# body
r(18, 14, 6, 11, "#0f172a")
r(18, 14, 6, 1, "#475569")
r(18, 14, 1, 11, "#334155")
r(23, 14, 1, 11, "#020617")
# screen
r(19, 15, 4, 5, "#042f2e")
r(20, 16, 2, 1, "#2dd4bf", "glow")
r(20, 18, 1, 2, "#22c55e", "led")
r(21, 18, 1, 1, "#38bdf8", "led2")
# holster / head
r(24, 16, 3, 3, "#1e293b")
r(25, 17, 2, 2, "#0ea5e9", "glow")
r(26, 17, 1, 1, "#ecfeff", "glow2")

# Charge cable from holster down, across the bay, up into the car inlet
# path in tile coords
cable = []
# down from holster
for y in range(19, 24):
    cable.append((27, y))
# across the floor
for x in range(27, 48):
    cable.append((x, 23))
# up to inlet
for y in range(23, 19, -1):
    cable.append((47, y))
cable.append((48, 19))
for x, y in cable:
    r(x, y, 1, 1, "#164e63")

# Animated charge pulses travelling along the cable
# Place three pulse rects at the start; CSS could translate, but tile-step
# opacity animation with staggered delays on key cable points is simpler
# and stays on the cable path.
pulse_cls = ["pulse", "pulse2", "pulse3"]
pulse_col = ["#67e8f9", "#5eead4", "#fde047"]
# pick every nth point as a pulse lamp; staggered classes create a travelling look
for i, (x, y) in enumerate(cable):
    if i % 5 == 0:
        r(x, y, 1, 1, pulse_col[(i // 5) % 3], pulse_cls[(i // 5) % 3])

# Generic compact EV on the right (boxy hatch, no badges)
# shadow
r(50, 25, 32, 1, "#0b1220")
# tyres
r(54, 23, 4, 3, "#111827")
r(55, 24, 2, 2, "#334155")
r(74, 23, 4, 3, "#111827")
r(75, 24, 2, 2, "#334155")
# body lower
r(51, 19, 32, 5, "#1e3a5f")
r(52, 19, 30, 4, "#2563eb")
# cabin / glass
r(58, 15, 18, 5, "#1e3a5f")
r(59, 16, 16, 4, "#082f49")
r(60, 17, 6, 2, "#38bdf8", "glow")
r(68, 17, 5, 2, "#0ea5e9")
# roof
r(59, 15, 16, 1, "#1d4ed8")
# nose and tail lights
r(51, 20, 1, 2, "#fbbf24", "glow")
r(81, 20, 2, 2, "#ef4444", "led")
# charge inlet on the front quarter, glowing
r(48, 19, 2, 2, "#0f172a")
r(49, 19, 1, 2, "#22d3ee", "glow")

# Battery pack graphic above the car / on a sign to the right of the title area
# A large battery with filling cells, sitting on a small post near the charger
r(32, 14, 14, 7, "#0f172a")
r(32, 14, 14, 1, "#475569")
r(46, 16, 1, 3, "#64748b")  # terminal
# empty track
r(33, 16, 12, 4, "#1e293b")
# filling bar (scales from the left)
r(33, 16, 12, 4, "#16a34a", "fill")
# four cells overlaid so the fill is readable as segments
for i, cls in enumerate(["cell", "cell2", "cell3", "cell4"]):
    r(34 + i * 3, 17, 2, 2, "#4ade80", cls)

# Operator standing by the charger (generic figure, no uniform marks)
r(13, 20, 2, 2, "#f1c27d")  # head
r(14, 21, 1, 1, "#0f172a")  # eye
r(13, 22, 2, 3, "#0f766e")  # body
r(13, 25, 1, 1, "#111827")
r(14, 25, 1, 1, "#111827")

# Ground / bay floor
for x in range(W):
    r(x, 26, 1, 1, "#22c55e" if x % 5 == 0 else "#14532d")
    r(x, 27, 1, 1, "#0f172a" if x % 2 else "#1e293b")
    for y in range(28, H):
        if (x + y) % 4 == 0:
            r(x, y, 1, 1, "#1e293b")
        else:
            r(x, y, 1, 1, "#0b1220")

# Status bar
out.append(
    f'<text x="{8}" y="{H*P-8}" font-family="monospace" font-size="12" fill="#5eead4">'
    f"&gt; charging with open-source tools"
    f'<tspan class="blink">_</tspan></text>'
)

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W*P} {H*P}" '
    f'width="{W*P}" height="{H*P}" shape-rendering="crispEdges">'
    + style
    + "".join(out)
    + "</svg>"
)

dest = Path(__file__).resolve().parent / "assets" / "craft-ev.svg"
dest.write_text(svg)
print(f"wrote {dest} ({dest.stat().st_size} bytes)")
