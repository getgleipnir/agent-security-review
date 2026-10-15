# Contributing

Thanks for helping. The checklist is only as good as the questions real reviewers ask.

## Most useful contributions

1. **A question you were asked in a real review.** Open an issue with the "Add a question I was asked" template. Paraphrase it; never paste a buyer's confidential questionnaire, and don't name the buyer unless the questionnaire is public.
2. **A wrong or weak mapping.** Open an issue with the "Fix a mapping" template and link the exact section of the source.
3. **Better evidence examples.** Pull requests to `evidence-examples/` are welcome. Keep them fictional and redacted.

## Editing the checklist

`checklist.yaml` is the source of truth. `checklist.md`, `checklist.csv`, `answers-template.*`, `mappings/*.md` and `site/` are generated.

```bash
pip install pyyaml jsonschema
# edit checklist.yaml
python scripts/build.py          # validates, then regenerates md, csv, templates, mappings and site
python scripts/build.py --check  # what CI runs
python scripts/build_pdf.py      # optional: refresh the PDF (needs Playwright + Chromium)
```

Rules:

- **IDs are stable.** Never renumber or reuse an ID. To retire an item, set `deprecated: true` and leave it in place. New IDs go at the end of their group and must be added to `schema/ids.lock`.
- **Every reference needs a source you checked.** Set `confidence` honestly:
  - `verified`: you read the primary text.
  - `secondary`: the primary is gated, and you checked a reliable secondary source.
  - `title-only`: only the control title is public.
- **Paraphrase, don't copy.** Notes are short summaries in your own words, max 160 characters. Many frameworks are copyrighted.
- **Stay vendor-neutral.** Evidence descriptions must be achievable with any tooling. Don't name products in items.
- **Questions are phrased the way buyers ask them**, not the way vendors would like to be asked.
- **Template answers must not overclaim.** Put every fact the vendor has to supply in `[square brackets]`, so nobody can submit the template unchanged by accident.

## Pull requests

- One logical change per PR.
- Run `python scripts/build.py` and commit the generated files.
- CI must pass.

By contributing, you agree that your contribution is licensed under CC BY 4.0 (content) or MIT (scripts and schema), matching the files you change.
