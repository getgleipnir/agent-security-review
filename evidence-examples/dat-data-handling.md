# DAT · Data handling — sample answer

Covers [DAT-01](../checklist.md#dat-01), [DAT-02](../checklist.md#dat-02).

## Sample answer

> Your data is not used to train or fine-tune any model, by us or by our model providers; both providers are contracted with zero data retention. Conversation content is kept for 90 days for support, then deleted; action records follow the retention you set (see RET). On request we delete a customer's data and send a deletion confirmation within 30 days.
>
> Action records do not store full request and response bodies. Account numbers, card numbers and names are redacted or replaced with a keyed hash before a record is written, so records can still be matched to your systems without containing the raw value. The list of fields and their treatment is documented and versioned.

## Example redaction map

```yaml
redaction_version: r-5
fields:
  arguments.account_ref: hmac-sha256   # matchable, not reversible
  arguments.card_number: drop
  sources[].customer_name: drop
  system_response.account_holder: drop
  agent_claim: keep                     # contains amounts and IDs only
```
