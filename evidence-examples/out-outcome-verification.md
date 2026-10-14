# OUT · Outcome verification — sample answer

Covers [OUT-01](../checklist.md#out-01), [OUT-02](../checklist.md#out-02).

## Sample answer

> We do not treat the agent's own message as evidence. Each action record stores the agent's claim next to the raw response from your system. For write actions we also run a read-back: after `issue_provisional_credit`, we query `GET /credits/{id}` and compare amount, account and dispute ID with what the agent intended. The result (`match`, `mismatch` or `not_checked`) is stored on the record.
>
> In September there were 4,812 credit actions: 4,806 matched, 4 failed with an error the agent reported correctly, and 2 were mismatches (the API applied a currency rounding rule). Both mismatches were flagged within one minute and corrected by your operations team. The monthly report lists every failure and mismatch with its record ID.

## Example record (outcome fields)

```json
{
  "action_id": "act_01HZY…2M",
  "agent_claim": { "credit_amount_usd": 18.00, "dispute_id": "D-88577" },
  "system_response": { "status": 201, "credit_id": "CR-55168" },
  "outcome_check": {
    "method": "read_back",
    "query": "GET /credits/CR-55168",
    "observed": { "amount_usd": 17.99, "dispute_id": "D-88577" },
    "result": "mismatch",
    "fields": ["amount_usd"],
    "checked_at": "2026-09-14T11:02:44Z"
  }
}
```
