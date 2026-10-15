<!-- Generated from checklist.yaml by scripts/build.py. Do not edit by hand. -->

# Autonomous Action Runtime Management (AARM) specification, Cloud Security Alliance AARM Working Group

- Source: <https://aarm.dev/spec>
- Version used: v1.0, February 2026 (arXiv:2602.09433); donated by Vanta to CSA 2026-04-30; v2.0 planned
- Type: Industry framework
- Access: public (CC BY 4.0)
- Checked: 2026-10-15

| Control | What it covers | Checklist items | How we checked |
|---|---|---|---|
| [R1](https://arxiv.org/abs/2602.09433) | Intercept actions before execution; denied actions must have no effect, no fail-open mode | [ACC-01](../checklist.md#acc-01) | verified |
| [R2](https://arxiv.org/abs/2602.09433) | Should keep session context as an append-only, hash-chained log | [TMP-01](../checklist.md#tmp-01) | verified |
| [R3](https://arxiv.org/abs/2602.09433) | Evaluate each action against static policy and alignment with the user's stated intent | [ACC-03](../checklist.md#acc-03) | verified |
| [R4](https://arxiv.org/abs/2602.09433) | STEP_UP blocks the action until an approver decides; deny on timeout recommended | [HUM-01](../checklist.md#hum-01) | verified |
| [R5](https://arxiv.org/abs/2602.09433) | Signed receipt per action with tool, parameters, context, identity, decision and outcome; Receipt includes execution result and error details, not only the decision; Cryptographically signed receipts for all actions, over a canonical serialization; Receipt signatures verifiable offline with published public keys; Receipt records approver identity, decision and timestamp | [ACT-01](../checklist.md#act-01), [HUM-01](../checklist.md#hum-01), [OUT-01](../checklist.md#out-01), [TMP-01](../checklist.md#tmp-01), [TMP-02](../checklist.md#tmp-02) | verified |
| [R5 / R6](https://arxiv.org/abs/2602.09433) | Receipts with identity binding support forensic reconstruction of actions | [INC-01](../checklist.md#inc-01) | verified |
| [R6](https://arxiv.org/abs/2602.09433) | Bind each action to human principal, service identity, agent identity and privilege scope | [ACC-02](../checklist.md#acc-02) | verified |
| [R8](https://arxiv.org/abs/2602.09433) | Should stream telemetry to SIEM in a standard schema (OCSF, CEF) plus batch export | [RET-01](../checklist.md#ret-01) | verified |
| [R9](https://arxiv.org/abs/2602.09433) | Should scope credentials per action (just-in-time, operation-specific) | [ACC-01](../checklist.md#acc-01) | verified |
| [Sec. VI.D](https://arxiv.org/abs/2602.09433) | Vendor-side integrations must let customers export or receive receipts for their audit trail | [RET-02](../checklist.md#ret-02) | verified |
