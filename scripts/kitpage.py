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


BRAND_SVG = ('<svg viewBox="0 0 34 30" aria-hidden="true"><g fill="none" stroke="#C9A45C" stroke-linecap="round">'
             '<path d="M3 23 C 9 5, 16 30, 21 13 S 31 8, 31 8" stroke-width="3"/>'
             '<path d="M3 27 C 9 11, 16 34, 21 18 S 31 13, 31 13" stroke-opacity=".5" stroke-width="1.8"/></g></svg>')


def header(active: str, prefix: str = "") -> str:
    """Site header shared by the Kit and the Scanner. prefix is the path back to site/."""
    def link(href: str, label: str, key: str) -> str:
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="wrap top">
  <a class="brand" href="https://getgleipnir.com" aria-label="Gleipnir home">{BRAND_SVG}GLEIPNIR</a>
  <nav class="nav" aria-label="Main">
    {link(prefix + "index.html", "Review Kit", "kit")}
    {link(prefix + "scanner/index.html", "Readiness Scanner", "scanner")}
    <a href="https://github.com/getgleipnir/agent-security-review">GitHub</a>
    <a class="cta" href="{prefix}index.html#downloads">Get the sheet</a>
  </nav>
</header>"""


def footer() -> str:
    return """<footer class="wrap foot">
  <span>Free under CC BY 4.0. Not legal advice; does not certify compliance with anything.</span>
  <nav aria-label="More">
    <a href="https://github.com/getgleipnir/agent-security-review">Source</a>
    <a href="https://github.com/getgleipnir/agent-security-review/issues/new?template=add-question.yml">Suggest a question</a>
    <a href="https://getgleipnir.com">getgleipnir.com</a>
  </nav>
</footer>"""


def render_item(item: dict, fws: dict) -> str:
    iid = item["id"]
    hard = item["often_unevidenced"]
    refs = []
    for r in item["references"]:
        fw = fws[r["fw"]]
        ref = esc(r["ref"])
        if r.get("url"):
            ref = f'<a href="{esc(r["url"])}" rel="noopener">{ref}</a>'
        refs.append(f'<li><b>{esc(fw["short"])}</b> {ref}: {esc(r["note"])} '
                    f'<span class="conf">{CONF[r["confidence"]]}</span></li>')
    evidence = "".join(f"<li>{esc(e)}</li>" for e in item["evidence"])
    not_enough = "".join(f"<li>{esc(e)}</li>" for e in item["not_enough"])
    note = f'<dt>Note</dt><dd class="muted">{esc(item["note"])}</dd>' if item.get("note") else ""
    search = " ".join([iid, item["question"], item["why"], item["strong_answer"], item["template_answer"],
                       *item["evidence"], *item["not_enough"],
                       *(f'{fws[r["fw"]]["short"]} {r["ref"]} {r["note"]}' for r in item["references"])]).lower()
    flag = '<span class="pill stop">Hard to evidence</span>' if hard else ""
    weak = f'<dt>Not enough on its own</dt><dd><ul class="weak">{not_enough}</ul></dd>' if not_enough else ""
    return f"""
<details class="item" id="{iid.lower()}" data-hard="{str(hard).lower()}" data-search="{esc(search)}">
  <summary><span class="iid">{iid}</span><span class="q">{esc(item["question"])}</span>{flag}</summary>
  <dl class="rec body">
    <dt>Why buyers ask</dt><dd>{esc(item["why"])}</dd>
    <dt>Strong answer</dt><dd class="strong">{esc(item["strong_answer"])}</dd>
    <dt>Evidence to attach</dt><dd><ul>{evidence}</ul></dd>
    {weak}
    <dt>Template answer</dt>
    <dd class="template">
      <p class="form" data-raw="{esc(item["template_answer"])}">{blanks(item["template_answer"])}</p>
      <div class="tpl-foot"><button type="button" class="btn small copy">Copy template</button>
      <span class="hint">Fill every blank with what your system really does. Delete anything that isn't true.</span></div>
    </dd>
    {note}
    <dt>Frameworks</dt>
    <dd><details class="refs"><summary>{len(item["references"])} references</summary><ul>{"".join(refs)}</ul></details></dd>
  </dl>
</details>"""


def render_site(data: dict) -> str:
    fws = data["frameworks"]
    nav, groups = [], []
    for g in data["groups"]:
        items = [i for i in data["items"] if i["group"] == g["id"] and not i.get("deprecated")]
        gid = g["id"].lower()
        nav.append(f'<li><a href="#g-{gid}">{esc(g["title"])}<span class="n">{len(items)}</span></a></li>')
        groups.append(f"""
<div class="group" id="g-{gid}">
  <h3>{esc(g["title"])}</h3>
  <p class="gsum">{esc(g["summary"])}</p>
  {"".join(render_item(i, fws) for i in items)}
</div>""")
    live = [i for i in data["items"] if not i.get("deprecated")]
    fw_list = "".join(
        f'<li><a href="{esc(f["url"])}" rel="noopener">{esc(f["name"])}</a><span class="conf">{esc(f["version"])}</span></li>'
        for f in fws.values())
    return TEMPLATE.format(
        version=esc(data["version"]), updated=esc(data["updated"]), n_items=len(live), n_groups=len(data["groups"]),
        n_fw=len(fws), n_hard=sum(1 for i in live if i["often_unevidenced"]), nav="".join(nav),
        groups="".join(groups), fw_list=fw_list, header=header("kit"), footer=footer(),
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent Security Review Kit</title>
<meta name="description" content="The questions banks, insurers and enterprise security teams ask AI agent vendors before production, with what a strong answer looks like, what evidence to attach and a template answer.">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; base-uri 'none'; form-action 'none'">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/brand.css">
<style>
.anatomy .rec {{ font-size: 0.92rem; }}
.anatomy .rec dt {{ font-family: var(--mono); font-size: 0.84rem; padding-top: 2px; }}
.anatomy .q-big {{ font-family: var(--serif); font-size: 1.35rem; line-height: 1.3; margin-bottom: 16px; }}
.counts {{ display: flex; flex-wrap: wrap; gap: 8px 22px; font-size: 0.95rem; color: var(--soft); }}
.counts b {{ font-family: var(--serif); font-weight: 400; font-size: 1.6rem; color: var(--gold); margin-right: 6px; }}
.head2 {{ display: flex; flex-direction: column; gap: 14px; margin-bottom: 36px; max-width: 46em; }}
.head2 p {{ color: var(--soft); }}
.dl-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; margin-top: 8px; }}
.dl {{ display: flex; flex-direction: column; gap: 6px; padding: 18px; border: 1px solid var(--line); border-radius: 12px;
  background: var(--bg-2); text-decoration: none; }}
.dl:hover {{ border-color: var(--gold); color: var(--text); }}
.dl b {{ font-weight: 600; }}
.dl span {{ font-size: 0.9rem; color: var(--muted); }}
.dl em {{ font-style: normal; font-family: var(--mono); font-size: 0.8rem; color: var(--gold); }}
.layout {{ display: grid; grid-template-columns: 230px minmax(0, 1fr); gap: 48px; align-items: start; }}
.areas {{ position: sticky; top: 16px; font-size: 0.95rem; }}
.areas ul {{ list-style: none; padding: 0; }}
.areas a {{ display: flex; justify-content: space-between; gap: 8px; padding: 7px 0; text-decoration: none;
  color: var(--soft); border-bottom: 1px solid var(--line); }}
.areas a:hover {{ color: var(--gold-lit); }}
.areas .n {{ color: var(--muted); font-variant-numeric: tabular-nums; }}
.tools {{ display: flex; flex-wrap: wrap; gap: 12px 18px; align-items: center; margin-bottom: 28px; }}
.tools input[type=search] {{ flex: 1 1 260px; font: inherit; padding: 11px 14px; color: var(--text); background: var(--bg-2);
  border: 1px solid var(--line); border-radius: 7px; }}
.tools input[type=search]::placeholder {{ color: var(--muted); }}
.tools input[type=search]:focus {{ border-color: var(--gold); outline: none; }}
.tools label {{ display: flex; gap: 8px; align-items: center; font-size: 0.95rem; color: var(--soft); cursor: pointer; }}
.tools input[type=checkbox] {{ accent-color: var(--gold); width: 16px; height: 16px; }}
#count {{ font-size: 0.9rem; color: var(--muted); }}
.group {{ margin-bottom: 44px; }}
.group h3 {{ font-family: var(--serif); font-weight: 400; font-size: 1.7rem; line-height: 1.2; }}
.gsum {{ color: var(--muted); margin: 4px 0 16px; max-width: 40em; }}
details.item {{ background: var(--bg-2); border: 1px solid var(--line); border-radius: 12px; margin-bottom: 10px; }}
details.item[open] {{ border-color: #4a4434; }}
details.item > summary {{ list-style: none; cursor: pointer; display: grid; grid-template-columns: 70px minmax(0, 1fr) auto;
  gap: 4px 14px; align-items: baseline; padding: 16px 20px; }}
details.item > summary::-webkit-details-marker {{ display: none; }}
details.item > summary:hover .q {{ color: var(--gold-lit); }}
.iid {{ font-family: var(--mono); font-size: 0.85rem; color: var(--gold); }}
.q {{ font-size: 1.05rem; font-weight: 500; line-height: 1.45; }}
details.item[open] > summary {{ border-bottom: 1px solid var(--line); }}
.body {{ padding: 20px 20px 22px; font-size: 0.98rem; }}
.body dt {{ font-size: 0.88rem; }}
.body ul {{ margin: 0; padding-left: 18px; }}
.body li {{ margin: 2px 0; }}
.body .strong {{ border-left: 2px solid var(--ok); padding-left: 12px; }}
.weak li::marker {{ color: var(--stop); }}
.template .form {{ background: var(--bg); border: 1px dashed var(--line); border-radius: 8px; padding: 14px 16px;
  line-height: 1.85; }}
.tpl-foot {{ display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: center; margin-top: 10px; }}
.hint {{ font-size: 0.85rem; color: var(--muted); }}
.muted {{ color: var(--muted); }}
details.refs summary {{ cursor: pointer; color: var(--soft); }}
details.refs ul {{ margin-top: 8px; font-size: 0.9rem; }}
.conf {{ color: var(--muted); margin-left: 6px; font-size: 0.85em; }}
.fws ul {{ columns: 2; column-gap: 40px; padding-left: 18px; color: var(--soft); font-size: 0.95rem; }}
.fws li {{ break-inside: avoid; margin-bottom: 8px; }}
.fws .conf {{ display: block; margin: 0; }}
.fws p {{ color: var(--soft); max-width: 46em; margin-bottom: 24px; }}
@media (max-width: 900px) {{
  .dl-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .layout {{ grid-template-columns: minmax(0, 1fr); gap: 0; }}
  .areas {{ position: static; min-width: 0; margin-bottom: 20px; }}
  .areas ul {{ display: flex; gap: 8px; overflow-x: auto; padding-bottom: 6px; }}
  .areas a {{ white-space: nowrap; border: 1px solid var(--line); border-radius: 999px; padding: 6px 12px; gap: 8px; }}
  .fws ul {{ columns: 1; }}
}}
@media (max-width: 720px) {{
  details.item > summary {{ grid-template-columns: minmax(0, 1fr); padding: 14px 16px; }}
  details.item > summary .pill {{ justify-self: start; }}
  .body {{ padding: 16px; }}
  .dl-grid {{ grid-template-columns: minmax(0, 1fr); }}
}}
@media print {{
  :root {{ --bg: #fff; --bg-2: #fff; --bg-3: #fff; --line: #c8c8c8; --text: #111; --soft: #222; --muted: #555;
    --gold: #7a5a1c; --gold-lit: #7a5a1c; --gold-soft: #f3ead6; --ok: #1d6a4d; --stop: #a1271e; color-scheme: light; }}
  body {{ font-size: 10.5pt; }}
  .top .nav, .skip, .tools, .areas, .copy, .hint, .dl-grid, .hero .btns, .anatomy, .steps-sec {{ display: none !important; }}
  .hero-grid, .layout {{ display: block; }}
  section {{ padding-block: 14pt; }}
  .hero {{ padding-top: 0; }}
  details.item {{ border-color: #bbb; }}
  details.item > summary, .rec dt, .template .form {{ break-inside: avoid; }}
  .screen-only {{ display: none !important; }}
  .group h3 {{ break-after: avoid; }}
  .hidden {{ display: block !important; }}
  details.item, details.item > * {{ display: block; }}
  .rec {{ display: block; }}
  .rec dt {{ margin-top: 8pt; break-after: avoid; }}
}}
</style>
</head>
<body>
{header}
<main id="main">
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">Agent Security Review Kit</p>
      <h1>Know the questions before the security review asks them.</h1>
      <p class="lede">Banks, insurers and enterprise security teams ask AI agent vendors the same things before production.
      Here they are, with why they ask, what a strong answer looks like, what evidence to attach, and a template answer to start from.</p>
      <div class="btns">
        <a class="btn primary" href="downloads/answers-template.csv" download>Download the answer sheet</a>
        <a class="btn" href="#questions">Browse the questions</a>
      </div>
      <p class="counts"><span><b>{n_items}</b>questions</span><span><b>{n_groups}</b>areas</span><span><b>{n_fw}</b>frameworks cited</span><span><b>{n_hard}</b>hard to evidence</span></p>
    </div>
    <div class="card anatomy" aria-label="What each question contains">
      <div class="card-top"><span>question ACC-02</span><span class="pill stop">hard to evidence</span></div>
      <p class="q-big">Which identity performed each write in our systems?</p>
      <dl class="rec">
        <dt>why they ask</dt><dd>Shared accounts make the agent look like a staff member in the buyer's logs.</dd>
        <dt>strong answer</dt><dd>One identity per deployment, recorded on every action.</dd>
        <dt>evidence</dt><dd>A record joined to the buyer's own audit log.</dd>
        <dt>template</dt><dd>Agent actions run under <span class="blank">identity</span>, which appears in your <span class="blank">system</span> audit logs.</dd>
        <dt>frameworks</dt><dd>FINOS, AIUC-1, CSA AARM, NYDFS 500, SOC 2</dd>
      </dl>
      <p class="card-note">Every question in the kit has these parts.</p>
    </div>
  </div>
</section>

<section class="steps-sec">
  <div class="wrap">
    <ol class="steps">
      <li><h3>Download the answer sheet</h3><p>Every question with empty columns for status, answer and evidence link.</p></li>
      <li><h3>Answer with evidence</h3><p>Start from the template, fill each gold blank with what your system really does, attach the evidence listed.</p></li>
      <li><h3>Close the gaps first</h3><p>The {n_hard} questions marked hard to evidence are where reviews usually stall. Fix or plan those before the call.</p></li>
    </ol>
  </div>
</section>

<section id="questions">
  <div class="wrap">
    <div class="head2">
      <p class="eyebrow">The questions</p>
      <h2>What buyers ask, and what a good answer contains.</h2>
      <p class="screen-only">Open a question to see the full answer guide. Search finds words in the question, the answers and the framework references.</p>
    </div>
    <div class="layout">
      <nav class="areas" aria-label="Areas"><ul>{nav}</ul></nav>
      <div>
        <div class="tools" role="search">
          <input type="search" id="q" placeholder="Search, e.g. kill switch or SOC 2" aria-label="Search questions">
          <label><input type="checkbox" id="hard"> Hard to evidence only</label>
          <button type="button" class="btn small" id="expand">Expand all</button>
          <span id="count" aria-live="polite"></span>
        </div>
        {groups}
      </div>
    </div>
  </div>
</section>

<section id="downloads">
  <div class="wrap">
    <div class="head2">
      <p class="eyebrow">Downloads</p>
      <h2>Take it into your review.</h2>
      <p>Version {version}, updated {updated}. Free to use and adapt under CC BY 4.0.</p>
    </div>
    <div class="dl-grid">
      <a class="dl" href="downloads/answers-template.csv" download><em>CSV</em><b>Answer sheet</b><span>Status, answer and evidence link per question. Opens in Excel or Sheets.</span></a>
      <a class="dl" href="downloads/answers-template.json" download><em>JSON</em><b>Answer file</b><span>Same sheet for tools. The Readiness Scanner reads it.</span></a>
      <a class="dl" href="downloads/agent-security-review-kit.pdf" download><em>PDF</em><b>Full kit</b><span>Every question with its answer guide, to print or attach.</span></a>
      <a class="dl" href="downloads/checklist.md" download><em>Markdown</em><b>Full kit</b><span>For your wiki, repo or questionnaire tool.</span></a>
    </div>
  </div>
</section>

<section class="fws">
  <div class="wrap">
    <div class="head2">
      <p class="eyebrow">Sources</p>
      <h2>Every reference, and how we checked it.</h2>
    </div>
    <p>Each reference is marked verified (checked against the primary text), secondary source (the primary is gated,
    checked against a reliable secondary source) or title only. Paraphrases are ours and short; read the source before relying on one.</p>
    <ul>{fw_list}</ul>
  </div>
</section>
</main>
{footer}
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
    document.querySelectorAll(".group").forEach(function (g) {{
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
    var box = b.closest(".template").querySelector(".form");
    var done = function () {{ b.textContent = "Copied"; setTimeout(function () {{ b.textContent = "Copy template"; }}, 1500); }};
    var fallback = function () {{
      var r = document.createRange(); r.selectNodeContents(box);
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      b.textContent = "Selected: press Ctrl+C";
    }};
    if (navigator.clipboard && window.isSecureContext !== false) navigator.clipboard.writeText(box.dataset.raw).then(done, fallback);
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
