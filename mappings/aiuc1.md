<!-- Generated from checklist.yaml by scripts/build.py. Do not edit by hand. -->

# AIUC-1, the AI agent standard (Artificial Intelligence Underwriting Company)

- Source: <https://standard.aiuc-1.com/>
- Version used: October 15, 2026 release (quarterly; next due 2027-01-15)
- Type: Certifiable standard
- Access: public
- Checked: 2026-10-15

| Control | What it covers | Checklist items | How we checked |
|---|---|---|---|
| [A001](https://standard.aiuc-1.com/data-and-privacy/establish-data-use-policy) | Input data policy on training use, retention and customer rights; enforced retention and deletion | [DAT-01](../checklist.md#dat-01) | verified |
| [A002](https://standard.aiuc-1.com/data-and-privacy/define-output-rights) | Output ownership, opt-out and deletion policy | [DAT-01](../checklist.md#dat-01) | verified |
| [A003](https://standard.aiuc-1.com/data-and-privacy/implement-contextual-data-safeguards) | Limit agent data access by task, user role, agent role and context | [ACC-01](../checklist.md#acc-01) | verified |
| [A003.2](https://standard.aiuc-1.com/data-and-privacy/implement-contextual-data-safeguards) | Agent identity management (supplemental) | [ACC-02](../checklist.md#acc-02) | verified |
| [A006](https://standard.aiuc-1.com/data-and-privacy/prevent-pii-leakage) | Prevent personal data leakage through outputs and logs | [DAT-02](../checklist.md#dat-02) | verified |
| [B002](https://standard.aiuc-1.com/security/detect-adversarial-input) | Detect and respond to adversarial inputs and prompt injection attempts | [ACC-03](../checklist.md#acc-03) | verified |
| [B005](https://standard.aiuc-1.com/security/implement-real-time-input-filtering) | Filter inputs before they reach the model | [ACC-03](../checklist.md#acc-03) | verified |
| [B006](https://standard.aiuc-1.com/security/enforce-contextual-access-controls) | Technical limits on agent actions to authorized scope, with alerting on boundary breaches | [ACC-01](../checklist.md#acc-01) | verified |
| [C002](https://standard.aiuc-1.com/safety/conduct-pre-deployment-testing) | Pre-deployment testing of changes with risk assessment and approval sign-off | [CHG-02](../checklist.md#chg-02) | verified |
| [C007](https://standard.aiuc-1.com/safety/flag-high-risk-recommendations) | Flag high-risk outputs for human review | [HUM-01](../checklist.md#hum-01) | verified |
| [C008](https://standard.aiuc-1.com/safety/monitor-ai-risk-categories) | Ongoing monitoring of AI outputs across risk categories | [CHG-04](../checklist.md#chg-04) | verified |
| [C009](https://standard.aiuc-1.com/safety/collect-real-time-feedback) | Real-time user intervention; intervention logs reviewed (supplemental) | [HUM-02](../checklist.md#hum-02) | verified |
| [D003.1](https://standard.aiuc-1.com/reliability/restrict-unsafe-tool-calls) | Tool call validation and authorization | [ACC-01](../checklist.md#acc-01) | verified |
| [D003.3](https://standard.aiuc-1.com/reliability/restrict-unsafe-tool-calls) | Tool call log | [ACT-01](../checklist.md#act-01) | verified |
| [D003.4](https://standard.aiuc-1.com/reliability/restrict-unsafe-tool-calls) | Human approval for sensitive tool operations (core control since Oct 2026) | [HUM-01](../checklist.md#hum-01) | verified |
| [E001](https://standard.aiuc-1.com/accountability/ai-failure-plan-for-security-breaches) | Breach plan covers evidence collection and preservation for legal review; Failure plan for AI privacy and security breaches with notification procedures | [INC-01](../checklist.md#inc-01), [INC-02](../checklist.md#inc-02) | verified |
| [E002](https://standard.aiuc-1.com/accountability/ai-failure-plan-for-harmful-outputs) | Failure plan for harmful outputs with customer communication protocols | [INC-02](../checklist.md#inc-02) | verified |
| [E004](https://standard.aiuc-1.com/accountability/assign-accountability) | Define changes needing approval (model, system prompt, guardrails); named approver and records | [CHG-02](../checklist.md#chg-02) | verified |
| [E006](https://standard.aiuc-1.com/accountability/conduct-vendor-due-diligence) | Due diligence on foundation and upstream model providers: data handling, PII, security | [SUB-01](../checklist.md#sub-01) | verified |
| [E009](https://standard.aiuc-1.com/accountability/monitor-3rd-party-access) | Log third-party API connections, sessions and data access | [ACT-03](../checklist.md#act-03) | verified |
| [E011](https://standard.aiuc-1.com/accountability/record-processing-locations) | Document AI data processing locations | [SUB-01](../checklist.md#sub-01) | verified |
| [E015](https://standard.aiuc-1.com/accountability/log-model-activity) | Mandatory logging of AI system processes, actions and agent outputs for investigation and audit; Logs must support incident investigation and explanation of behaviour | [ACT-01](../checklist.md#act-01), [INC-01](../checklist.md#inc-01) | verified |
| [E015.2](https://standard.aiuc-1.com/accountability/log-model-activity) | Agent provenance metadata per execution, e.g. agent type and deployment origin (supplemental); Tool call parameters and results, sub-agent delegations, approvals and reasoning traces (supplemental); Tool call results logged alongside parameters (supplemental); Approval records linked to execution: approver, timestamp, decision (supplemental) | [ACC-02](../checklist.md#acc-02), [ACT-01](../checklist.md#act-01), [HUM-01](../checklist.md#hum-01), [OUT-01](../checklist.md#out-01) | verified |
| [E015.3](https://standard.aiuc-1.com/accountability/log-model-activity) | Log storage with access controls, retention and sanitation; Log storage with defined retention periods, access controls and PII masking; Data sanitation in log storage | [DAT-02](../checklist.md#dat-02), [RET-01](../checklist.md#ret-01), [TMP-03](../checklist.md#tmp-03) | verified |
| [E015.4](https://standard.aiuc-1.com/accountability/log-model-activity) | Tamper-evident logs; gaps, omissions and reordering detectable (supplemental); Logs independently verifiable (supplemental); no verification method specified | [TMP-01](../checklist.md#tmp-01), [TMP-02](../checklist.md#tmp-02) | verified |
| [E016](https://standard.aiuc-1.com/accountability/implement-ai-disclosure-mechanisms) | Disclose AI interaction (text, voice) and when autonomous agents perform actions | [ACT-07](../checklist.md#act-07) | verified |
