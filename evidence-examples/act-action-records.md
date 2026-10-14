# ACT · Action records — sample answer

Covers [ACT-01](../checklist.md#act-01) to [ACT-07](../checklist.md#act-07).

## Sample answer

> Every tool call produces one action record. It contains what triggered the action (the chat turn and dispute ID), the model and version that proposed it, the prompt and config versions, the tool and its arguments (sensitive fields redacted at write time), the documents retrieved, every outbound call made, the response from your system, and timestamps. Records share a trace ID with the conversation, so a full case can be exported in one step. For any dispute ID we can produce the complete record set within 15 minutes; a redacted sample is attached.
>
> Model provider, model name and pinned version are stored on every record. Our model inventory keeps retired versions with their active date ranges, so a record from last year still resolves to the exact model that produced it.
>
> For customer-facing conduct rules, each conversation record stores the AI disclosure shown, the customer's local time at first contact and the contact count in the current period, with the rule-set version applied.

## Example record

```json
{
  "action_id": "act_01HZX…7Q",
  "trace_id": "tr_5c1e…90",
  "trigger": { "type": "chat_turn", "conversation_id": "conv_…a1", "dispute_id": "D-88213" },
  "model": { "provider": "provider-a", "name": "model-x", "version": "2026-08-01" },
  "versions": { "prompt": "pr-31", "config": "cfg-9", "policy": "p-14" },
  "sources": [
    { "type": "transaction", "id": "txn_…88", "retrieved_at": "2026-10-02T09:14:03Z" },
    { "type": "kb_article", "id": "kb-dispute-faq", "version": "v7" }
  ],
  "outbound_calls": [
    { "service": "provider-a", "endpoint": "chat.completions", "region": "eu-west" },
    { "service": "bank-card-servicing", "endpoint": "POST /credits", "region": "bank-dc-1" }
  ],
  "tool": "issue_provisional_credit",
  "arguments": { "dispute_id": "D-88213", "amount_usd": 42.10, "account_ref": "[REDACTED:acct]" },
  "agent_claim": "Issued provisional credit of $42.10 for dispute D-88213.",
  "system_response": { "status": 201, "credit_id": "CR-55120", "amount_usd": 42.10 },
  "conduct": { "ai_disclosure": "shown", "customer_local_time": "10:14", "contacts_this_period": 1, "ruleset": "conduct-r4" },
  "started_at": "2026-10-02T09:14:05.112Z",
  "finished_at": "2026-10-02T09:14:05.871Z"
}
```
