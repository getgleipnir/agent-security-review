# RET · Retention — sample answer

Covers [RET-01](../checklist.md#ret-01) to [RET-04](../checklist.md#ret-04).

## Sample answer

> We log every agent action (see ACT), every policy decision and every human review, in addition to infrastructure logs. Action records are kept for the period set in your contract, by default 7 years for financial customers. Infrastructure logs are kept for 1 year.
>
> Records are delivered continuously to a storage bucket you control (S3 or GCS, your account), in the same signed format, so your copy is verifiable without us. You can also pull records through the export API or receive a scheduled monthly bundle. SIEM export is available in JSON over syslog or HTTPS.
>
> On termination, we deliver a final signed bundle and the verification material, wait for your confirmation, then delete our copy and send a deletion certificate.

## Example retention configuration

```yaml
customer: bank-example
action_records:
  retention: 7y
  buyer_copy: s3://bank-example-agent-records/acme/   # written continuously
  format: signed-jsonl-v1
infrastructure_logs:
  retention: 1y
exports:
  siem: https://siem.bank-example.internal/ingest  # JSON over HTTPS
  monthly_bundle: true
exit:
  final_bundle: true
  delete_after_confirmation: true
```
