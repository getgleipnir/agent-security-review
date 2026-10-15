# AI Agent Security Review Checklist

A free, vendor-neutral checklist for AI agent vendors selling into banks, lenders and insurers. It lists the questions their security, risk and compliance teams ask about agents, why they ask them, what evidence actually satisfies them, and which frameworks each question comes from.

**Who it's for:** founders, security leads and solutions engineers at companies whose agents take actions in a regulated buyer's systems (issuing refunds, updating claims, dispositioning alerts, changing loan records). It is also useful for the buyer's side: TPRM, model risk and internal audit teams who need a structured way to review an agent.

- [checklist.md](checklist.md): 33 items in 10 groups, readable version
- [checklist.csv](checklist.csv): paste into a questionnaire or tracker (has empty `your_answer` and `evidence_link` columns)
- [checklist.yaml](checklist.yaml): source of truth with stable item IDs, for tools
- [mappings/](mappings/): one table per framework, plus a coverage matrix
- [evidence-examples/](evidence-examples/): a sample answer and redacted example record for each group

## The 60-second version

Most AI questionnaire items (which model, do you train on our data, SOC 2, pen test) are answered today with policy text. Reviews stall on a smaller set where buyers want proof about **what the agent actually did**, and vendors only have their own logs:

1. **One action, end to end** ([ACT-01](checklist.md#act-01)). Pick any action and produce the trigger, inputs, tool call, arguments, the system's response and the downstream effect, in minutes.
2. **Which identity did it** ([ACC-02](checklist.md#acc-02)). Every write traceable to a specific agent, version, credential and scope, not a shared service account.
3. **Did it really happen** ([OUT-01](checklist.md#out-01)). The agent's claim stored next to the system of record's actual response, with mismatches counted.
4. **Can records be changed after the fact** ([TMP-01](checklist.md#tmp-01)). Tamper evidence with a mechanism (hash chains, signatures), not the word "immutable".
5. **Can the buyer check without trusting you** ([TMP-02](checklist.md#tmp-02)). An offline verification the buyer, auditor or regulator runs themselves.
6. **Reconstruct an incident** ([INC-01](checklist.md#inc-01)). An ordered, gap-free account of what the agent did across the buyer's systems.
7. **Buyer-held logs for the required period** ([RET-02](checklist.md#ret-02)). A copy the buyer controls, for as long as its rules require.

If you have good answers to these seven, the rest of the review usually goes faster. Items marked **Hard to evidence today** in the checklist are this set and a few others.

## How to use it in a live review

**Before the review**
1. Copy `checklist.csv` into your tracker. Fill `your_answer` with what your system does today, and link evidence in `evidence_link`.
2. For every item marked **Hard to evidence today**, decide: real evidence now, a dated roadmap item, or a compensating control. Don't leave it to the call.
3. Prepare one fully worked case: a single redacted action with its complete record. Reviewers almost always ask for one.

**During the review**
- When a question comes in, find the matching item (the `id` column) and answer with the evidence, then the policy. Reviewers trust a record more than a paragraph.
- If the buyer cites a framework (FS-ISAC, NYDFS, NAIC, DORA, EU AI Act, AICM, AIUC-1, CSA AARM), use [mappings/](mappings/) to show which items you've covered for it.
- If you get a question that isn't here, note it and [add it](https://github.com/getgleipnir/agent-security-review/issues/new?template=add-question.yml).

**After the review**
- Turn follow-ups into items in your own copy of the YAML and track them by ID.

## How the mappings were built

Each item's references were checked on 2026-10-14 against the source (AIUC-1 and CSA AARM references on 2026-10-15) and marked:

- **verified**: checked against the primary text.
- **secondary source**: the primary is gated or unreadable (for example ISO 42001 and CSA AICM), so it was checked against a reliable secondary source.
- **title only**: only the control title was publicly available (common for CSA AICM's AI-specific controls).

Paraphrases are ours and short. Read the source before relying on one. Some points worth knowing:

- Three frameworks explicitly ask for audit records that are tamper-evident *and* independently verifiable: the **FINOS AI Governance Framework** (AIR-DET-021, verifiable by the deployer, auditor or regulator without privileged access to the provider), **AIUC-1** (E015.4, a supplemental "may include" control under the mandatory logging requirement E015) and the **CSA AARM** specification (R5: cryptographically signed receipts for every action, covering action, context, identity, decision and outcome, verifiable offline). DORA's RTS (2024/1774, Art. 12) requires logs to be protected against tampering and deletion; NYDFS Part 500, NAIC, the EU AI Act and ISO 42001 require records to exist, be retained and support reconstruction, without naming a mechanism.
- EU AI Act high-risk obligations for Annex III use cases, including credit scoring and life and health insurance pricing, apply from **2 December 2027** after the Digital Omnibus on AI (Regulation (EU) 2026/1744, published 24 July 2026, in force 27 July 2026).
- The FS-ISAC question workbook, SIG question text and the AI-CAIQ question text are licensed or login-gated, so this checklist maps to their published categories and control IDs, not to their exact question wording.

The checklist does not give legal advice and does not certify compliance with any framework.

## Contributing

Questions you were actually asked in a review are the most valuable contribution. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Content (checklist, mappings, examples) is licensed under [CC BY 4.0](LICENSE). Scripts and the JSON schema are under the [MIT License](LICENSE-CODE).

---

Maintained by [Gleipnir](https://getgleipnir.com), which builds independently verifiable action records for AI agents.
