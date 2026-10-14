#!/usr/bin/env python3
"""Validate checklist.yaml against the JSON schema and the repo's ID rules.

Usage: python scripts/validate.py
Exit code 0 on success, 1 on any error.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
CHECKLIST = ROOT / "checklist.yaml"
SCHEMA = ROOT / "schema" / "checklist.schema.json"
IDS_LOCK = ROOT / "schema" / "ids.lock"


class _DateSafeLoader(yaml.SafeLoader):
    """SafeLoader that keeps dates as strings so they match the JSON schema."""


_DateSafeLoader.add_constructor(
    "tag:yaml.org,2002:timestamp",
    lambda loader, node: loader.construct_scalar(node),
)


def load_checklist(path: Path = CHECKLIST) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.load(fh, Loader=_DateSafeLoader)


def check(data: dict) -> list[str]:
    import json

    errors: list[str] = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "(root)"
        errors.append(f"schema: {loc}: {err.message}")
    if errors:
        return errors

    group_ids = [g["id"] for g in data["groups"]]
    if len(group_ids) != len(set(group_ids)):
        errors.append("groups: duplicate group id")
    frameworks = set(data["frameworks"])

    seen: set[str] = set()
    used_frameworks: set[str] = set()
    for item in data["items"]:
        iid = item["id"]
        if iid in seen:
            errors.append(f"{iid}: duplicate item id")
        seen.add(iid)
        if item["group"] not in group_ids:
            errors.append(f"{iid}: unknown group {item['group']}")
        if not iid.startswith(item["group"] + "-"):
            errors.append(f"{iid}: id prefix does not match group {item['group']}")
        for ref in item["references"]:
            if ref["fw"] not in frameworks:
                errors.append(f"{iid}: unknown framework key '{ref['fw']}'")
            used_frameworks.add(ref["fw"])

    for g in group_ids:
        if not any(i["group"] == g for i in data["items"]):
            errors.append(f"group {g}: has no items")
    for fw in sorted(frameworks - used_frameworks):
        errors.append(f"framework {fw}: declared but never referenced")

    # Stable IDs: every ID ever issued must still exist (deprecate, never delete).
    if IDS_LOCK.exists():
        locked = {
            line.strip()
            for line in IDS_LOCK.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        }
        for missing in sorted(locked - seen):
            errors.append(f"{missing}: listed in schema/ids.lock but removed; mark it deprecated instead")
        for new in sorted(seen - locked):
            errors.append(f"{new}: new id not in schema/ids.lock; add it there")
    else:
        errors.append("schema/ids.lock is missing")

    return errors


def main() -> int:
    errors = check(load_checklist())
    if errors:
        for e in errors:
            print(f"ERROR {e}", file=sys.stderr)
        print(f"{len(errors)} error(s)", file=sys.stderr)
        return 1
    print("checklist.yaml is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
