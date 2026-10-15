#!/usr/bin/env python3
"""Generate checklist.md, checklist.csv, mappings/*.md, the fill-in templates and site/ from checklist.yaml.

Usage:
  python scripts/build.py          # write generated files
  python scripts/build.py --check  # fail if generated files are out of date
"""
from __future__ import annotations

import csv
import io
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kitpage import render_site  # noqa: E402
from scannerpage import render_scanner  # noqa: E402
from validate import ROOT, check, load_checklist  # noqa: E402

GENERATED_NOTE = "<!-- Generated from checklist.yaml by scripts/build.py. Do not edit by hand. -->"
CONFIDENCE_LABEL = {
    "verified": "verified",
    "secondary": "secondary source",
    "title-only": "title only",
}
KIND_LABEL = {
    "binding": "Binding law or regulation",
    "supervisory": "Supervisory guidance",
    "industry": "Industry framework",
    "voluntary": "Voluntary government framework",
    "standard": "Certifiable standard",
    "attestation": "Attestation criteria (an auditor's report, not a certification)",
}


def ref_link(ref: dict, fw: dict) -> str:
    url = ref.get("url")
    return f"[{ref['ref']}]({url})" if url else ref["ref"]


def md_escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render_checklist_md(data: dict) -> str:
    fws = data["frameworks"]
    out: list[str] = [GENERATED_NOTE, ""]
    out.append("# AI Agent Security Review Checklist")
    out.append("")
    out.append(
        f"Version {data['version']}, updated {data['updated']}. "
        f"{len(data['items'])} items in {len(data['groups'])} groups."
    )
    out.append("")
    out.append("How to read each item:")
    out.append("")
    out.append("- **Question**: how buyers usually phrase it in a questionnaire or review call.")
    out.append("- **Why they ask**: the risk or obligation behind it.")
    out.append("- **What a strong answer looks like**: the bar reviewers are looking for.")
    out.append("- **Evidence that satisfies it**: what to attach.")
    out.append("- **Not enough on its own**: answers that usually trigger a follow-up.")
    out.append("- **Template answer**: a starting point; replace every [bracketed] part with what your system "
               "actually does, and delete what isn't true.")
    out.append("- **References**: framework controls that cover the topic, with how we checked them "
               "(*verified* = primary text; *secondary source* = primary is gated, checked via a reliable "
               "secondary source; *title only* = only the control title was available).")
    out.append("- Items marked **Hard to evidence today** are the ones most vendors answer with a policy "
               "statement rather than proof.")
    out.append("")
    out.append("## Contents")
    out.append("")
    for g in data["groups"]:
        n = sum(1 for i in data["items"] if i["group"] == g["id"])
        anchor = f"{g['id'].lower()}--{slug(g['title'])}"
        out.append(f"- [{g['id']} · {g['title']}](#{anchor}) ({n})")
    out.append("")

    for g in data["groups"]:
        out.append(f"## {g['id']} · {g['title']}")
        out.append("")
        out.append(g["summary"])
        out.append("")
        for item in (i for i in data["items"] if i["group"] == g["id"]):
            title = item["id"]
            if item.get("deprecated"):
                title += " (deprecated)"
            out.append(f"### {title}")
            out.append("")
            flag = " **Hard to evidence today.**" if item["often_unevidenced"] else ""
            out.append(f"> {item['question']}{flag}")
            out.append("")
            if item["origin"] == "derived":
                out.append(f"*Derived item, split out from {item['derived_from']}.*")
                out.append("")
            out.append(f"**Why they ask.** {item['why']}")
            out.append("")
            out.append(f"**What a strong answer looks like.** {item['strong_answer']}")
            out.append("")
            out.append("**Evidence that satisfies it**")
            out.append("")
            out.extend(f"- {e}" for e in item["evidence"])
            out.append("")
            if item["not_enough"]:
                out.append("**Not enough on its own**")
                out.append("")
                out.extend(f"- {e}" for e in item["not_enough"])
                out.append("")
            out.append("**Template answer**")
            out.append("")
            out.append(f"> {item['template_answer']}")
            out.append("")
            if item.get("note"):
                out.append(f"*Note: {item['note']}*")
                out.append("")
            out.append("**References**")
            out.append("")
            for ref in item["references"]:
                fw = fws[ref["fw"]]
                out.append(
                    f"- {fw['short']} {ref_link(ref, fw)}: {ref['note']} "
                    f"*({CONFIDENCE_LABEL[ref['confidence']]})*"
                )
            out.append("")
    out.append("---")
    out.append("")
    out.append("Framework details, versions and per-framework tables: [mappings/](mappings/).")
    out.append("")
    return "\n".join(out)


def slug(text: str) -> str:
    keep = []
    for ch in text.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in " -":
            keep.append("-")
    return "".join(keep).strip("-")


def render_csv(data: dict) -> str:
    fws = data["frameworks"]
    groups = {g["id"]: g["title"] for g in data["groups"]}
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow([
        "id", "group", "question", "why_they_ask", "strong_answer", "evidence_that_satisfies",
        "not_enough_on_its_own", "template_answer", "hard_to_evidence_today", "references",
        "your_answer", "evidence_link",
    ])
    for item in data["items"]:
        writer.writerow([
            item["id"],
            groups[item["group"]],
            item["question"],
            item["why"],
            item["strong_answer"],
            " | ".join(item["evidence"]),
            " | ".join(item["not_enough"]),
            item["template_answer"],
            "yes" if item["often_unevidenced"] else "no",
            "; ".join(f"{fws[r['fw']]['short']} {r['ref']}" for r in item["references"]),
            "",
            "",
        ])
    return buf.getvalue()


def render_framework_md(key: str, data: dict) -> str:
    fw = data["frameworks"][key]
    rows: dict[str, dict] = {}
    order: list[str] = []
    for item in data["items"]:
        for ref in item["references"]:
            if ref["fw"] != key:
                continue
            if ref["ref"] not in rows:
                rows[ref["ref"]] = {"ref": ref, "notes": [], "items": [], "conf": set()}
                order.append(ref["ref"])
            row = rows[ref["ref"]]
            if ref["note"] not in row["notes"]:
                row["notes"].append(ref["note"])
            row["items"].append(item["id"])
            row["conf"].add(ref["confidence"])

    out = [GENERATED_NOTE, "", f"# {fw['name']}", ""]
    out.append(f"- Source: <{fw['url']}>")
    out.append(f"- Version used: {fw['version']}")
    out.append(f"- Type: {KIND_LABEL[fw['kind']]}")
    out.append(f"- Access: {fw['access']}")
    out.append(f"- Checked: {data['updated']}")
    out.append("")
    out.append("| Control | What it covers | Checklist items | How we checked |")
    out.append("|---|---|---|---|")
    for name in sorted(order, key=natural_key):
        row = rows[name]
        conf = ", ".join(CONFIDENCE_LABEL[c] for c in sorted(row["conf"]))
        items = ", ".join(f"[{i}](../checklist.md#{i.lower()})" for i in sorted(set(row["items"])))
        out.append(
            f"| {md_escape_cell(ref_link(row['ref'], fw))} | {md_escape_cell('; '.join(row['notes']))} "
            f"| {items} | {conf} |"
        )
    out.append("")
    return "\n".join(out)


def natural_key(text: str):
    import re

    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", text)]


def render_mappings_index(data: dict) -> str:
    fws = data["frameworks"]
    keys = list(fws)
    hits: dict[str, set[str]] = defaultdict(set)
    for item in data["items"]:
        for ref in item["references"]:
            hits[item["id"]].add(ref["fw"])
    out = [GENERATED_NOTE, "", "# Framework mappings", ""]
    out.append("One file per framework. Each lists the controls we map, what they cover, and which "
               "checklist items they support. Paraphrases are ours; read the source before relying on one.")
    out.append("")
    out.append("| Framework | Type | File |")
    out.append("|---|---|---|")
    for k in keys:
        out.append(f"| {fws[k]['name']} | {KIND_LABEL[fws[k]['kind']]} | [{k}.md]({k}.md) |")
    out.append("")
    out.append("## Coverage matrix")
    out.append("")
    out.append("| Item | " + " | ".join(fws[k]["short"] for k in keys) + " |")
    out.append("|---|" + "---|" * len(keys))
    for item in data["items"]:
        cells = ["x" if k in hits[item["id"]] else "" for k in keys]
        out.append(f"| [{item['id']}](../checklist.md#{item['id'].lower()}) | " + " | ".join(cells) + " |")
    out.append("")
    return "\n".join(out)


def render_answers_json(data: dict) -> str:
    """Fill-in template a vendor completes; tools can read the completed file."""
    import json

    from kitpage import STATUS

    doc = {
        "$schema": "https://github.com/getgleipnir/agent-security-review/schema/answers.schema.json",
        "kit": "agent-security-review",
        "kit_version": data["version"],
        "vendor": "",
        "product": "",
        "completed_by": "",
        "date": "",
        "status_values": {k: v for k, v in STATUS},
        "answers": [
            {
                "id": i["id"],
                "question": i["question"],
                "status": "",
                "answer": "",
                "evidence_links": [],
                "template_answer": i["template_answer"],
            }
            for i in data["items"] if not i.get("deprecated")
        ],
    }
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def render_answers_csv(data: dict) -> str:
    groups = {g["id"]: g["title"] for g in data["groups"]}
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["id", "area", "question", "status", "answer", "evidence_link", "template_answer",
                     "hard_to_evidence_today"])
    for i in data["items"]:
        if i.get("deprecated"):
            continue
        writer.writerow([i["id"], groups[i["group"]], i["question"], "", "", "", i["template_answer"],
                         "yes" if i["often_unevidenced"] else "no"])
    return buf.getvalue()


def outputs(data: dict) -> dict[Path, str]:
    files = {
        ROOT / "checklist.md": render_checklist_md(data),
        ROOT / "checklist.csv": render_csv(data),
        ROOT / "mappings" / "README.md": render_mappings_index(data),
        ROOT / "answers-template.json": render_answers_json(data),
        ROOT / "answers-template.csv": render_answers_csv(data),
        ROOT / "site" / "index.html": render_site(data),
        ROOT / "site" / "scanner" / "index.html": render_scanner(data),
    }
    # The site serves its own copies so it works without GitHub.
    for name in ("checklist.md", "answers-template.json", "answers-template.csv"):
        files[ROOT / "site" / "downloads" / name] = files[ROOT / name]
    for key in data["frameworks"]:
        files[ROOT / "mappings" / f"{key}.md"] = render_framework_md(key, data)
    return files


def main() -> int:
    data = load_checklist()
    errors = check(data)
    if errors:
        for e in errors:
            print(f"ERROR {e}", file=sys.stderr)
        return 1
    files = outputs(data)
    if "--check" in sys.argv:
        stale = [p for p, text in files.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
        expected = {p.name for p in files if p.parent.name == "mappings"}
        extra = [p for p in (ROOT / "mappings").glob("*.md") if p.name not in expected]
        for p in stale:
            print(f"OUT OF DATE {p.relative_to(ROOT)}", file=sys.stderr)
        for p in extra:
            print(f"UNEXPECTED {p.relative_to(ROOT)}", file=sys.stderr)
        if stale or extra:
            print("Run: python scripts/build.py", file=sys.stderr)
            return 1
        print("generated files are up to date")
        return 0
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
