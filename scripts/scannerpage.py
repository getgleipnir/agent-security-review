"""Render the Agent Readiness Scanner (site/scanner/index.html) from checklist.yaml.

A static page: the questions are embedded as JSON, scoring runs in the browser,
nothing is sent or stored. The shareable link keeps the answers in the URL
fragment, which browsers never send to a server.
"""
from __future__ import annotations

import json

from kitpage import esc, footer, header

# Points per status. not_applicable is left out of the score.
POINTS = {"evidenced": 1.0, "partial": 0.5, "policy_only": 0.25, "missing": 0.0}
CHOICES = [
    ("evidenced", "Yes, with evidence"),
    ("partial", "Partly"),
    ("policy_only", "Policy only"),
    ("missing", "No"),
    ("not_applicable", "Doesn't apply"),
]


def scanner_data(data: dict) -> dict:
    groups = {g["id"]: g["title"] for g in data["groups"]}
    items = []
    for i in data["items"]:
        if i.get("deprecated"):
            continue
        sc = i.get("scanner")
        items.append({
            "id": i["id"],
            "area": i["group"],
            "core": sc is not None,
            "check": sc["check"] if sc else i["question"],
            "gap": sc["gap"] if sc else i["why"],
            "strong": i["strong_answer"],
            "hard": i["often_unevidenced"],
        })
    return {
        "version": data["version"],
        "areas": [{"id": g["id"], "title": groups[g["id"]]} for g in data["groups"]],
        "items": items,
        "points": POINTS,
        "choices": [{"key": k, "label": v} for k, v in CHOICES],
    }


def render_scanner(data: dict) -> str:
    payload = json.dumps(scanner_data(data), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    n_core = sum(1 for i in data["items"] if i.get("scanner") and not i.get("deprecated"))
    n_all = sum(1 for i in data["items"] if not i.get("deprecated"))
    return TEMPLATE.replace("{{HEADER}}", header("scanner", "../")).replace("{{FOOTER}}", footer()) \
        .replace("{{DATA}}", payload).replace("{{N_CORE}}", str(n_core)).replace("{{N_ALL}}", str(n_all)) \
        .replace("{{VERSION}}", esc(data["version"]))


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent Readiness Scanner</title>
<meta name="description" content="Answer {{N_CORE}} questions about your AI agent and see how ready it is for a bank, insurer or enterprise security review. Runs in your browser; nothing is sent or stored.">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="no-referrer">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../assets/brand.css">
<style>
html { scroll-padding-bottom: 90px; }
.privacy { display: flex; gap: 10px; align-items: flex-start; font-size: 0.92rem; color: var(--soft); }
.privacy svg { flex: none; margin-top: 3px; }
.preview .gauge-row { display: flex; gap: 22px; align-items: center; margin-bottom: 18px; }
.gauge { position: relative; width: 120px; height: 120px; flex: none; }
.gauge svg { width: 100%; height: 100%; transform: rotate(-90deg); }
.gauge .num { position: absolute; inset: 0; display: grid; place-items: center; font-family: var(--serif);
  font-size: 2.4rem; line-height: 1; }
.gauge.big { width: 168px; height: 168px; }
.gauge.big .num { font-size: 3.4rem; }
.track { stroke: var(--line); }
.arc { transition: stroke-dashoffset 0.6s ease; }
.band { font-family: var(--serif); font-size: 1.5rem; line-height: 1.2; }
.bars { display: grid; gap: 12px; }
.bar-row { display: grid; grid-template-columns: minmax(0, 11em) minmax(0, 1fr) 3.2em; gap: 12px; align-items: center;
  font-size: 0.92rem; }
.bar-row a { color: var(--soft); text-decoration: none; }
.bar-row a:hover { color: var(--gold-lit); }
.bar { height: 8px; border-radius: 4px; background: var(--line); overflow: hidden; }
.bar i { display: block; height: 100%; border-radius: 4px; }
.bar-row .pct { text-align: right; font-variant-numeric: tabular-nums; color: var(--soft); }
.bar-row .na { color: var(--muted); }

.head2 { display: flex; flex-direction: column; gap: 14px; margin-bottom: 32px; max-width: 46em; }
.head2 p { color: var(--soft); }
.import { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 28px; }
.import .hint, .hint { font-size: 0.88rem; color: var(--muted); }
#msg { font-size: 0.9rem; }
#msg.ok { color: var(--ok); } #msg.err { color: var(--stop); }
.qarea { margin-bottom: 36px; }
.qarea h3 { font-family: var(--serif); font-weight: 400; font-size: 1.55rem; margin-bottom: 12px; }
fieldset.qq { border: 1px solid var(--line); border-radius: 12px; background: var(--bg-2); padding: 18px 20px 20px;
  margin: 0 0 10px; min-width: 0; }
fieldset.qq.answered { border-color: #4a4434; }
fieldset.qq legend { float: left; width: 100%; padding: 0; margin-bottom: 14px; display: grid;
  grid-template-columns: 70px minmax(0, 1fr); gap: 4px 14px; }
fieldset.qq legend .iid { font-family: var(--mono); font-size: 0.85rem; color: var(--gold); padding-top: 3px; }
fieldset.qq legend .txt { font-size: 1.05rem; font-weight: 500; line-height: 1.45; }
.opts { clear: both; display: flex; flex-wrap: wrap; gap: 8px; padding-left: 84px; }
.opts label { position: relative; }
.opts input { position: absolute; opacity: 0; inset: 0; margin: 0; cursor: pointer; }
.opts span { display: inline-block; padding: 7px 14px; border: 1px solid var(--line); border-radius: 999px;
  font-size: 0.92rem; color: var(--soft); cursor: pointer; user-select: none; }
.opts label:hover span { border-color: var(--gold); color: var(--text); }
.opts input:focus-visible + span { outline: 3px solid var(--gold); outline-offset: 2px; }
.opts input:checked + span { background: var(--gold); border-color: var(--gold); color: var(--bg); font-weight: 600; }
.opts input[value="missing"]:checked + span { background: var(--stop); border-color: var(--stop); }
.opts input[value="evidenced"]:checked + span { background: var(--ok); border-color: var(--ok); }
.opts input[value="not_applicable"]:checked + span { background: var(--bg-3); border-color: var(--muted); color: var(--text); }
.more { margin: 8px 0 0; }
.dock { position: sticky; bottom: 0; z-index: 5; background: rgba(12, 14, 19, 0.94); border-top: 1px solid var(--line);
  backdrop-filter: blur(6px); }
.dock .wrap { display: flex; align-items: center; gap: 16px; padding-block: 12px; }
.dock .prog { flex: 1; display: flex; align-items: center; gap: 12px; font-size: 0.92rem; color: var(--soft); }
.dock .prog .bar { flex: 1; max-width: 320px; }
.dock .bar i { background: var(--gold); }

.report-top { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 32px; align-items: center; margin-bottom: 40px; }
.report-top .who { display: flex; flex-direction: column; gap: 10px; }
.who input { font: inherit; font-size: 1rem; padding: 9px 12px; color: var(--text); background: var(--bg-2);
  border: 1px solid var(--line); border-radius: 7px; max-width: 360px; }
.who input:focus { border-color: var(--gold); outline: none; }
.who .basis { color: var(--muted); font-size: 0.9rem; }
.report-grid { display: grid; grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: 48px; align-items: start; }
.report h3 { font-family: var(--serif); font-weight: 400; font-size: 1.55rem; margin-bottom: 16px; }
.gaps { list-style: none; padding: 0; display: grid; gap: 10px; }
.gap { border: 1px solid var(--line); border-radius: 12px; background: var(--bg-2); padding: 16px 18px; }
.gap-top { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: baseline; margin-bottom: 6px; }
.gap-top .iid { font-family: var(--mono); font-size: 0.85rem; color: var(--gold); }
.gap-top b { font-weight: 600; flex: 1 1 260px; line-height: 1.45; }
.gap p { color: var(--soft); font-size: 0.95rem; margin-top: 6px; }
.gap .good { border-left: 2px solid var(--ok); padding-left: 10px; color: var(--soft); }
.gap .good b { color: var(--text); font-weight: 600; }
.gap a { font-size: 0.9rem; }
.ok-list { list-style: none; padding: 0; font-size: 0.95rem; color: var(--soft); display: grid; gap: 6px; }
.ok-list .iid { font-family: var(--mono); font-size: 0.85rem; color: var(--ok); margin-right: 8px; }
.actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 28px; }
.empty { color: var(--soft); border: 1px dashed var(--line); border-radius: 12px; padding: 22px; }
.method { margin-top: 40px; font-size: 0.9rem; color: var(--muted); max-width: 52em; }
.method b { color: var(--soft); }

@media (max-width: 900px) {
  .report-grid { grid-template-columns: minmax(0, 1fr); gap: 36px; }
  .report-top { grid-template-columns: minmax(0, 1fr); gap: 20px; }
}
@media (max-width: 720px) {
  fieldset.qq { padding: 16px; }
  fieldset.qq legend { grid-template-columns: minmax(0, 1fr); }
  .opts { padding-left: 0; }
  .bar-row { grid-template-columns: minmax(0, 1fr) 3.2em; }
  .bar-row .bar { grid-column: 1 / -1; grid-row: 2; }
  .dock .prog .bar { display: none; }
}
@media print {
  :root { --bg: #fff; --bg-2: #fff; --bg-3: #f2f2f2; --line: #c8c8c8; --text: #111; --soft: #222; --muted: #555;
    --gold: #7a5a1c; --gold-lit: #7a5a1c; --ok: #1d6a4d; --stop: #a1271e; color-scheme: light; }
  body { font-size: 10.5pt; }
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .report .head2 { display: none; }
  .top .nav, .skip, .hero, #questions, .dock, .actions, .foot nav, .who input { display: none !important; }
  section { padding-block: 0; border: 0 !important; }
  .report-grid { grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: 24pt; }
  .gap, .bar-row { break-inside: avoid; }
  .who .name-print { display: block !important; font-family: var(--serif); font-size: 16pt; }
  .print-title { display: block !important; }
}
.name-print, .print-title { display: none; }
</style>
</head>
<body>
{{HEADER}}
<main id="main">
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">Agent Readiness Scanner</p>
      <h1>How ready is your agent for a security review?</h1>
      <p class="lede">Answer {{N_CORE}} questions banks, insurers and enterprise security teams ask before an AI agent goes
      into production. You get a score per area, the gaps that will stall the review, and a report you can share.</p>
      <div class="btns">
        <a class="btn primary" href="#questions">Start the scan</a>
        <a class="btn" href="#import">Import answers from the Kit</a>
      </div>
      <p class="privacy"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.5 2.5 3.8v3.6c0 3.2 2.3 6 5.5 7.1 3.2-1.1 5.5-3.9 5.5-7.1V3.8L8 1.5Z" fill="none" stroke="#C9A45C" stroke-width="1.4"/><path d="m5.6 8.2 1.7 1.7 3.2-3.3" fill="none" stroke="#C9A45C" stroke-width="1.4" stroke-linecap="round"/></svg>
      <span>Runs entirely in your browser. Nothing is sent or stored; the page cannot make network requests. About two minutes.</span></p>
    </div>
    <div class="card preview" aria-hidden="true">
      <div class="card-top"><span>readiness report, example</span><span class="pill gold">self-assessment</span></div>
      <div class="gauge-row">
        <div class="gauge"><svg viewBox="0 0 120 120"><circle class="track" cx="60" cy="60" r="52" fill="none" stroke-width="9"/><circle cx="60" cy="60" r="52" fill="none" stroke="#C9A45C" stroke-width="9" stroke-linecap="round" stroke-dasharray="326.7" stroke-dashoffset="124"/></svg><span class="num">62</span></div>
        <div><p class="band">Gaps to close</p><p class="hint">4 gaps, 2 of them hard to evidence</p></div>
      </div>
      <div class="bars">
        <div class="bar-row"><span>Access &amp; scope</span><div class="bar"><i style="width:100%;background:var(--ok)"></i></div><span class="pct">100</span></div>
        <div class="bar-row"><span>Tamper evidence</span><div class="bar"><i style="width:25%;background:var(--stop)"></i></div><span class="pct">25</span></div>
        <div class="bar-row"><span>Incidents &amp; kill switch</span><div class="bar"><i style="width:75%;background:var(--gold)"></i></div><span class="pct">75</span></div>
      </div>
    </div>
  </div>
</section>

<section id="questions">
  <div class="wrap">
    <div class="head2">
      <p class="eyebrow">The scan</p>
      <h2>Answer for what you can show today.</h2>
      <p>"Yes, with evidence" means you could hand a reviewer proof right now. A policy or a plan counts as "Policy only".
      Each question links to its full answer guide in the Review Kit.</p>
    </div>
    <div class="import" id="import">
      <label class="btn small" for="file">Import answers (JSON or CSV)</label>
      <input type="file" id="file" accept=".json,.csv,application/json,text/csv" class="hidden">
      <button type="button" class="btn small" id="reset">Clear answers</button>
      <span class="hint">Use the answer sheet from the <a href="../index.html#downloads">Review Kit</a>. The file is read in your browser.</span>
      <span id="msg" role="status"></span>
    </div>
    <div id="form"></div>
    <button type="button" class="btn small more" id="more" aria-expanded="false"></button>
  </div>
</section>

<div class="dock" id="dock">
  <div class="wrap">
    <div class="prog"><span id="prog-text">0 of {{N_CORE}} answered</span><div class="bar"><i id="prog-bar" style="width:0"></i></div></div>
    <a class="btn primary" href="#report" id="see">See report</a>
  </div>
</div>

<section id="report" class="report">
  <div class="wrap">
    <p class="eyebrow print-title">Agent Readiness Scanner, report</p>
    <div class="head2">
      <p class="eyebrow">Your report</p>
      <h2>Your readiness report.</h2>
    </div>
    <div id="report-body"></div>
    <p class="method"><b>How the score works.</b> Each answer earns points: yes with evidence 100, partly 50, policy only 25, no 0.
    "Doesn't apply" is left out. An area's score is the average of its answers; the overall score is the average of all answers.
    This is a self-assessment against the open Agent Security Review Kit (version {{VERSION}}), not an audit or a certification.</p>
  </div>
</section>
</main>
{{FOOTER}}
<script type="application/json" id="data">{{DATA}}</script>
<script>
(function () {
  "use strict";
  var D = JSON.parse(document.getElementById("data").textContent);
  var CODE = { evidenced: "e", partial: "p", policy_only: "o", missing: "m", not_applicable: "n" };
  var DECODE = {}; Object.keys(CODE).forEach(function (k) { DECODE[CODE[k]] = k; });
  var SYN = { yes: "evidenced", evidenced: "evidenced", partly: "partial", partial: "partial", policy: "policy_only",
    policy_only: "policy_only", "policy only": "policy_only", no: "missing", missing: "missing", "n/a": "not_applicable",
    na: "not_applicable", not_applicable: "not_applicable" };
  var answers = {}, extra = {}, showAll = false, name = "";
  var byId = {}; D.items.forEach(function (it) { byId[it.id] = it; });
  var core = D.items.filter(function (it) { return it.core; });

  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function visible() { return D.items.filter(function (it) { return showAll || it.core || answers[it.id]; }); }
  function color(p) { return p >= 80 ? "var(--ok)" : p >= 50 ? "var(--gold)" : "var(--stop)"; }
  function band(p) { return p >= 80 ? "Ready for review" : p >= 50 ? "Gaps to close" : "Not ready yet"; }
  function kitLink(id) { return "../index.html#" + id.toLowerCase(); }

  function renderForm() {
    var form = document.getElementById("form"); form.innerHTML = "";
    var items = visible();
    D.areas.forEach(function (a) {
      var its = items.filter(function (it) { return it.area === a.id; });
      if (!its.length) return;
      var box = el("div", { "class": "qarea" }); box.appendChild(el("h3", null, esc(a.title)));
      its.forEach(function (it) {
        var fs = el("fieldset", { "class": "qq" + (answers[it.id] ? " answered" : ""), id: "q-" + it.id });
        fs.appendChild(el("legend", null, '<span class="iid">' + it.id + '</span><span class="txt">' + esc(it.check) +
          ' <a class="hint" href="' + kitLink(it.id) + '">Kit guide</a></span>'));
        var opts = el("div", { "class": "opts" });
        D.choices.forEach(function (c) {
          var lab = el("label");
          var inp = el("input", { type: "radio", name: it.id, value: c.key });
          if (answers[it.id] === c.key) inp.checked = true;
          inp.addEventListener("change", function () { answers[it.id] = c.key; fs.classList.add("answered"); update(); });
          lab.appendChild(inp); lab.appendChild(el("span", null, c.label)); opts.appendChild(lab);
        });
        fs.appendChild(opts); box.appendChild(fs);
      });
      form.appendChild(box);
    });
    var more = document.getElementById("more");
    var n = D.items.length - core.length;
    more.textContent = showAll ? "Show only the " + core.length + " core questions" : "Add the other " + n + " questions from the Kit";
    more.setAttribute("aria-expanded", String(showAll));
  }

  function scores() {
    var areas = [], all = [];
    D.areas.forEach(function (a) {
      var pts = D.items.filter(function (it) { return it.area === a.id && answers[it.id] && answers[it.id] !== "not_applicable"; })
        .map(function (it) { return D.points[answers[it.id]]; });
      all = all.concat(pts);
      areas.push({ id: a.id, title: a.title, n: pts.length,
        pct: pts.length ? Math.round(100 * pts.reduce(function (x, y) { return x + y; }, 0) / pts.length) : null });
    });
    var overall = all.length ? Math.round(100 * all.reduce(function (x, y) { return x + y; }, 0) / all.length) : null;
    return { areas: areas, overall: overall, counted: all.length };
  }

  function gauge(p, big) {
    var r = big ? 74 : 52, c = 2 * Math.PI * r, size = big ? 168 : 120, w = big ? 11 : 9, h = size / 2;
    var off = p == null ? c : c * (1 - p / 100);
    return '<div class="gauge' + (big ? " big" : "") + '"><svg viewBox="0 0 ' + size + " " + size + '">' +
      '<circle class="track" cx="' + h + '" cy="' + h + '" r="' + r + '" fill="none" stroke-width="' + w + '"/>' +
      '<circle class="arc" cx="' + h + '" cy="' + h + '" r="' + r + '" fill="none" stroke="' + (p == null ? "transparent" : color(p)) +
      '" stroke-width="' + w + '" stroke-linecap="round" stroke-dasharray="' + c.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '"/></svg>' +
      '<span class="num">' + (p == null ? "–" : p) + "</span></div>";
  }

  function renderReport() {
    var s = scores(), body = document.getElementById("report-body");
    var answered = Object.keys(answers).length;
    if (!answered) {
      body.innerHTML = '<p class="empty">Answer at least one question above and your report appears here, updating as you go.</p>';
      return;
    }
    var rank = { missing: 0, policy_only: 1, partial: 2 };
    var gaps = D.items.filter(function (it) { return answers[it.id] in rank; }).sort(function (a, b) {
      return rank[answers[a.id]] - rank[answers[b.id]] || (b.hard - a.hard) || (a.id < b.id ? -1 : 1); });
    var good = D.items.filter(function (it) { return answers[it.id] === "evidenced"; });
    var hardGaps = gaps.filter(function (g) { return g.hard; }).length;
    var label = { missing: "No", policy_only: "Policy only", partial: "Partly" };
    var unanswered = visible().filter(function (it) { return !answers[it.id]; }).length;

    var h = '<div class="report-top">' + gauge(s.overall, true) + '<div class="who">' +
      '<p class="band">' + (s.overall == null ? "Nothing scored yet" : band(s.overall)) + "</p>" +
      '<p class="basis">' + gaps.length + " gap" + (gaps.length === 1 ? "" : "s") + (hardGaps ? ", " + hardGaps + " of them hard to evidence" : "") +
      ". Based on " + s.counted + " scored answer" + (s.counted === 1 ? "" : "s") + (unanswered ? ", " + unanswered + " not answered yet" : "") +
      ". Self-assessment, " + new Date().toISOString().slice(0, 10) + ".</p>" +
      '<p class="name-print">' + esc(name || "") + "</p>" +
      '<input type="text" id="name" placeholder="Company or product (optional, shown on the report)" value="' + esc(name) + '" maxlength="80" aria-label="Company or product name">' +
      "</div></div>";
    h += '<div class="report-grid"><div><h3>By area</h3><div class="bars">';
    s.areas.forEach(function (a) {
      if (a.pct == null && !visible().some(function (it) { return it.area === a.id; })) return;
      h += '<div class="bar-row"><a href="../index.html#g-' + a.id.toLowerCase() + '">' + esc(a.title) + "</a>" +
        (a.pct == null ? '<div class="bar"></div><span class="pct na">–</span>' :
          '<div class="bar"><i style="width:' + a.pct + "%;background:" + color(a.pct) + '"></i></div><span class="pct">' + a.pct + "</span>") + "</div>";
    });
    h += "</div>";
    if (good.length) {
      h += '<h3 style="margin-top:36px">What you can already show</h3><ul class="ok-list">';
      good.forEach(function (it) { h += '<li><span class="iid">' + it.id + "</span>" + esc(it.check) + "</li>"; });
      h += "</ul>";
    }
    h += "</div><div><h3>Gaps to close" + (gaps.length ? ", most serious first" : "") + "</h3>";
    if (!gaps.length) h += '<p class="empty">No gaps in what you answered. Make sure you can hand over the evidence for each "yes".</p>';
    else {
      h += '<ol class="gaps">';
      gaps.forEach(function (it) {
        h += '<li class="gap"><div class="gap-top"><span class="iid">' + it.id + "</span><b>" + esc(it.check) + "</b>" +
          '<span class="pill ' + (answers[it.id] === "missing" ? "stop" : "gold") + '">' + label[answers[it.id]] + "</span>" +
          (it.hard ? '<span class="pill stop">hard to evidence</span>' : "") + "</div>" +
          "<p>" + esc(it.gap) + "</p>" +
          '<p class="good"><b>What good looks like:</b> ' + esc(it.strong) + "</p>" +
          '<p><a href="' + kitLink(it.id) + '">Answer guide and template for ' + it.id + "</a></p></li>";
      });
      h += "</ol>";
    }
    h += '</div></div><div class="actions">' +
      '<button type="button" class="btn primary" id="share">Copy share link</button>' +
      '<button type="button" class="btn" id="pdf">Save as PDF</button>' +
      '<button type="button" class="btn" id="dljson">Download answers (JSON)</button>' +
      '<button type="button" class="btn" id="dlcsv">Download answers (CSV)</button>' +
      '<span class="hint" id="share-msg" role="status"></span></div>';
    body.innerHTML = h;
    document.getElementById("name").addEventListener("input", function (e) { name = e.target.value; writeHash(); });
    document.getElementById("share").addEventListener("click", share);
    document.getElementById("pdf").addEventListener("click", function () { window.print(); });
    document.getElementById("dljson").addEventListener("click", function () { download("agent-readiness-answers.json", "application/json", toJSON()); });
    document.getElementById("dlcsv").addEventListener("click", function () { download("agent-readiness-answers.csv", "text/csv", toCSV()); });
  }

  function update() {
    var n = core.filter(function (it) { return answers[it.id]; }).length;
    var total = Object.keys(answers).length;
    document.getElementById("prog-text").textContent = n + " of " + core.length + " core answered" +
      (total > n ? " (+" + (total - n) + " more)" : "");
    document.getElementById("prog-bar").style.width = (100 * n / core.length) + "%";
    writeHash(); renderReport();
  }

  function encode() {
    return Object.keys(answers).map(function (id) { return id + CODE[answers[id]]; }).join(".");
  }
  function writeHash() {
    var parts = [];
    if (Object.keys(answers).length) parts.push("r=" + encode());
    if (name) parts.push("n=" + encodeURIComponent(name));
    var h = parts.length ? "#" + parts.join("&") : "";
    try { history.replaceState(null, "", location.pathname + location.search + h); } catch (e) { /* file:// in some browsers */ }
  }
  function readHash() {
    var h = location.hash.replace(/^#/, ""), got = false;
    h.split("&").forEach(function (kv) {
      var i = kv.indexOf("="); if (i < 0) return;
      var k = kv.slice(0, i), v = kv.slice(i + 1);
      if (k === "r") v.split(".").forEach(function (t) {
        var m = /^([A-Z]{3}-\d{2})([epomn])$/.exec(t);
        if (m && byId[m[1]]) { answers[m[1]] = DECODE[m[2]]; got = true; }
      });
      if (k === "n") { try { name = decodeURIComponent(v).slice(0, 80); } catch (e) { name = ""; } }
    });
    return got;
  }
  function share() {
    writeHash();
    var url = location.href.split("#")[0] + "#r=" + encode() + (name ? "&n=" + encodeURIComponent(name) : "");
    var msg = document.getElementById("share-msg");
    var done = function () { msg.textContent = "Link copied. The answers live in the link itself; nothing is stored anywhere."; };
    if (navigator.clipboard && window.isSecureContext !== false) navigator.clipboard.writeText(url).then(done, function () { prompt("Copy this link", url); });
    else prompt("Copy this link", url);
  }

  function toJSON() {
    var doc = { kit: "agent-security-review", kit_version: D.version, vendor: name, product: "", completed_by: "",
      date: new Date().toISOString().slice(0, 10), answers: [] };
    D.items.forEach(function (it) {
      var x = extra[it.id] || {};
      doc.answers.push({ id: it.id, status: answers[it.id] || "", answer: x.answer || "", evidence_links: x.links || [] });
    });
    return JSON.stringify(doc, null, 2) + "\n";
  }
  function csvCell(s) { s = String(s == null ? "" : s); return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
  function toCSV() {
    var rows = [["id", "status", "answer", "evidence_link"]];
    D.items.forEach(function (it) { var x = extra[it.id] || {};
      rows.push([it.id, answers[it.id] || "", x.answer || "", (x.links || []).join(" ")]); });
    return rows.map(function (r) { return r.map(csvCell).join(","); }).join("\n") + "\n";
  }
  function download(fname, type, text) {
    var a = el("a", { href: URL.createObjectURL(new Blob([text], { type: type })), download: fname });
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  function parseCSV(text) {
    var rows = [], row = [], cell = "", q = false;
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (q) { if (ch === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += ch; }
      else if (ch === '"') q = true;
      else if (ch === ",") { row.push(cell); cell = ""; }
      else if (ch === "\n" || ch === "\r") { if (ch === "\r" && text[i + 1] === "\n") i++; row.push(cell); rows.push(row); row = []; cell = ""; }
      else cell += ch;
    }
    if (cell || row.length) { row.push(cell); rows.push(row); }
    var head = (rows.shift() || []).map(function (h) { return h.trim().toLowerCase(); });
    return rows.filter(function (r) { return r.some(function (c) { return c.trim(); }); }).map(function (r) {
      var o = {}; head.forEach(function (h, j) { o[h] = r[j] || ""; }); return o; });
  }
  function importText(text, fname) {
    var list = [];
    var t = text.replace(/^﻿/, "");
    if (/\.json$/i.test(fname) || /^\s*[\[{]/.test(t)) {
      var doc = JSON.parse(t);
      list = (doc.answers || doc).map(function (a) { return { id: a.id, status: a.status, answer: a.answer,
        links: a.evidence_links || (a.evidence_link ? [a.evidence_link] : []) }; });
      if (doc.vendor && !name) name = String(doc.vendor).slice(0, 80);
    } else {
      list = parseCSV(t).map(function (r) { return { id: (r.id || "").trim(), status: r.status, answer: r.answer || r.your_answer,
        links: (r.evidence_link || "").split(/\s+/).filter(Boolean) }; });
    }
    var n = 0, skipped = 0;
    list.forEach(function (a) {
      var id = String(a.id || "").trim().toUpperCase();
      if (!byId[id]) return;
      var st = SYN[String(a.status || "").trim().toLowerCase()];
      extra[id] = { answer: a.answer || "", links: a.links || [] };
      if (st) { answers[id] = st; n++; } else if (String(a.status || "").trim()) skipped++;
    });
    if (list.some(function (a) { return byId[String(a.id || "").trim().toUpperCase()] && !byId[String(a.id).trim().toUpperCase()].core && SYN[String(a.status || "").trim().toLowerCase()]; })) showAll = true;
    return { n: n, skipped: skipped };
  }

  document.getElementById("file").addEventListener("change", function (e) {
    var f = e.target.files[0], msg = document.getElementById("msg");
    if (!f) return;
    var rd = new FileReader();
    rd.onload = function () {
      try {
        var r = importText(String(rd.result), f.name);
        if (!r.n) { msg.className = "err"; msg.textContent = "No statuses found. Fill the status column with evidenced, partial, policy_only, missing or not_applicable."; }
        else { msg.className = "ok"; msg.textContent = "Imported " + r.n + " answers" + (r.skipped ? ", skipped " + r.skipped + " with an unknown status" : "") + "."; }
        renderForm(); update();
        if (r.n) document.getElementById("report").scrollIntoView();
      } catch (err) { msg.className = "err"; msg.textContent = "Could not read that file. Use the JSON or CSV answer sheet from the Kit."; }
      e.target.value = "";
    };
    rd.readAsText(f);
  });
  document.getElementById("reset").addEventListener("click", function () {
    answers = {}; extra = {}; name = ""; showAll = false; document.getElementById("msg").textContent = ""; renderForm(); update();
  });
  document.getElementById("more").addEventListener("click", function () { showAll = !showAll; renderForm(); });

  if ("IntersectionObserver" in window) {
    var dock = document.getElementById("dock");
    new IntersectionObserver(function (es) { es.forEach(function (x) { dock.classList.toggle("hidden", x.isIntersecting); }); })
      .observe(document.getElementById("report"));
  }
  var fromLink = readHash();
  if (fromLink && D.items.some(function (it) { return !it.core && answers[it.id]; })) showAll = true;
  renderForm(); update();
  if (fromLink) document.getElementById("report").scrollIntoView();
})();
</script>
</body>
</html>
"""
