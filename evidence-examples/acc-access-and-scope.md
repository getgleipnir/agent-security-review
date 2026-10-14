# ACC · Access & scope — sample answer

Covers [ACC-01](../checklist.md#acc-01), [ACC-02](../checklist.md#acc-02), [ACC-03](../checklist.md#acc-03).

## Sample answer

> The agent can call three tools in your environment: `get_transaction` (read), `get_dispute` (read) and `issue_provisional_credit` (write, max $250 per dispute). The list and limits live in a versioned policy file (`agent-policy.yaml`, current version `p-14`), and are enforced in our tool gateway before any request leaves our service. The model cannot call an endpoint that is not on the list, and the gateway rejects a credit above $250 regardless of what the model asks for. Our last quarterly test sent 200 out-of-scope and over-limit calls; all were rejected and logged.
>
> The agent uses its own service identity in your card-servicing system (`svc-acme-agent-prod`), separate from any staff account, with an OAuth client scoped to the three endpoints. Credentials are held by the gateway and never enter the model context. Every action record carries the agent ID, version, credential ID and the dispute it belongs to.
>
> Retrieved content (customer messages, transaction memos) is passed to the model as data, never as instructions. Tool arguments are validated against a schema and the dispute in scope; an injected instruction to credit a different account fails validation. Our latest red-team report (indirect injection via chat and memo fields) is available under NDA.

## Example record (scope fields)

```json
{
  "action_id": "act_01HZX…7Q",
  "agent": { "id": "acme-support-agent", "version": "3.2.4" },
  "identity": { "principal": "svc-acme-agent-prod", "credential_id": "oauth-client-…4f2", "on_behalf_of": "dispute:D-88213" },
  "tool": "issue_provisional_credit",
  "policy": { "version": "p-14", "rule": "credit.max_amount_usd<=250", "decision": "allowed" },
  "arguments": { "dispute_id": "D-88213", "amount_usd": 42.10, "account_ref": "[REDACTED:acct]" }
}
```
