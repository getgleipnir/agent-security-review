# SUB · Sub-processors — sample answer

Covers [SUB-01](../checklist.md#sub-01), [SUB-02](../checklist.md#sub-02), [SUB-03](../checklist.md#sub-03).

## Sample answer

> Sub-processors involved in the agent: provider A (primary reasoning model, EU region, zero retention, no training), provider B (fallback model, EU region, zero retention, no training), cloud host (EU region), and a speech-to-text provider for the voice channel (not enabled for you). The list with regions and terms is in our trust center, and we notify you 30 days before any change. The monthly report compares the services actually called for your traffic with this list.
>
> Our contract gives you and your regulators audit rights over the agent service, including its records. Beyond our SOC 2 Type II report (infrastructure and access), we provide a quarterly evidence pack covering agent behaviour: actions by type and system, policy rejections, reviews, failures and mismatches, model and prompt changes, with the underlying signed records so your auditors can check them independently.
>
> We will cooperate with any regulatory inquiry about your use of the agent and give examiners the documentation and records they request, through you or directly as you prefer.

## Example evidence pack contents

```text
evidence-pack-2026-Q3/
  summary.pdf              actions, systems touched, access used, failures, mismatches, reviews
  model-and-prompt-changes.md
  subprocessors-observed.csv   declared vs actually called, per month
  records/                 signed action records for the quarter
  verify.md                how to verify the records offline
```
