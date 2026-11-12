"""Builds every animated SVG used by README.md into ./assets/dark and
./assets/light. The README picks one or the other with <picture>, so the
panels follow the reader's GitHub theme.

Run from the repo root:   python scripts/build_assets.py

Edit the data blocks (INFO, PROJECTS, SECTIONS), the THEMES colors, or
scripts/ascii_art.txt and re-run. Everything is plain SVG + CSS keyframes,
which is what GitHub allows inside a README: no scripts, no external fonts.
"""

from pathlib import Path
from types import SimpleNamespace
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assets"
W = 760

MONO = ('ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,'
        '"Liberation Mono","DejaVu Sans Mono",monospace')

# Dark: off-white #f1ede6, tan #bba590, cream #f9ebc7 and sky blue #5ab1ef
# on GitHub's own near-black. Light: no background at all, just a border in
# that same near-black, with black text and portrait. (#1a73c7 is the blue
# deepened so it stays readable on a white page.)
THEMES = {
    "dark": dict(
        BG="#0d1117", EDGE="#30363d",
        INK="#f1ede6", DIM="#948a7b",
        KEY="#5ab1ef", VALUE="#f9ebc7",
        ART="#bba590", ART_HI="#f9ebc7",
        RULE="#1f4a70", LEAD="#2f6a9c",
        ACCENT="#f9ebc7",
        WELL="#1b4a73", WELL_EDGE="#2a6396", CELL_OFF="#173f63", CELL_ON="#f9ebc7",
        WIP="#5ab1ef", LIVE="#f9ebc7",
    ),
    "light": dict(
        BG="none", EDGE="#0d1117",
        INK="#0d1117", DIM="#59636e",
        KEY="#1a73c7", VALUE="#0d1117",
        ART="#0d1117", ART_HI="#1a73c7",
        RULE="#c3d3e3", LEAD="#9fb6cd",
        ACCENT="#0d1117",
        WELL="none", WELL_EDGE="#0d1117", CELL_OFF="#dbe7f3", CELL_ON="#1a73c7",
        WIP="#1a73c7", LIVE="#0d1117",
    ),
}
C = SimpleNamespace(**THEMES["dark"])  # the theme being built

BASE_CSS = f"""
text{{font-family:{MONO}}}
.b{{font-weight:700}}
@keyframes blink{{0%,49%{{fill-opacity:1}}50%,100%{{fill-opacity:0}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.cur{{animation:blink 1.1s step-end infinite}}
.pulse{{animation:pulse 2.2s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""


def svg(h, body, css="", title=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
        f'viewBox="0 0 {W} {h}" role="img">\n'
        f"<title>{escape(title)}</title>\n"
        f"<style>{BASE_CSS}{css}</style>\n"
        f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="12" '
        f'fill="{C.BG}" stroke="{C.EDGE}"/>\n'
        f"{body}\n</svg>\n"
    )


def mono(x, y, s, fill, size, bold=False, extra=""):
    """Text locked to a character grid (0.6em per glyph) whatever font the
    viewer has, so columns and dotted leaders line up everywhere."""
    s_xml = escape(s).replace(" ", " ")
    cls = ' class="b"' if bold else ""
    return (f'<text{cls} x="{x:.1f}" y="{y}" font-size="{size}" fill="{fill}" '
            f'textLength="{len(s) * size * 0.6:.1f}" lengthAdjust="spacing"{extra}>{s_xml}</text>')


# --------------------------------------------------------------------------
# The card: neofetch-style. ASCII portrait on the left, facts on the right.
# --------------------------------------------------------------------------

USER, HOST = "marce", "byt3marc"

# A string is a section rule, a tuple is a "key: ..... value" line,
# None is a blank line. Keep key + value under ~50 characters.
INFO = [
    ("OS", "Windows 11, Kali Linux, Android"),
    ("Host", "UTEC, Lima, Perú"),
    ("Kernel", "Cybersecurity student"),
    ("IDE", "VS Code"),
    None,
    ("Languages.Code", "Python, TypeScript, JS, C++, Java"),
    ("Languages.Markup", "HTML, CSS"),
    ("Languages.Real", "Spanish, English"),
    None,
    "Learning",
    ("Learning.Networks", "TCP/IP, DNS, HTTP"),
    ("Learning.Web", "OWASP Top 10"),
    ("Learning.Tools", "Kali, Burp Suite, Wireshark, Nmap"),
    ("Learning.Practice", "CTFs, Python automation"),
    None,
    "Projects",
    ("Projects.Mobile", "PocketAnt"),
    ("Projects.Desktop", "MRC-Launcher, BM-MCL"),
    ("Projects.Web", "Emulator-GBA, MGL"),
    None,
    "Contact",
    ("Email", "marcelo.revilla@utec.edu.pe"),
    ("GitHub", "byt3marc"),
]


def neofetch():
    size, lh = 11.67, 16
    cw = size * 0.6
    art = (HERE / "ascii_art.txt").read_text(encoding="utf-8").splitlines()
    while art and not art[0].strip():
        art.pop(0)
    art_cols, info_cols = 42, 58
    ax = 18
    ix = ax + (art_cols + 3) * cw
    right = ix + info_cols * cw
    lines = 1 + len(INFO)
    y0 = 36
    height = y0 + (lines - 1) * lh + 24
    art_y = y0 + ((lines - len(art)) // 2) * lh

    css = f"""
@keyframes on{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes wave{{0%,7%,100%{{fill:{C.ART}}}3.5%{{fill:{C.ART_HI}}}}}
.ln{{animation:on .45s ease-out both}}
.art{{animation:on .45s ease-out both,wave 9s linear infinite}}
"""
    p = []
    for r, row in enumerate(art):
        if not row.strip():
            continue
        p.append(mono(ax, art_y + r * lh, row, C.ART, size,
                      extra=f' class="art" style="animation-delay:{0.15 + r * 0.06:.2f}s,{3.5 + r * 0.1:.2f}s"'))

    def rule(x, y):
        return f'<path d="M{x:.1f} {y - 4}H{right:.1f}" stroke="{C.RULE}"/>'

    def line(i, parts):
        return f'<g class="ln" style="animation-delay:{0.15 + i * 0.06:.2f}s">{"".join(parts)}</g>'

    y = y0
    head = f"{USER}@{HOST}"
    p.append(line(0, [
        mono(ix, y, USER, C.KEY, size, bold=True),
        mono(ix + len(USER) * cw, y, "@", C.DIM, size),
        mono(ix + (len(USER) + 1) * cw, y, HOST, C.KEY, size, bold=True),
        rule(ix + (len(head) + 1) * cw, y),
    ]))
    for i, item in enumerate(INFO, start=1):
        y = y0 + i * lh
        if item is None:
            continue
        if isinstance(item, str):
            p.append(line(i, [
                mono(ix, y, "-", C.DIM, size),
                mono(ix + 2 * cw, y, item, C.INK, size, bold=True),
                rule(ix + (len(item) + 3) * cw, y),
            ]))
            continue
        key, value = item
        dots = info_cols - (2 + len(key) + 1 + 1) - (len(value) + 1)
        assert dots >= 3, f"line too long for the card: {key}"
        p.append(line(i, [
            mono(ix, y, ".", C.LEAD, size),
            mono(ix + 2 * cw, y, key + ":", C.KEY, size),
            mono(ix + (2 + len(key) + 2) * cw, y, "." * dots, C.LEAD, size),
            mono(right - len(value) * cw, y, value, C.VALUE, size),
        ]))
    return svg(height, "\n".join(p), css, f"{head}: profile card in the style of neofetch")


# --------------------------------------------------------------------------
# Section rules ("- Projects ------") and the closing prompt
# --------------------------------------------------------------------------

SECTIONS = [  # (file, title)
    ("s-projects", "Projects"),
    ("s-certificates", "Certificates"),
    ("s-contact", "Contact"),
]


def section(title):
    size = 15
    cw = size * 0.6
    start, end = 20 + (len(title) + 3) * cw, 740
    span = end - start
    css = (f"@keyframes run{{from{{stroke-dashoffset:{span + 18:.0f}}}to{{stroke-dashoffset:0}}}}"
           f".spark{{stroke-dasharray:18 {span:.0f};animation:run 5s linear infinite}}")
    body = "\n".join([
        mono(20, 26, "-", C.KEY, size, bold=True),
        mono(20 + 2 * cw, 26, title, C.INK, size, bold=True),
        f'<path d="M{start:.1f} 21.5H{end}" stroke="{C.RULE}"/>',
        f'<path class="spark" d="M{start:.1f} 21.5H{end}" stroke="{C.ACCENT}" '
        f'stroke-width="1.5" stroke-linecap="round"/>',
    ])
    return svg(42, body, css, title)


def footer():
    size = 15
    cw = size * 0.6
    head = f"{USER}@{HOST}"
    body = "\n".join([
        mono(20, 26, head, C.KEY, size, bold=True),
        mono(20 + len(head) * cw, 26, ":~$", C.DIM, size),
        mono(20 + (len(head) + 4) * cw, 26, "exit", C.INK, size),
        f'<rect class="cur" x="{20 + (len(head) + 9) * cw:.1f}" y="13" width="{cw:.1f}" '
        f'height="17" fill="{C.ACCENT}"/>',
    ])
    return svg(42, body, "", "End of file")


# --------------------------------------------------------------------------
# Project cards: dot-matrix icon, "name ....... status", two lines, stack
# --------------------------------------------------------------------------

def cells(rows, order):
    """Lit cells of an 8x8 icon, sorted by the order they should draw in."""
    lit = [(c, r) for r, row in enumerate(rows) for c, bit in enumerate(row) if bit == "#"]
    return sorted(lit, key=order)


ICONS = {
    # three bars, each growing from the baseline
    "bars": cells(["........", "...##...", "...##...", "...##.##",
                   "...##.##", "##.##.##", "##.##.##", "##.##.##"],
                  lambda p: (p[0] // 3, -p[1], p[0])),
    # play
    "play": cells(["........", ".##.....", ".####...", ".######.",
                   ".######.", ".####...", ".##.....", "........"],
                  lambda p: (p[0], p[1])),
    # three layers, built from the core up
    "layers": cells(["########", "########", "........", "########",
                     "########", "........", "########", "########"],
                    lambda p: (-(p[1] // 3), p[0], p[1])),
    # d-pad and two buttons
    "pad": cells(["........", "..#.....", "..#....#", "#####...",
                  "..#...#.", "..#.....", "........", "........"],
                 lambda p: (p[0] > 4, abs(p[0] - 2) + abs(p[1] - 3), p[1], p[0])),
}

# status kind: "wip" (pulsing dot), "live" (solid dot), "done" (dim)
PROJECTS = [  # (file, title, icon, status, kind, line 1, line 2, stack)
    ("p-pocketant", "PocketAnt", "bars", "preparing Google Play release", "wip",
     "Expense tracker for the small daily spends (gastos hormiga).",
     "Charts, recurring charges, on-device AI. Nothing leaves the phone.",
     "typescript · react native · expo · on-device gemma"),
    ("p-bm-mcl", "BM-MCL", "layers", "rewrite in progress", "wip",
     "Ground-up rewrite of MRC-Launcher: a QML interface, a testable",
     "core, and Microsoft or offline accounts.",
     "python · pyside6 · qml"),
    ("p-mrc-launcher", "MRC-Launcher", "play", "the original", "done",
     "A lightweight Minecraft launcher: pick a version, manage your",
     "skin and name, play.",
     "python · customtkinter"),
    ("p-emulator-gba", "Emulator-GBA", "pad", "live on GitHub Pages", "live",
     "A web page that plays Game Boy Advance ROMs in the browser.",
     "Nothing to install.",
     "html · runs client-side"),
]


def card(title, icon, status, kind, line1, line2, stack):
    lit = ICONS[icon]
    css = ("@keyframes cell{0%{opacity:0}3%,82%{opacity:1}88%,100%{opacity:0}}"
           ".c{animation:cell 7s linear infinite backwards}")
    ix, iy, pitch = 24, 24, 10
    p = [
        f'<defs><pattern id="m" x="{ix}" y="{iy}" width="{pitch}" height="{pitch}" '
        f'patternUnits="userSpaceOnUse"><rect x="1" y="1" width="8" height="8" rx="1.5" '
        f'fill="{C.CELL_OFF}"/></pattern></defs>',
        f'<rect x="16.5" y="16.5" width="95" height="95" rx="8" fill="{C.WELL}" stroke="{C.WELL_EDGE}"/>',
        f'<rect x="{ix}" y="{iy}" width="80" height="80" fill="url(#m)"/>',
    ]
    for n, (c, r) in enumerate(lit):
        p.append(f'<rect class="c" style="animation-delay:{n * 0.05:.2f}s" x="{ix + c * pitch + 1}" '
                 f'y="{iy + r * pitch + 1}" width="8" height="8" rx="1.5" fill="{C.CELL_ON}"/>')

    title_end = 132 + len(title) * 20 * 0.6
    status_x = 722 - len(status) * 13 * 0.6
    dot_fill = {"wip": C.WIP, "live": C.LIVE, "done": C.DIM}[kind]
    dot_cls = ' class="pulse"' if kind == "wip" else ""
    p += [
        mono(132, 43, title, C.KEY, 20, bold=True),
        f'<path d="M{title_end + 12:.1f} 39H{status_x - 10:.1f}" stroke="{C.LEAD}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-dasharray=".1 7.7"/>',
        mono(status_x, 43, status, C.DIM if kind == "done" else C.VALUE, 13),
        f'<circle{dot_cls} cx="735" cy="38.5" r="4" fill="{dot_fill}"/>',
        f'<text x="132" y="70" font-size="15" fill="{C.INK}">{escape(line1)}</text>',
        f'<text x="132" y="91" font-size="15" fill="{C.INK}">{escape(line2)}</text>',
        f'<text x="132" y="114" font-size="13" fill="{C.DIM}">{escape(stack)}</text>',
    ]
    return svg(128, "\n".join(p), css, f"{title}: {line1} {line2}")


def build(theme):
    global C
    C = SimpleNamespace(**THEMES[theme])
    out = OUT / theme
    out.mkdir(parents=True, exist_ok=True)
    files = {"card": neofetch(), "footer": footer()}
    files.update({name: section(title) for name, title in SECTIONS})
    files.update({name: card(*rest) for name, *rest in PROJECTS})
    for name, content in files.items():
        (out / f"{name}.svg").write_text(content, encoding="utf-8", newline="\n")
    print(f"  assets/{theme}/  {len(files)} files, "
          f"{sum(len(c) for c in files.values()) / 1024:.0f} KB")


if __name__ == "__main__":
    print("Building README assets:")
    for theme in THEMES:
        build(theme)
