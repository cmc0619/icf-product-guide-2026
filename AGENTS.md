# Repository working conventions

- This is a shared construction research brainspace.
- Commit small, coherent changes frequently with descriptive messages.
- Routine research edits may be committed directly to main without asking for commit, push or merge approval.
- Attribute each product to its relevant sources; treat all discovery sources equally.
- Distinguish verified facts from research leads and hypotheses.
- Do not publish private information or secrets.
- Remove confirmed defunct vendors and discontinued products; do not maintain a vendor-status archive. Verify commercial relevance before adding products; Git history preserves prior entries.
- Prefer durable functional descriptions over time-relative wording, ownership history, prices or marketing claims. Retain useful brand/parent relationships such as Nudura (Tremco).
- Exclude wood-cement ICF; retain interesting adjacent products. Keep HVAC guidance brief and tied to construction interfaces.
- Preserve dated primary research and its test limitations.
- Edit products.csv only. Never edit the product tables in README.md: a GitHub Action rebuilds them from the CSV on every push to main (`scripts/build_readme.py`). The Action fails on duplicate products, missing sources, non-URL vendors and misplaced option flags, so check its run after pushing. Fill Vendor with the maker's URL and give each row a specific Verification note naming who listed it.
- Accessories that only work with one maker's forms (its own bucks, brick ledges, R-value inserts) aren't listed as products. Mark them Y in that maker's Wall Systems row instead. Third-party accessories that work across brands keep their own rows.
