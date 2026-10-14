# CHG · Model & prompt changes — sample answer

Covers [CHG-01](../checklist.md#chg-01) to [CHG-04](../checklist.md#chg-04).

## Sample answer

> The agent uses one primary model (provider A, pinned version) and one fallback (provider B, pinned version) for reasoning, plus an embedding model for retrieval. The list per feature is in our trust center. We give 30 days' notice before changing a model or provider, and you can delay a change for your use case.
>
> Prompts, tool definitions and policies are code: versioned in Git, reviewed by two engineers, and released only after the evaluation suite passes (1,200 dispute scenarios, including injection and policy-limit cases). The prompt, config and policy versions are stored on every action record, so any action can be tied to the exact release.
>
> Validation runs before each release and monthly in production on a sample of 500 resolved disputes, compared against your team's outcomes. We track accuracy, credit-amount error, escalation rate and complaint rate, and send you a monthly report. A drift of more than 2 points on accuracy triggers re-validation.

## Example change log entry

```yaml
release: 3.2.4
date: 2026-09-22
changes:
  - prompt: pr-30 -> pr-31   # clarify partial-refund handling
  - policy: p-13 -> p-14     # add check: dispute must be open
model: unchanged (provider-a model-x 2026-08-01)
evaluation: 1,200 scenarios, 98.6% pass (prev 98.1%), 0 policy violations
approved_by: [eng-lead-1, risk-review-2]
customer_notice: not required (no model change)
```
