"""Regenerate the product tables in README.md from products.csv.

Run from the repository root:  python scripts/build_readme.py
Text above the first category heading and from "## Technical research"
onward is kept as written; everything between is rebuilt from the CSV.
The CSV is checked for duplicate products and missing sources first.
"""
import csv
import pathlib
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
TAIL = "## Technical research"


def load():
    with open(ROOT / "products.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    errors = []
    seen = set()
    for i, r in enumerate(rows, start=2):
        key = r["Product"].strip().lower()
        if key in seen:
            errors.append(f"line {i}: duplicate product {r['Product']!r}")
        seen.add(key)
        if not r["Source"].startswith("http"):
            errors.append(f"line {i}: {r['Product']!r} has no source URL")
        if r["Vendor"] and not r["Vendor"].startswith("http"):
            errors.append(f"line {i}: {r['Product']!r} vendor is not a URL")
    if errors:
        sys.exit("\n".join(errors))
    return rows


def cell(text):
    return text.replace("|", "\\|")


def tables(rows):
    by_cat = defaultdict(list)
    for r in rows:
        by_cat[r["Category"]].append(r)
    out = []
    for cat in sorted(by_cat, key=str.lower):
        out += [f"## {cat}", "", "| Product | Function | Vendor | Source |", "|---|---|---|---|"]
        for r in sorted(by_cat[cat], key=lambda r: r["Product"].lower().strip('"')):
            vendor = f"[Link]({r['Vendor']})" if r["Vendor"] else "—"
            out.append(f"| {cell(r['Product'])} | {cell(r['Function'])} | {vendor} | [Reference]({r['Source']}) |")
        out.append("")
    return out


def main():
    rows = load()
    readme = (ROOT / "README.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    lines = readme.split("\n")
    first = next(i for i, l in enumerate(lines) if l.startswith("## "))
    tail = next(i for i, l in enumerate(lines) if l.startswith(TAIL))
    new = lines[:first] + tables(rows) + lines[tail:]
    (ROOT / "README.md").write_text("\n".join(new), encoding="utf-8", newline="\n")
    print(f"README.md rebuilt: {len(rows)} products")


if __name__ == "__main__":
    main()
