# HUM · Human oversight (as the buyer defines it) — sample answer

Covers [HUM-01](../checklist.md#hum-01), [HUM-02](../checklist.md#hum-02).

## Sample answer

> You set the oversight rules for this use case in a policy file you can read and change. Your current rules: credits up to $250 run without review; credits above $250, any dispute from a customer flagged as vulnerable, and any second credit on the same card within 30 days go to your dispute team before execution. Every action record states which rule applied and, where review was required, who reviewed it, the decision, and the time of review relative to execution.
>
> A weekly exceptions report lists any action where a review rule applied but no review is recorded. Since go-live the count is zero.
>
> When your team overrides or reverses an agent action, the override is recorded against the original action ID with the reviewer, time, change and reason. Override rates by reason are in the monthly report.

## Example record (oversight fields)

```json
{
  "action_id": "act_01J02…K8",
  "oversight": {
    "policy_version": "buyer-oversight-v6",
    "rule": "credit.amount_usd>250 -> review_before_execution",
    "review": { "reviewer": "bank-staff:…419", "decision": "approved", "decided_at": "2026-10-03T13:22:10Z" },
    "executed_at": "2026-10-03T13:22:12Z"
  }
}
```

```json
{
  "override_id": "ovr_01J03…P1",
  "original_action_id": "act_01HZY…2M",
  "by": "bank-staff:…207",
  "at": "2026-09-14T11:20:05Z",
  "change": { "credit_amount_usd": [17.99, 18.00] },
  "reason": "rounding_mismatch"
}
```
