# Agent Security Review Kit

The questions banks, insurers and enterprise security teams ask an AI agent vendor before the agent goes into production. For each question you get:

- **why buyers ask it**: the risk or obligation behind it;
- **what a strong answer looks like**: the bar the reviewer is holding you to;
- **what evidence to attach**, and which answers usually trigger a follow-up;
- **a template answer** you adapt, with every fact you must supply marked as a `[blank]`;
- **framework references** (NIST AI RMF, ISO/IEC 42001, EU AI Act, SOC 2, DORA, NYDFS, AIUC-1 and others), each marked with how it was checked.

Free, vendor-neutral, no signup. Content under CC BY 4.0.

## Try it in two minutes

1. Open the kit page. Until it is hosted, download this repo and open `site/index.html` in a browser; it works offline and makes no network requests.
2. Search for a topic you know you'll be asked about, such as `kill switch`, `retention` or `SOC 2`, and open the question.
3. Download the fill-in sheet ([CSV](answers-template.csv) or [JSON](answers-template.json)), and answer the questions marked **Hard to evidence today** first.

| File | What it is |
|---|---|
| [`site/index.html`](site/index.html) | The kit as a searchable page |
| [`site/downloads/agent-security-review-kit.pdf`](site/downloads/agent-security-review-kit.pdf) | The same, as a PDF to print or attach |
| [`checklist.md`](checklist.md) | The same, as Markdown |
| [`answers-template.csv`](answers-template.csv) | Fill-in sheet: `status`, `answer`, `evidence_link` per question |
| [`answers-template.json`](answers-template.json) | Fill-in file for tools, with `evidence_links` as a list ([schema](schema/answers.schema.json)) |
| [`checklist.csv`](checklist.csv) | Every field in one table, for questionnaires and trackers |
| [`checklist.yaml`](checklist.yaml) | Source of truth with stable IDs |
| [`mappings/`](mappings/) | One table per framework, plus a coverage matrix |
| [`evidence-examples/`](evidence-examples/) | A sample answer and redacted record per area |

`status` takes one of: `evidenced` (you can show it today), `partial`, `policy_only` (a statement, no proof), `missing`, `not_applicable`.

## What's covered

33 questions in 10 areas:

| Area | Covers |
|---|---|
| Access & scope | What the agent can do, under which identity, how limits are enforced, prompt injection |
| Action records | The full record of one action, model version, endpoints called, sources, decision reasons |
| Outcome verification | Whether what the agent reports matches what happened in the system of record |
| Tamper evidence | Whether records can be changed unnoticed, and whether the buyer can check them independently |
| Incident reconstruction | Detecting, reporting, stopping (kill switch) and reconstructing an incident |
| Retention | How long records are kept, by whom, and the buyer's own copy |
| Model & prompt changes | Which models run, change control, validation and drift |
| Data handling | Training use, retention and deletion, personal data inside records |
| Human oversight | Evidence that the oversight the buyer chose was actually followed |
| Sub-processors | Model, voice and tool providers, audit rights, regulator access |

## The seven questions where reviews stall

Most questionnaire items (which model, do you train on our data, SOC 2, pen test) are answered with policy text. Reviews stall where the buyer wants proof of **what the agent actually did**, and the vendor only has its own logs:

1. **One action, end to end** ([ACT-01](checklist.md#act-01)): the trigger, inputs, tool call, arguments, the system's response and the effect, produced in minutes.
2. **Which identity did it** ([ACC-02](checklist.md#acc-02)): every write traceable to an agent, version, credential and scope.
3. **Did it really happen** ([OUT-01](checklist.md#out-01)): the agent's claim next to the system of record's actual response.
4. **Can records be changed after the fact** ([TMP-01](checklist.md#tmp-01)): a mechanism such as hash chains and signatures, not the word "immutable".
5. **Can the buyer check without trusting you** ([TMP-02](checklist.md#tmp-02)): verification the buyer, auditor or regulator runs themselves.
6. **Reconstruct an incident** ([INC-01](checklist.md#inc-01)): an ordered, gap-free account across the buyer's systems.
7. **Buyer-held logs for the required period** ([RET-02](checklist.md#ret-02)): a copy the buyer controls.

## Using it in a live review

**Before.** Fill in the answer sheet with what your system does today. For each question marked hard to evidence, decide: evidence now, a dated roadmap item, or a compensating control. Prepare one fully worked, redacted case; reviewers almost always ask for one.

**During.** Answer with the evidence first, then the policy. If the buyer cites a framework, use [mappings/](mappings/) to show what you cover for it.

**After.** Turn follow-ups into items in your own copy and track them by ID. If you were asked something that isn't here, [add it](https://github.com/getgleipnir/agent-security-review/issues/new?template=add-question.yml).

Template answers are starting points. Replace every `[blank]` with what your system actually does and delete anything that isn't true; a template submitted unchanged will read as exactly that.

## How the references were checked

Each reference was checked against its source (most on 2026-10-14; AIUC-1, CSA AARM and SOC 2 on 2026-10-15) and marked:

- **verified**: checked against the primary text;
- **secondary source**: the primary is gated or unreadable (for example ISO/IEC 42001 and CSA AICM), so it was checked against a reliable secondary source;
- **title only**: only the control title was publicly available.

Paraphrases are ours and short. Read the source before relying on one. Worth knowing:

- **Tamper evidence and independent verification.** Three frameworks explicitly ask for audit records that are tamper-evident *and* independently verifiable: the FINOS AI Governance Framework (AIR-DET-021), AIUC-1 (E015.4, a supplemental control under the mandatory logging requirement E015) and the CSA AARM specification (R5, signed receipts per action, verifiable offline). DORA's RTS (2024/1774, Art. 12) requires logs to be protected against tampering and deletion. NYDFS Part 500, NAIC, the EU AI Act and ISO/IEC 42001 require records to exist, be retained and support reconstruction, without naming a mechanism. SOC 2 criteria cover logging, monitoring and processing integrity, also without naming a tamper-evidence mechanism.
- **EU AI Act.** Art. 12 requires automatic event logging for high-risk systems, and Art. 19 and 26(6) set log retention of at least six months. High-risk obligations for Annex III use cases, including credit scoring and life and health insurance pricing, apply from **2 December 2027** after the Digital Omnibus on AI (Regulation (EU) 2026/1744).
- **SOC 2** is an auditor's attestation report against the AICPA Trust Services Criteria, not a certification. It covers the vendor's controls, not individual agent actions, which is why a SOC 2 report alone rarely closes the agent-specific questions. The criteria text was checked against the AICPA's 2020 edition; the 2022 revision changed the points of focus, not the criteria.
- **Gated sources.** The FS-ISAC question workbook, SIG question text and AI-CAIQ question text are licensed or login-gated, so this kit maps to their published categories and control IDs, not their exact wording.

This kit is not legal advice and does not certify compliance with any framework.

## Building

```bash
pip install pyyaml jsonschema
python scripts/build.py          # validate, then regenerate everything from checklist.yaml
python scripts/build.py --check  # what CI runs
python scripts/build_pdf.py      # refresh the PDF (needs Playwright + Chromium)
```

## Contributing

Questions you were actually asked in a review are the most valuable contribution. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Content (questions, answers, mappings, examples, the page) is licensed under [CC BY 4.0](LICENSE). Scripts and JSON schemas are under the [MIT License](LICENSE-CODE). Public Sans is under the [SIL Open Font License](site/fonts/OFL.txt).

---

Maintained by [Gleipnir](https://getgleipnir.com), which builds independently verifiable action records for AI agents.
