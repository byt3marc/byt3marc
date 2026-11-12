"""Writes preview.html: README.md rendered the way GitHub shows it, so you
can check it before pushing.

Run from the repo root:   python scripts/preview.py
Then open preview.html in a browser. Re-run after editing README.md.
(preview.html is only for you; it does not need to go to GitHub.)
"""

import json
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>README preview</title>
<style>
:root{--bg:#0d1117;--fg:#e6edf3;--muted:#9198a1;--line:#30363d;--link:#4493f8;--chip:#151b23}
:root[data-theme=light]{--bg:#fff;--fg:#1f2328;--muted:#59636e;--line:#d1d9e0;--link:#0969da;--chip:#f6f8fa}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif}
header{display:flex;gap:12px;align-items:center;max-width:894px;margin:0 auto;padding:16px 24px 0;color:var(--muted);font-size:13px}
button{font:inherit;color:var(--fg);background:var(--chip);border:1px solid var(--line);border-radius:6px;padding:4px 10px;cursor:pointer}
main{max-width:846px;margin:16px auto 64px;padding:24px;border:1px solid var(--line);border-radius:6px}
img{max-width:100%;vertical-align:middle} a{color:var(--link);text-decoration:none} a:hover{text-decoration:underline}
p,ul,table{margin:0 0 16px} ul{padding-left:2em} h3{margin:24px 0 16px;font-size:20px}
table{border-collapse:collapse;display:block;max-width:100%;overflow:auto}
th,td{border:1px solid var(--line);padding:6px 13px} tr:nth-child(2n) td{background:var(--chip)}
code{background:var(--chip);padding:.2em .4em;border-radius:6px;font:85% ui-monospace,Consolas,monospace}
kbd{background:var(--chip);border:1px solid var(--line);border-bottom-width:2px;border-radius:6px;padding:3px 5px;font:11px ui-monospace,Consolas,monospace;vertical-align:middle}
@media (max-width:600px){main{border:0;padding:16px;margin-top:0}}
</style></head><body>
<header><span>README.md &middot; local preview</span>
<button id="t" type="button">Light / dark</button></header>
<main id="out">Loading the Markdown renderer (needs internet the first time)...</main>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script>
const md = __README__;
document.getElementById("out").innerHTML = marked.parse(md, {gfm: true});
// GitHub shows the <picture> source that matches its theme; do the same here.
function apply(theme) {
  document.documentElement.dataset.theme = theme;
  document.querySelectorAll("picture source").forEach((s) => {
    s.dataset.media = s.dataset.media || s.media;
    s.media = s.dataset.media.includes(theme) ? "all" : "not all";
  });
}
const asked = new URLSearchParams(location.search).get("theme");
apply(asked || (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark"));
document.getElementById("t").onclick = () =>
  apply(document.documentElement.dataset.theme === "light" ? "dark" : "light");
</script></body></html>
"""

if __name__ == "__main__":
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    out = ROOT / "preview.html"
    out.write_text(PAGE.replace("__README__", json.dumps(readme).replace("</", "<\\/")),
                   encoding="utf-8", newline="\n")
    print(f"Wrote {out}")
    webbrowser.open(out.as_uri())
