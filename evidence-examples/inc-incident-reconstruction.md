# INC · Incident reconstruction — sample answer

Covers [INC-01](../checklist.md#inc-01), [INC-02](../checklist.md#inc-02), [INC-03](../checklist.md#inc-03).

## Sample answer

> For any time window, dispute or customer, we can export every agent action across all your systems in order, with identity, scope, inputs and your systems' responses. Because records are hash-chained, the export also shows there are no gaps. In our last tabletop (August 2026, scenario: unexpected credits on 30 disputes) we produced the full ordered export in 11 minutes.
>
> We notify you of AI-related incidents (model failure, data leakage, harmful output, out-of-policy actions) within 24 hours of detection, so you can meet your 72-hour regulatory clock. Triggers include mismatch spikes, policy-gateway rejections above threshold and customer complaints tagged to the agent.
>
> Your operations team has a kill switch in the admin console that stops all write actions within 30 seconds (last tested 2026-09-30: 12 seconds). Model and prompt versions are pinned; rollback to the previous release takes under 10 minutes.

## Example reconstruction export (excerpt)

```text
window: 2026-08-20T14:00Z–15:00Z  systems: card-servicing  chain: complete (records 18,201–18,262)
#18,214 14:03:11Z svc-acme-agent-prod  issue_provisional_credit D-80114 $250.00  resp 201 CR-50771  check=match
#18,215 14:03:14Z svc-acme-agent-prod  issue_provisional_credit D-80115 $250.00  resp 201 CR-50772  check=match
#18,216 14:03:15Z policy-gateway       issue_provisional_credit D-80116 $900.00  REJECTED rule=credit.max_amount_usd
…
```
