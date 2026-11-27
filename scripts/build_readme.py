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
WALLS = "Wall Systems"
BASE = ["Category", "Product", "Function", "Vendor", "Source", "Verification"]
# Every CSV column after BASE is a Wall Systems checkbox (Y or blank).
# Add a checkbox by adding a column to products.csv; no code change needed.
FLAGS = []


def load():
    with open(ROOT / "products.csv", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if reader.fieldnames[:len(BASE)] != BASE:
        sys.exit(f"products.csv must start with columns {BASE}")
    FLAGS[:] = reader.fieldnames[len(BASE):]
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
        for flag in FLAGS:
            if r[flag] not in ("", "Y"):
                errors.append(f"line {i}: {r['Product']!r} {flag} must be Y or blank")
            if r[flag] and r["Category"] != WALLS:
                errors.append(f"line {i}: {flag} is only for {WALLS}")
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
        walls = cat == WALLS
        out += [f"## {cat}", ""]
        if walls:
            out += ["✓ means the maker sells its own version. Blank means not confirmed, so check the maker's site.", ""]
            out += ["| Product | Function | " + " | ".join(FLAGS) + " | Vendor | Source |",
                    "|---|---|" + "---|" * len(FLAGS) + "---|---|"]
        else:
            out += ["| Product | Function | Vendor | Source |", "|---|---|---|---|"]
        for r in sorted(by_cat[cat], key=lambda r: r["Product"].lower().strip('"')):
            vendor = f"[Link]({r['Vendor']})" if r["Vendor"] else "—"
            ticks = "".join(f" {'✓' if r[f] else ''} |" for f in FLAGS) if walls else ""
            out.append(f"| {cell(r['Product'])} | {cell(r['Function'])} |{ticks} {vendor} | [Reference]({r['Source']}) |")
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
