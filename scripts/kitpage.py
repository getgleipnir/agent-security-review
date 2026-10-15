"""Render the static Kit page (site/index.html) from checklist.yaml.

Called by build.py. No JavaScript framework, no external requests: fonts are
self-hosted and the page works offline.
"""
from __future__ import annotations

import html
import re

STATUS = [
    ("evidenced", "Evidenced: we can show it today"),
    ("partial", "Partly: some evidence, gaps remain"),
    ("policy_only", "Policy only: a statement, no proof"),
    ("missing", "Not in place"),
    ("not_applicable", "Not applicable"),
]

CONF = {"verified": "verified", "secondary": "secondary source", "title-only": "title only"}


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def blanks(text: str) -> str:
    """Escape, then render [placeholders] as fill-in blanks."""
    return re.sub(r"\[([^\]]+)\]", r'<span class="blank">\1</span>', esc(text))


def render_item(item: dict, fws: dict) -> str:
    iid = item["id"]
    hard = item["often_unevidenced"]
    refs = []
    for r in item["references"]:
        fw = fws[r["fw"]]
        ref = esc(r["ref"])
        if r.get("url"):
            ref = f'<a href="{esc(r["url"])}" rel="noopener">{ref}</a>'
        refs.append(f'<li><span class="fw">{esc(fw["short"])}</span> {ref}: {esc(r["note"])} '
                    f'<span class="conf">({CONF[r["confidence"]]})</span></li>')
    evidence = "".join(f"<li>{esc(e)}</li>" for e in item["evidence"])
    not_enough = "".join(f"<li>{esc(e)}</li>" for e in item["not_enough"])
    note = f'<p class="note">{esc(item["note"])}</p>' if item.get("note") else ""
    search = " ".join([iid, item["question"], item["why"], item["strong_answer"], item["template_answer"],
                       *item["evidence"], *item["not_enough"],
                       *(f'{fws[r["fw"]]["short"]} {r["ref"]} {r["note"]}' for r in item["references"])]).lower()
    flag = '<span class="flag">Hard to evidence today</span>' if hard else ""
    return f"""
<details class="item" id="{iid.lower()}" data-hard="{str(hard).lower()}" data-search="{esc(search)}">
  <summary><span class="iid">{iid}</span><span class="q">{esc(item["question"])}</span>{flag}</summary>
  <div class="body">
    <section><h4>Why buyers ask</h4><p>{esc(item["why"])}</p></section>
    <section class="strong"><h4>What a strong answer looks like</h4><p>{esc(item["strong_answer"])}</p></section>
    <section><h4>Evidence to attach</h4><ul>{evidence}</ul></section>
    {f'<section class="weak"><h4>Not enough on its own</h4><ul>{not_enough}</ul></section>' if not_enough else ""}
    <section class="template"><h4>Template answer</h4>
      <p class="hint">Fill every blank with what your system actually does. If a sentence isn't true for you, delete it and say what you do instead.</p>
      <p class="form" data-raw="{esc(item["template_answer"])}">{blanks(item["template_answer"])}</p>
      <button type="button" class="copy">Copy template</button>
    </section>
    {note}
    <details class="refs"><summary>Framework references ({len(item["references"])})</summary><ul>{"".join(refs)}</ul></details>
  </div>
</details>"""


def render_site(data: dict) -> str:
    fws = data["frameworks"]
    nav, groups = [], []
    for g in data["groups"]:
        items = [i for i in data["items"] if i["group"] == g["id"] and not i.get("deprecated")]
        gid = g["id"].lower()
        nav.append(f'<li><a href="#g-{gid}">{esc(g["title"])} <span class="n">{len(items)}</span></a></li>')
        groups.append(f"""
<section class="group" id="g-{gid}">
  <h2>{esc(g["title"])}</h2>
  <p class="gsum">{esc(g["summary"])}</p>
  {"".join(render_item(i, fws) for i in items)}
</section>""")
    n_items = sum(1 for i in data["items"] if not i.get("deprecated"))
    fw_list = "".join(
        f'<li><a href="{esc(f["url"])}" rel="noopener">{esc(f["name"])}</a> <span class="conf">{esc(f["version"])}</span></li>'
        for f in fws.values())
    return TEMPLATE.format(
        version=esc(data["version"]), updated=esc(data["updated"]), n_items=n_items, n_groups=len(data["groups"]),
        n_fw=len(fws), nav="".join(nav), groups="".join(groups), fw_list=fw_list,
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent Security Review Kit</title>
<meta name="description" content="The questions banks, insurers and enterprise security teams ask AI agent vendors before production, with what a strong answer looks like, what evidence to attach and a template answer.">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; base-uri 'none'; form-action 'none'">
<style>
@font-face {{ font-family: "Public Sans"; src: url("fonts/public-sans-latin-wght-normal.woff2") format("woff2");
  font-weight: 100 900; font-display: swap; }}
:root {{
  --paper: #eef1f4; --surface: #ffffff; --ink: #14213d; --muted: #4d5b70; --rule: #c9d2dc;
  --accent: #0f6e6a; --accent-soft: #e1f0ee; --caution: #8a5100; --caution-soft: #fbf0df; --blank: #dfe6ee;
  color-scheme: light;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --paper: #0e1622; --surface: #152031; --ink: #e6ecf2; --muted: #a3b0c2; --rule: #2a3a50;
    --accent: #5cc4bb; --accent-soft: #15322f; --caution: #e3a852; --caution-soft: #34270f; --blank: #233348;
    color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
  --paper: #0e1622; --surface: #152031; --ink: #e6ecf2; --muted: #a3b0c2; --rule: #2a3a50;
  --accent: #5cc4bb; --accent-soft: #15322f; --caution: #e3a852; --caution-soft: #34270f; --blank: #233348;
  color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{ margin: 0; background: var(--paper); color: var(--ink);
  font: 400 17px/1.55 "Public Sans", system-ui, -apple-system, "Segoe UI", sans-serif; }}
a {{ color: var(--accent); text-underline-offset: 2px; }}
:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 2px; border-radius: 3px; }}
.wrap {{ max-width: 1120px; margin: 0 auto; padding: 0 16px; }}
header.top {{ padding: 56px 0 32px; }}
h1 {{ font-size: clamp(34px, 6vw, 56px); line-height: 1.05; font-weight: 750; letter-spacing: -0.02em; margin: 0 0 16px;
  max-width: 14ch; }}
.lede {{ font-size: 20px; line-height: 1.5; color: var(--muted); max-width: 62ch; margin: 0 0 28px; }}
.downloads {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 0 0 12px; padding: 0; list-style: none; }}
.downloads a {{ display: inline-block; padding: 10px 16px; border: 1.5px solid var(--ink); border-radius: 6px;
  color: var(--ink); text-decoration: none; font-weight: 600; font-size: 15px; background: var(--surface); }}
.downloads a.primary {{ background: var(--ink); color: var(--paper); }}
.downloads a:hover {{ border-color: var(--accent); }}
.meta {{ font-size: 14px; color: var(--muted); margin: 0; }}
.how {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin: 8px 0 40px; padding: 24px 0;
  border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); counter-reset: step; list-style: none; }}
.how li {{ counter-increment: step; font-size: 15px; color: var(--muted); }}
.how li::before {{ content: counter(step); display: block; font-weight: 750; font-size: 22px; color: var(--accent); }}
.how strong {{ color: var(--ink); display: block; font-size: 16px; }}
.layout {{ display: grid; grid-template-columns: 240px minmax(0, 1fr); gap: 48px; align-items: start; }}
nav.groups {{ position: sticky; top: 16px; font-size: 15px; }}
nav.groups ul {{ list-style: none; margin: 0; padding: 0; }}
nav.groups a {{ display: flex; justify-content: space-between; gap: 8px; padding: 6px 0; color: var(--ink);
  text-decoration: none; border-bottom: 1px solid var(--rule); }}
nav.groups a:hover {{ color: var(--accent); }}
nav.groups .n {{ color: var(--muted); font-variant-numeric: tabular-nums; }}
.tools {{ display: flex; flex-wrap: wrap; gap: 12px 20px; align-items: center; margin: 0 0 24px; }}
.tools input[type=search] {{ flex: 1 1 260px; font: inherit; font-size: 16px; padding: 10px 12px; color: var(--ink);
  background: var(--surface); border: 1.5px solid var(--rule); border-radius: 6px; }}
.tools label {{ font-size: 15px; display: flex; gap: 8px; align-items: center; cursor: pointer; }}
.tools button, .copy {{ font: inherit; font-size: 14px; font-weight: 600; padding: 7px 12px; border-radius: 6px;
  border: 1.5px solid var(--rule); background: var(--surface); color: var(--ink); cursor: pointer; }}
.tools button:hover, .copy:hover {{ border-color: var(--accent); }}
#count {{ font-size: 14px; color: var(--muted); }}
.group {{ margin: 0 0 48px; }}
.group h2 {{ font-size: 26px; line-height: 1.2; font-weight: 700; margin: 0 0 4px; letter-spacing: -0.01em; }}
.gsum {{ color: var(--muted); margin: 0 0 16px; max-width: 66ch; }}
details.item {{ background: var(--surface); border: 1px solid var(--rule); border-radius: 8px; margin: 0 0 10px; }}
details.item > summary {{ list-style: none; cursor: pointer; display: grid; grid-template-columns: 76px 1fr;
  gap: 4px 12px; padding: 16px 18px; }}
details.item > summary::-webkit-details-marker {{ display: none; }}
.iid {{ font-weight: 700; font-size: 14px; color: var(--accent); padding-top: 3px; font-variant-numeric: tabular-nums;
  letter-spacing: 0.02em; }}
.q {{ font-weight: 600; font-size: 18px; line-height: 1.4; }}
.flag {{ grid-column: 2; justify-self: start; font-size: 13px; font-weight: 600; color: var(--caution);
  background: var(--caution-soft); padding: 2px 8px; border-radius: 4px; }}
details.item[open] > summary {{ border-bottom: 1px solid var(--rule); }}
.body {{ padding: 4px 18px 18px 106px; }}
.body section {{ margin: 16px 0 0; max-width: 68ch; }}
.body h4 {{ font-size: 14px; font-weight: 700; margin: 0 0 4px; color: var(--muted); }}
.body p {{ margin: 0; }}
.body ul {{ margin: 0; padding-left: 20px; }}
.body li {{ margin: 2px 0; }}
.body a, footer a {{ overflow-wrap: anywhere; }}
.strong p {{ border-left: 3px solid var(--accent); padding-left: 12px; }}
.weak li::marker {{ color: var(--caution); }}
.template .form {{ background: var(--paper); border: 1px dashed var(--rule); border-radius: 6px; padding: 14px 16px;
  line-height: 1.9; }}
.blank {{ background: var(--blank); border-bottom: 1.5px solid var(--muted); padding: 1px 5px; border-radius: 2px;
  color: var(--muted); font-size: 0.92em;
  -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
.copy {{ margin-top: 8px; }}
.hint {{ font-size: 14px; color: var(--muted); margin: 0 0 8px !important; }}
.note {{ font-size: 15px; color: var(--muted); margin-top: 16px !important; }}
details.refs {{ margin-top: 16px; font-size: 14px; }}
details.refs summary {{ cursor: pointer; color: var(--muted); font-weight: 600; }}
details.refs ul {{ margin-top: 8px; }}
.fw {{ font-weight: 600; }}
.conf {{ color: var(--muted); }}
footer {{ border-top: 1px solid var(--rule); padding: 32px 0 56px; margin-top: 24px; font-size: 15px; color: var(--muted); }}
footer h2 {{ font-size: 18px; color: var(--ink); margin: 0 0 8px; }}
footer ul {{ padding-left: 20px; margin: 0 0 20px; }}
.hidden {{ display: none !important; }}
@media (max-width: 860px) {{
  .layout {{ grid-template-columns: minmax(0, 1fr); gap: 0; }}
  nav.groups {{ position: static; margin: 0 0 20px; min-width: 0; }}
  nav.groups ul {{ display: flex; gap: 8px; overflow-x: auto; padding-bottom: 6px; }}
  nav.groups a {{ white-space: nowrap; border: 1px solid var(--rule); border-radius: 999px; padding: 6px 12px;
    background: var(--surface); }}
  .how {{ grid-template-columns: 1fr; gap: 16px; }}
  details.item > summary {{ grid-template-columns: 1fr; padding: 14px; }}
  .flag {{ grid-column: 1; }}
  .body {{ padding: 4px 14px 16px; }}
}}
@media print {{
  body {{ background: #fff; color: #000; font-size: 11pt; }}
  .downloads, .tools, nav.groups, .copy, .how {{ display: none !important; }}
  .layout {{ display: block; }}
  header.top {{ padding: 0 0 12pt; }}
  details.item {{ border-color: #bbb; }}
  details.item > summary, .body section {{ break-inside: avoid; }}
  details.item > summary {{ break-after: avoid; }}
  .group h2 {{ break-after: avoid; }}
  .hidden {{ display: block !important; }}
}}
@media (prefers-reduced-motion: reduce) {{ * {{ scroll-behavior: auto !important; }} }}
</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <h1>Agent Security Review Kit</h1>
  <p class="lede">The questions banks, insurers and enterprise security teams ask before an AI agent goes into production.
  For each one: why they ask, what a strong answer looks like, what evidence to attach, and a template answer you can adapt.</p>
  <ul class="downloads">
    <li><a class="primary" href="downloads/answers-template.csv" download>Fill in (CSV)</a></li>
    <li><a href="downloads/answers-template.json" download>Fill in (JSON)</a></li>
    <li><a href="downloads/agent-security-review-kit.pdf" download>PDF</a></li>
    <li><a href="downloads/checklist.md" download>Markdown</a></li>
    <li><a href="https://github.com/getgleipnir/agent-security-review">Source on GitHub</a></li>
  </ul>
  <p class="meta">Version {version}, updated {updated}. {n_items} questions in {n_groups} areas, mapped to {n_fw} frameworks. Free to use under CC BY 4.0.</p>
</header>

<ol class="how">
  <li><strong>Download the fill-in sheet</strong>Every question with an empty answer, status and evidence column.</li>
  <li><strong>Answer with evidence</strong>Start from the template answer, replace each blank, attach the evidence listed.</li>
  <li><strong>Fix the gaps first</strong>Questions marked hard to evidence are where reviews usually stall.</li>
</ol>

<div class="layout">
<nav class="groups" aria-label="Areas"><ul>{nav}</ul></nav>
<main>
  <div class="tools" role="search">
    <input type="search" id="q" placeholder="Search, e.g. kill switch or SOC 2" aria-label="Search questions">
    <label><input type="checkbox" id="hard"> Hard to evidence only</label>
    <button type="button" id="expand">Expand all</button>
    <span id="count" aria-live="polite"></span>
  </div>
  {groups}
</main>
</div>

<footer>
  <h2>How the references were checked</h2>
  <p>Each framework reference is marked <em>verified</em> (checked against the primary text), <em>secondary source</em>
  (primary is gated, checked against a reliable secondary source) or <em>title only</em>. Paraphrases are ours and short;
  read the source before relying on one. This kit is not legal advice and does not certify compliance with anything.</p>
  <h2>Frameworks</h2>
  <ul>{fw_list}</ul>
  <p>Maintained by <a href="https://getgleipnir.com">Gleipnir</a>. Suggest a question you were asked in a real review on
  <a href="https://github.com/getgleipnir/agent-security-review/issues/new?template=add-question.yml">GitHub</a>.</p>
</footer>
</div>
<script>
(function () {{
  var items = Array.prototype.slice.call(document.querySelectorAll("details.item"));
  var q = document.getElementById("q"), hard = document.getElementById("hard");
  var count = document.getElementById("count"), expand = document.getElementById("expand");
  function apply() {{
    var term = q.value.trim().toLowerCase(), shown = 0;
    items.forEach(function (el) {{
      var ok = (!term || el.dataset.search.indexOf(term) !== -1) && (!hard.checked || el.dataset.hard === "true");
      el.classList.toggle("hidden", !ok);
      if (ok) shown++;
    }});
    document.querySelectorAll("section.group").forEach(function (g) {{
      g.classList.toggle("hidden", !g.querySelector("details.item:not(.hidden)"));
    }});
    count.textContent = shown === items.length ? items.length + " questions" : shown + " of " + items.length;
  }}
  q.addEventListener("input", apply);
  hard.addEventListener("change", apply);
  expand.addEventListener("click", function () {{
    var open = expand.textContent === "Expand all";
    items.forEach(function (el) {{ el.open = open; }});
    expand.textContent = open ? "Collapse all" : "Expand all";
  }});
  document.addEventListener("click", function (e) {{
    var b = e.target.closest(".copy");
    if (!b) return;
    var text = b.parentNode.querySelector(".form").dataset.raw;
    var done = function () {{ b.textContent = "Copied"; setTimeout(function () {{ b.textContent = "Copy template"; }}, 1500); }};
    var fallback = function () {{
      var r = document.createRange(); r.selectNodeContents(b.parentNode.querySelector(".form"));
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      b.textContent = "Selected: press Ctrl+C or Cmd+C";
    }};
    if (navigator.clipboard && window.isSecureContext !== false) navigator.clipboard.writeText(text).then(done, fallback);
    else fallback();
  }});
  function openHash() {{
    var el = location.hash && document.getElementById(location.hash.slice(1));
    if (el && el.tagName === "DETAILS") {{ el.open = true; el.scrollIntoView(); }}
  }}
  window.addEventListener("hashchange", openHash);
  window.addEventListener("beforeprint", function () {{ items.forEach(function (el) {{ el.open = true; }}); }});
  openHash(); apply();
}})();
</script>
</body>
</html>
"""
